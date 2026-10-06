"""
Full Tier 1 + Tier 2 Validation Pipeline
Aerospace Structural Design Dataset
Academic-grade validation for all 18+ synthetic datasets.
"""
import os
import sys
import json
import logging
import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import ks_2samp, entropy, wasserstein_distance, chi2_contingency, pearsonr, spearmanr, f_oneway
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# ── Constants ──────────────────────────────────────────────────────────────────
REAL_PATH = r"d:\aero\aerospace_structural_design_dataset.csv"
SYN_DIR   = r"d:\aero\final\per_model_datasets"
OUT_DIR   = r"d:\aero\final\validation_reports"
PLOT_DIR  = r"d:\aero\final\reports\plots"
EXP_DIR   = r"d:\aero\final\experiments"
SEED      = 42

# Exact Feature Reference ranges (from brief)
FEATURE_RANGES = {
    "E (GPa)":                  (50.1,   199.8),
    "ν":                        (0.30,   0.35),
    "ρ (kg/m³)":                (1521,   4496),
    "Tensile Strength (MPa)":   (261,    1496),
    "Young's Modulus":          (50,     99.6),
    "Altitude (m)":             (5086,   19963),
    "Temperature (°C)":         (-60,    -40),
    "Pressure (Pa)":            (100172, 199839),
    "Operational Life (years)": (20,     39),
    "Wing Span (m)":            (20,     59.7),
    "Fuselage Length (m)":      (30,     70),
    "Structural Thickness (mm)":(5,      14.9),
    "Number of Iterations":     (523,    1983),
    "Optimization Time (sec)":  (51.5,   149.8),
}

CATEGORICAL_LEVELS = {
    "Material Type":          {"Aluminum", "Titanium", "Carbon Fiber"},
    "Structural Shape":       {"Rectangular", "Cylindrical", "Tapered"},
    "Load Distribution":      {"uniform", "point load", "distributed"},
    "Quantum Algorithm Type": {"Chaotic Quantum Genetic", "Shark Optimizer"},
}

TARGETS = ["Vibration Damping", "Computational Time", "Weight Efficiency", "Durability"]
TARGET_LEVELS = {
    "Vibration Damping": {"Low", "Moderate", "High"},
    "Computational Time": {"Short", "Medium", "Long"},
    "Weight Efficiency": {"Poor", "Good", "Excellent"},
    "Durability": {"Low", "Medium", "High"},
}

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def encode_df(df, cat_cols):
    """Label-encode categoricals for ML tasks."""
    enc = df.copy()
    for c in cat_cols:
        enc[c] = LabelEncoder().fit_transform(enc[c].astype(str))
    return enc


def tier1_check(real_df, syn_df, dataset_name):
    """
    Tier 1 — Minimum Bar.
    Returns (results_dict, pass_all_bool).
    """
    results = {}

    # 1. Schema — check same columns (order-insensitive, then reorder syn_df to match)
    real_cols = list(real_df.columns)
    syn_cols  = list(syn_df.columns)
    missing_cols = set(real_cols) - set(syn_cols)
    extra_cols   = set(syn_cols)  - set(real_cols)
    schema_ok = (not missing_cols) and (not extra_cols) and len(real_cols) == len(syn_cols)
    # Reorder synthetic columns to match real column order
    if schema_ok and syn_cols != real_cols:
        syn_df = syn_df[real_cols]
    results["schema_match"] = {"pass": schema_ok,
                                "detail": f"Expected {len(real_cols)} cols, got {len(syn_cols)}. "
                                          + ("" if schema_ok else f"Missing: {missing_cols}, Extra: {extra_cols}")}

    # 2. Nulls
    nulls = int(syn_df.isnull().sum().sum())
    results["null_check"] = {"pass": nulls == 0, "detail": f"{nulls} null values"}

    # 3. Numeric ranges — synthetic must stay within REAL DATA bounds (+ 1% tolerance)
    #    Feature Reference values are documented separately for reference
    range_failures = []
    num_cols_real = real_df.select_dtypes(include=np.number).columns.tolist()
    for col in num_cols_real:
        if col not in syn_df.columns:
            continue
        r_min, r_max = float(real_df[col].min()), float(real_df[col].max())
        s_min, s_max = float(syn_df[col].min()), float(syn_df[col].max())
        tol = max(abs(r_max - r_min) * 0.01, 1e-4)
        if s_min < r_min - tol or s_max > r_max + tol:
            range_failures.append(f"{col}: got [{s_min:.3f}, {s_max:.3f}], real bounds [{r_min:.3f}, {r_max:.3f}]")
    results["range_check"] = {"pass": len(range_failures) == 0,
                               "detail": "; ".join(range_failures) if range_failures else "All within real-data bounds"}

    # 4. Categorical levels
    cat_failures = []
    all_cats = {**CATEGORICAL_LEVELS, **TARGET_LEVELS}
    for col, expected in all_cats.items():
        if col not in syn_df.columns:
            cat_failures.append(f"{col}: MISSING")
            continue
        actual = set(syn_df[col].unique())
        if not actual.issubset(expected):
            cat_failures.append(f"{col}: unexpected levels {actual - expected}")
        missing = expected - actual
        if missing:
            cat_failures.append(f"{col}: missing levels {missing}")
    results["categorical_check"] = {"pass": len(cat_failures) == 0,
                                     "detail": "; ".join(cat_failures) if cat_failures else "All levels valid"}

    # 5. Row count
    n = len(syn_df)
    results["row_count"] = {"pass": n >= 300, "detail": f"{n} rows"}

    # 6. Class degeneracy (no target class with 0 rows)
    degenerate = []
    for t, levels in TARGET_LEVELS.items():
        if t not in syn_df.columns:
            continue
        counts = syn_df[t].value_counts()
        for lvl in levels:
            if counts.get(lvl, 0) == 0:
                degenerate.append(f"{t}:{lvl}=0")
    results["class_degeneracy"] = {"pass": len(degenerate) == 0,
                                    "detail": "; ".join(degenerate) if degenerate else "All classes populated"}

    # 7. Duplicate rows
    n_dup = int(syn_df.duplicated().sum())
    dup_pct = n_dup / len(syn_df) * 100
    results["duplicate_rows"] = {"pass": True,  # warn not fail
                                   "detail": f"{n_dup} duplicates ({dup_pct:.1f}%)"}

    pass_all = all(v["pass"] for k, v in results.items() if k != "duplicate_rows")
    return results, pass_all


def tier2_check(real_df, syn_df, model_name, plot_prefix):
    """
    Tier 2 — Statistical Fidelity, ML Utility, Rare Case Realism.
    Returns metrics dict.
    """
    metrics = {}
    num_cols = [c for c in real_df.select_dtypes(include=np.number).columns]
    cat_cols = [c for c in real_df.select_dtypes(exclude=np.number).columns
                if c not in TARGETS]
    features = [c for c in real_df.columns if c not in TARGETS]

    # ── KS tests ────────────────────────────────────────────────────────────
    ks_results = {}
    ks_pvals   = []
    for c in num_cols:
        if c not in syn_df.columns:
            continue
        stat, pval = ks_2samp(real_df[c].dropna(), syn_df[c].dropna())
        ks_results[c] = {"statistic": float(stat), "pvalue": float(pval), "pass": pval > 0.05}
        ks_pvals.append(pval)
    ks_pass_rate = float(np.mean([v["pass"] for v in ks_results.values()]))
    metrics["ks_pass_rate"] = round(ks_pass_rate, 4)
    metrics["ks_mean_pvalue"] = round(float(np.mean(ks_pvals)), 4)
    metrics["ks_details"] = ks_results

    # ── KL divergence ───────────────────────────────────────────────────────
    kl_vals = []
    for c in num_cols:
        if c not in syn_df.columns:
            continue
        lo = min(real_df[c].min(), syn_df[c].min())
        hi = max(real_df[c].max(), syn_df[c].max())
        bins = np.linspace(lo, hi, 31)
        r_hist, _ = np.histogram(real_df[c], bins=bins, density=True)
        s_hist, _ = np.histogram(syn_df[c], bins=bins, density=True)
        r_hist = r_hist + 1e-10
        s_hist = s_hist + 1e-10
        r_hist /= r_hist.sum()
        s_hist /= s_hist.sum()
        kl = float(entropy(r_hist, s_hist))
        kl_vals.append(kl)
    metrics["mean_kl_divergence"] = round(float(np.mean(kl_vals)), 4)

    # ── Wasserstein distance ─────────────────────────────────────────────────
    wass_vals = []
    for c in num_cols:
        if c not in syn_df.columns:
            continue
        scaler = StandardScaler().fit(real_df[[c]])
        r_scaled = scaler.transform(real_df[[c]]).flatten()
        s_scaled = scaler.transform(syn_df[[c]]).flatten()
        wass_vals.append(float(wasserstein_distance(r_scaled, s_scaled)))
    metrics["mean_wasserstein"] = round(float(np.mean(wass_vals)), 4)

    # ── Jensen-Shannon divergence ────────────────────────────────────────────
    def js_div(p, q):
        m = 0.5 * (p + q)
        return float(0.5 * entropy(p, m) + 0.5 * entropy(q, m))

    js_vals = []
    for c in num_cols:
        if c not in syn_df.columns:
            continue
        lo = min(real_df[c].min(), syn_df[c].min())
        hi = max(real_df[c].max(), syn_df[c].max())
        bins = np.linspace(lo, hi, 31)
        r_h, _ = np.histogram(real_df[c], bins=bins, density=True)
        s_h, _ = np.histogram(syn_df[c], bins=bins, density=True)
        r_h = r_h + 1e-10; r_h /= r_h.sum()
        s_h = s_h + 1e-10; s_h /= s_h.sum()
        js_vals.append(js_div(r_h, s_h))
    metrics["mean_js_divergence"] = round(float(np.mean(js_vals)), 4)

    # ── Correlation Preservation Score ──────────────────────────────────────
    r_num = real_df[num_cols].fillna(0)
    s_num = syn_df[num_cols].fillna(0)
    r_corr = r_num.corr(method='pearson').fillna(0).values
    s_corr = s_num.corr(method='pearson').fillna(0).values
    if r_corr.shape == s_corr.shape:
        frob_norm = float(np.linalg.norm(r_corr - s_corr, 'fro'))
        metrics["corr_frobenius_norm"] = round(frob_norm, 4)
    else:
        metrics["corr_frobenius_norm"] = None

    # ── TSTR ────────────────────────────────────────────────────────────────
    r_enc = encode_df(real_df, cat_cols + [c for c in TARGETS if c in real_df.columns])
    s_enc = encode_df(syn_df, cat_cols + [c for c in TARGETS if c in syn_df.columns])

    tstr_scores = {}
    tstr_f1 = {}
    for t in TARGETS:
        if t not in syn_df.columns:
            continue
        try:
            feat_cols = [c for c in features if c in r_enc.columns and c in s_enc.columns]
            rf = RandomForestClassifier(n_estimators=100, random_state=SEED)
            rf.fit(s_enc[feat_cols], s_enc[t])
            preds = rf.predict(r_enc[feat_cols])
            tstr_scores[t] = round(float(accuracy_score(r_enc[t], preds)), 4)
            tstr_f1[t] = round(float(f1_score(r_enc[t], preds, average='macro')), 4)
        except Exception as e:
            tstr_scores[t] = 0.0
            tstr_f1[t] = 0.0
    metrics["tstr_accuracy"] = tstr_scores
    metrics["tstr_macro_f1"] = tstr_f1
    metrics["tstr_mean_accuracy"] = round(float(np.mean(list(tstr_scores.values()))), 4)
    metrics["tstr_mean_f1"] = round(float(np.mean(list(tstr_f1.values()))), 4)

    # ── TRTS ────────────────────────────────────────────────────────────────
    trts_scores = {}
    for t in TARGETS:
        if t not in syn_df.columns:
            continue
        try:
            feat_cols = [c for c in features if c in r_enc.columns and c in s_enc.columns]
            rf = RandomForestClassifier(n_estimators=100, random_state=SEED)
            rf.fit(r_enc[feat_cols], r_enc[t])
            preds = rf.predict(s_enc[feat_cols])
            trts_scores[t] = round(float(accuracy_score(s_enc[t], preds)), 4)
        except:
            trts_scores[t] = 0.0
    metrics["trts_accuracy"] = trts_scores
    metrics["trts_mean_accuracy"] = round(float(np.mean(list(trts_scores.values()))), 4)

    # ── Feature Importance Alignment (FI-MAE) ────────────────────────────────
    fi_maes = {}
    feat_cols = [c for c in features if c in r_enc.columns and c in s_enc.columns]
    for t in TARGETS:
        if t not in syn_df.columns:
            continue
        try:
            rf_r = RandomForestClassifier(n_estimators=100, random_state=SEED).fit(r_enc[feat_cols], r_enc[t])
            rf_s = RandomForestClassifier(n_estimators=100, random_state=SEED).fit(s_enc[feat_cols], s_enc[t])
            fi_maes[t] = round(float(np.mean(np.abs(rf_r.feature_importances_ - rf_s.feature_importances_))), 4)
        except:
            fi_maes[t] = None
    metrics["fi_mae"] = fi_maes
    valid_fis = [v for v in fi_maes.values() if v is not None]
    metrics["mean_fi_mae"] = round(float(np.mean(valid_fis)), 4) if valid_fis else None

    # ── Isolation Forest ────────────────────────────────────────────────────
    try:
        iso = IsolationForest(contamination=0.05, random_state=SEED)
        iso.fit(r_num)
        s_num_aligned = syn_df[num_cols].fillna(0)
        s_preds = iso.predict(s_num_aligned)
        anomaly_count = int(np.sum(s_preds == -1))
        anomaly_rate  = round(float(anomaly_count / len(syn_df)), 4)
        metrics["isolation_forest_anomaly_rate"] = anomaly_rate
        metrics["isolation_forest_anomaly_pct"]  = round(anomaly_rate * 100, 2)

        # Distance of synthetic anomalies to real anomalies
        r_preds = iso.predict(r_num)
        real_anom = r_num.iloc[r_preds == -1]
        syn_anom  = s_num_aligned.iloc[s_preds == -1]

        if len(real_anom) > 0 and len(syn_anom) > 0:
            scaler = StandardScaler().fit(r_num)
            ra_scaled = scaler.transform(real_anom)
            sa_scaled = scaler.transform(syn_anom)
            nn = NearestNeighbors(n_neighbors=1).fit(ra_scaled)
            dists, _ = nn.kneighbors(sa_scaled)
            metrics["anomaly_distance_mean"] = round(float(np.mean(dists)), 4)
        else:
            metrics["anomaly_distance_mean"] = None
    except Exception as e:
        metrics["isolation_forest_anomaly_rate"] = None
        metrics["isolation_forest_anomaly_pct"]  = None
        metrics["anomaly_distance_mean"] = None

    # ── Nearest-Neighbor Distance (synthetic vs real) ────────────────────────
    try:
        scaler = StandardScaler().fit(r_num)
        r_sc = scaler.transform(r_num)
        s_sc = scaler.transform(syn_df[num_cols].fillna(0))
        nn = NearestNeighbors(n_neighbors=1).fit(r_sc)
        nn_dists, _ = nn.kneighbors(s_sc)
        metrics["nn_distance_mean"]   = round(float(np.mean(nn_dists)), 4)
        metrics["nn_distance_median"] = round(float(np.median(nn_dists)), 4)
        metrics["nn_distance_p95"]    = round(float(np.percentile(nn_dists, 95)), 4)
    except:
        metrics["nn_distance_mean"]   = None
        metrics["nn_distance_median"] = None
        metrics["nn_distance_p95"]    = None

    # ── MMD (Maximum Mean Discrepancy) ──────────────────────────────────────
    try:
        scaler = StandardScaler().fit(r_num)
        X = scaler.transform(r_num)
        Y = scaler.transform(syn_df[num_cols].fillna(0))
        # RBF kernel MMD
        n, m = len(X), len(Y)
        # Subsample for speed
        idx_x = np.random.choice(n, min(n, 200), replace=False)
        idx_y = np.random.choice(m, min(m, 200), replace=False)
        Xs, Ys = X[idx_x], Y[idx_y]
        sigma = np.median(np.pairwise_distances_chunked_dummy if False else
                          [1.0])[0] if False else 1.0
        # Simple MMD2 with RBF
        def rbf_kernel(A, B, sigma=1.0):
            dists = np.sum((A[:, None] - B[None, :]) ** 2, axis=2)
            return np.exp(-dists / (2 * sigma ** 2))
        Kxx = rbf_kernel(Xs, Xs)
        Kyy = rbf_kernel(Ys, Ys)
        Kxy = rbf_kernel(Xs, Ys)
        mmd2 = (np.mean(Kxx) + np.mean(Kyy) - 2 * np.mean(Kxy))
        metrics["mmd_score"] = round(float(max(0, mmd2)), 6)
    except:
        metrics["mmd_score"] = None

    # ── Discriminator Test ───────────────────────────────────────────────────
    try:
        from sklearn.ensemble import GradientBoostingClassifier
        feat_cols_num = [c for c in num_cols if c in syn_df.columns]
        real_sub = real_df[feat_cols_num].fillna(0).copy()
        syn_sub  = syn_df[feat_cols_num].fillna(0).copy()
        # Balance sample sizes
        n_disc = min(len(real_sub), len(syn_sub), 300)
        Xr = real_sub.sample(n_disc, random_state=SEED)
        Xs = syn_sub.sample(n_disc, random_state=SEED)
        X_disc = pd.concat([Xr, Xs], axis=0).values
        y_disc = np.array([0] * n_disc + [1] * n_disc)
        from sklearn.model_selection import cross_val_score
        clf = RandomForestClassifier(n_estimators=50, random_state=SEED)
        scores = cross_val_score(clf, X_disc, y_disc, cv=3, scoring='roc_auc')
        metrics["discriminator_auc"] = round(float(np.mean(scores)), 4)
    except:
        metrics["discriminator_auc"] = None

    # ── Class Balance Chi-square ────────────────────────────────────────────
    chi2_results = {}
    for t in TARGETS:
        if t not in syn_df.columns:
            continue
        try:
            r_counts = real_df[t].value_counts()
            s_counts = syn_df[t].value_counts()
            all_levels = sorted(set(r_counts.index) | set(s_counts.index))
            r_vec = np.array([r_counts.get(l, 0) for l in all_levels])
            s_vec = np.array([s_counts.get(l, 0) for l in all_levels])
            # Chi-square: does synthetic match real distribution?
            s_expected = r_vec / r_vec.sum() * s_vec.sum()
            chi2_stat = float(np.sum((s_vec - s_expected) ** 2 / (s_expected + 1e-10)))
            chi2_results[t] = {"chi2": round(chi2_stat, 4), "dof": len(all_levels) - 1}
        except:
            chi2_results[t] = None
    metrics["chi2_class_balance"] = chi2_results

    # ── GMM Log-Likelihood ───────────────────────────────────────────────────
    try:
        scaler = StandardScaler().fit(r_num)
        r_sc = scaler.transform(r_num)
        s_sc = scaler.transform(syn_df[num_cols].fillna(0))
        gmm = GaussianMixture(n_components=5, random_state=SEED)
        gmm.fit(r_sc)
        ll = float(np.mean(gmm.score_samples(s_sc)))
        metrics["gmm_log_likelihood"] = round(ll, 4)
    except:
        metrics["gmm_log_likelihood"] = None

    # ── Generate Comparison Plots ────────────────────────────────────────────
    os.makedirs(PLOT_DIR, exist_ok=True)

    # Histogram comparison (top 6 numeric)
    top_num = [c for c in num_cols if c in syn_df.columns][:6]
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    for i, c in enumerate(top_num):
        axes[i].hist(real_df[c], bins=25, alpha=0.6, color='steelblue', label='Real', density=True)
        axes[i].hist(syn_df[c], bins=25, alpha=0.6, color='tomato', label='Synthetic', density=True)
        axes[i].set_title(c, fontsize=10)
        axes[i].legend(fontsize=8)
    plt.suptitle(f"Histogram Comparison — {model_name}", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{plot_prefix}_histograms.png", dpi=150, bbox_inches='tight')
    plt.close()

    # Class balance comparison
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    for i, t in enumerate(TARGETS):
        if t not in syn_df.columns:
            continue
        r_c = real_df[t].value_counts(normalize=True).sort_index()
        s_c = syn_df[t].value_counts(normalize=True).sort_index()
        idx = sorted(set(r_c.index) | set(s_c.index))
        x = np.arange(len(idx)); w = 0.35
        axes[i].bar(x - w/2, [r_c.get(k, 0) for k in idx], w, label='Real', color='steelblue')
        axes[i].bar(x + w/2, [s_c.get(k, 0) for k in idx], w, label='Synthetic', color='tomato')
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(idx, rotation=30, fontsize=8)
        axes[i].set_title(t, fontsize=9)
        if i == 0:
            axes[i].legend()
    plt.suptitle(f"Class Balance — {model_name}")
    plt.tight_layout()
    plt.savefig(f"{plot_prefix}_class_balance.png", dpi=150, bbox_inches='tight')
    plt.close()

    # PCA overlay
    try:
        common_num = [c for c in num_cols if c in syn_df.columns]
        scaler = StandardScaler()
        r_sc = scaler.fit_transform(real_df[common_num].fillna(0))
        s_sc = scaler.transform(syn_df[common_num].fillna(0))
        pca = PCA(n_components=2, random_state=SEED)
        r_pca = pca.fit_transform(r_sc)
        s_pca = pca.transform(s_sc)
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.scatter(r_pca[:, 0], r_pca[:, 1], alpha=0.5, c='steelblue', label=f'Real (n={len(r_pca)})', s=20)
        ax.scatter(s_pca[:, 0], s_pca[:, 1], alpha=0.4, c='tomato',    label=f'Synthetic (n={len(s_pca)})', s=10)
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
        ax.set_title(f"PCA Overlay — {model_name}")
        ax.legend()
        plt.tight_layout()
        plt.savefig(f"{plot_prefix}_pca.png", dpi=150, bbox_inches='tight')
        plt.close()
    except:
        pass

    return metrics


def build_validation_report(dataset_name, t1_results, t1_pass, t2_metrics, real_df, syn_df, plot_prefix_rel):
    """Build a Markdown validation report."""
    lines = [
        f"# Validation Report: {dataset_name}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Table of Contents",
        "1. [Tier 1 — Minimum Bar](#tier-1--minimum-bar)",
        "2. [Tier 2 — Statistical Fidelity](#tier-2--statistical-fidelity)",
        "3. [Tier 2 — ML Utility (TSTR/TRTS)](#tier-2--ml-utility)",
        "4. [Tier 2 — Rare Case Realism](#tier-2--rare-case-realism)",
        "5. [Tier 2 — Overall Similarity](#tier-2--overall-similarity)",
        "6. [Class Balance](#class-balance)",
        "7. [Conclusion](#conclusion)",
        "",
        "---",
        "",
        "## Tier 1 — Minimum Bar",
        "",
        f"**Overall Tier 1 Result: {'✅ PASS' if t1_pass else '❌ FAIL'}**",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]

    check_labels = {
        "schema_match": "Schema Match (22 columns)",
        "null_check": "Null Values",
        "range_check": "Numeric Range Compliance",
        "categorical_check": "Categorical Level Validity",
        "row_count": "Row Count (≥ 300)",
        "class_degeneracy": "Class Degeneracy Check",
        "duplicate_rows": "Duplicate Rows (informational)",
    }

    for key, label in check_labels.items():
        res = t1_results.get(key, {})
        icon = "✅" if res.get("pass") else "❌"
        detail = res.get("detail", "N/A")
        lines.append(f"| {label} | {icon} | {detail} |")

    lines += [
        "",
        "---",
        "",
        "## Tier 2 — Statistical Fidelity",
        "",
        "| Metric | Value | Interpretation |",
        "|---|---|---|",
        f"| KS Pass Rate | {t2_metrics.get('ks_pass_rate', 'N/A')} | Fraction of features with KS p-value > 0.05 |",
        f"| Mean KS p-value | {t2_metrics.get('ks_mean_pvalue', 'N/A')} | Higher = more similar distributions |",
        f"| Mean KL Divergence | {t2_metrics.get('mean_kl_divergence', 'N/A')} | Lower = better (0 = identical) |",
        f"| Mean Wasserstein Distance | {t2_metrics.get('mean_wasserstein', 'N/A')} | Lower = better (normalized) |",
        f"| Mean JS Divergence | {t2_metrics.get('mean_js_divergence', 'N/A')} | Lower = better (0–1 bounded) |",
        f"| Correlation Frobenius Norm | {t2_metrics.get('corr_frobenius_norm', 'N/A')} | Lower = better (0 = identical) |",
        "",
        "### Per-Feature KS Test Results",
        "",
        "| Feature | KS Statistic | p-value | Pass (p > 0.05) |",
        "|---|---|---|---|",
    ]

    ks_det = t2_metrics.get("ks_details", {})
    for feat, v in ks_det.items():
        stat = f"{v['statistic']:.4f}"
        pval = f"{v['pvalue']:.4f}"
        icon = "✅" if v["pass"] else "❌"
        lines.append(f"| {feat} | {stat} | {pval} | {icon} |")

    lines += [
        "",
        f"![Histogram Comparison]({plot_prefix_rel}_histograms.png)",
        "",
        "---",
        "",
        "## Tier 2 — ML Utility",
        "",
        "### TSTR (Train on Synthetic, Test on Real)",
        "",
        "| Target | Accuracy | Macro F1 |",
        "|---|---|---|",
    ]
    tstr_acc = t2_metrics.get("tstr_accuracy", {})
    tstr_f1  = t2_metrics.get("tstr_macro_f1", {})
    for t in TARGETS:
        acc = tstr_acc.get(t, "N/A")
        f1  = tstr_f1.get(t, "N/A")
        lines.append(f"| {t} | {acc} | {f1} |")
    lines.append(f"| **Mean** | **{t2_metrics.get('tstr_mean_accuracy', 'N/A')}** | **{t2_metrics.get('tstr_mean_f1', 'N/A')}** |")

    lines += [
        "",
        "### TRTS (Train on Real, Test on Synthetic)",
        "",
        "| Target | Accuracy |",
        "|---|---|",
    ]
    trts_acc = t2_metrics.get("trts_accuracy", {})
    for t in TARGETS:
        acc = trts_acc.get(t, "N/A")
        lines.append(f"| {t} | {acc} |")
    lines.append(f"| **Mean** | **{t2_metrics.get('trts_mean_accuracy', 'N/A')}** |")

    lines += [
        "",
        "### Feature Importance Alignment (FI-MAE)",
        "Lower MAE = synthetic data learned the same physical rules as real data.",
        "",
        "| Target | FI-MAE |",
        "|---|---|",
    ]
    fi = t2_metrics.get("fi_mae", {})
    for t in TARGETS:
        val = fi.get(t, "N/A")
        lines.append(f"| {t} | {val} |")
    lines.append(f"| **Mean** | **{t2_metrics.get('mean_fi_mae', 'N/A')}** |")

    lines += [
        "",
        "---",
        "",
        "## Tier 2 — Rare Case Realism",
        "",
        "| Metric | Value | Target |",
        "|---|---|---|",
        f"| Isolation Forest Anomaly Rate | {t2_metrics.get('isolation_forest_anomaly_pct', 'N/A')}% | ~5% |",
        f"| Mean Distance to Real Anomalies | {t2_metrics.get('anomaly_distance_mean', 'N/A')} | Lower = more realistic |",
        f"| NN Distance Mean | {t2_metrics.get('nn_distance_mean', 'N/A')} | Lower = closer to real |",
        f"| NN Distance Median | {t2_metrics.get('nn_distance_median', 'N/A')} | |",
        f"| NN Distance P95 | {t2_metrics.get('nn_distance_p95', 'N/A')} | |",
        "",
        "---",
        "",
        "## Tier 2 — Overall Similarity",
        "",
        "| Metric | Value | Interpretation |",
        "|---|---|---|",
        f"| MMD Score | {t2_metrics.get('mmd_score', 'N/A')} | Lower = more similar (0 = identical) |",
        f"| Discriminator AUC | {t2_metrics.get('discriminator_auc', 'N/A')} | Near 0.5 = indistinguishable from real |",
        f"| GMM Log-Likelihood | {t2_metrics.get('gmm_log_likelihood', 'N/A')} | Higher = more plausible |",
        "",
        f"![PCA Overlay]({plot_prefix_rel}_pca.png)",
        "",
        "---",
        "",
        "## Class Balance",
        "",
        f"![Class Balance]({plot_prefix_rel}_class_balance.png)",
        "",
        "### Chi-Square Test (Synthetic vs Real Distribution)",
        "",
        "| Target | Chi² Statistic | Degrees of Freedom |",
        "|---|---|---|",
    ]
    chi2 = t2_metrics.get("chi2_class_balance", {})
    for t in TARGETS:
        v = chi2.get(t)
        if v:
            lines.append(f"| {t} | {v['chi2']} | {v['dof']} |")
        else:
            lines.append(f"| {t} | N/A | N/A |")

    # Conclusion
    tstr_mean = t2_metrics.get("tstr_mean_accuracy", 0) or 0
    ks_pass   = t2_metrics.get("ks_pass_rate", 0) or 0
    fi_mean   = t2_metrics.get("mean_fi_mae", 1) or 1
    disc_auc  = t2_metrics.get("discriminator_auc", 1) or 1

    if tstr_mean > 0.85 and ks_pass > 0.8:
        verdict = "✅ **MEETS MINIMUM BAR** — This dataset is suitable for production use."
        grade = "A"
    elif tstr_mean > 0.60 and ks_pass > 0.5:
        verdict = "⚠️ **CONDITIONAL PASS** — Acceptable for analysis but not production."
        grade = "B"
    else:
        verdict = "❌ **DOES NOT MEET MINIMUM BAR** — This dataset should not be used."
        grade = "F"

    lines += [
        "",
        "---",
        "",
        "## Conclusion",
        "",
        f"**Dataset:** {dataset_name}",
        f"**Overall Grade:** {grade}",
        f"**Verdict:** {verdict}",
        "",
        "### Key Metrics Summary",
        f"- TSTR Mean Accuracy: **{tstr_mean:.4f}** (benchmark: >0.85 = excellent)",
        f"- KS Pass Rate: **{ks_pass:.4f}** (benchmark: >0.80 = excellent)",
        f"- Mean FI-MAE: **{fi_mean:.4f}** (benchmark: <0.01 = excellent)",
        f"- Discriminator AUC: **{disc_auc:.4f}** (benchmark: <0.6 = excellent)",
        f"- MMD Score: **{t2_metrics.get('mmd_score', 'N/A')}** (benchmark: <0.1 = excellent)",
        "",
        "---",
        "*Report generated by the Aerospace Synthetic Data Validation Pipeline v2.0*",
    ]

    return "\n".join(lines)


def compute_composite_score(t2):
    """Compute composite score per brief formula."""
    kl   = t2.get("mean_kl_divergence", 1.0) or 1.0
    f1   = t2.get("tstr_mean_f1", 0.0) or 0.0
    fi   = t2.get("mean_fi_mae", 1.0) or 1.0
    auc  = t2.get("discriminator_auc", 1.0) or 1.0
    mmd  = t2.get("mmd_score", 1.0) or 1.0
    return round(
        0.30 * (1 - min(kl, 1.0)) +
        0.30 * f1 +
        0.20 * (1 - min(fi * 10, 1.0)) +
        0.10 * (1 - min(auc, 1.0)) +
        0.10 * (1 - min(mmd, 1.0)),
        4
    )


def run_all_validations():
    """Run full validation on all datasets, save reports, build experiments CSV."""
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(EXP_DIR, exist_ok=True)

    logger.info("Loading real dataset...")
    real_df = pd.read_csv(REAL_PATH)

    all_experiments = []

    # Discover all synthetic datasets
    datasets = []
    for fname in sorted(os.listdir(SYN_DIR)):
        if fname.endswith(".csv"):
            datasets.append(os.path.join(SYN_DIR, fname))

    logger.info(f"Found {len(datasets)} synthetic datasets to validate.")

    for syn_path in datasets:
        fname = os.path.basename(syn_path)
        dname = fname.replace(".csv", "")
        logger.info(f"\n{'='*60}")
        logger.info(f"Validating: {dname}")

        try:
            syn_df = pd.read_csv(syn_path)
        except Exception as e:
            logger.error(f"  Failed to load {fname}: {e}")
            continue

        # Tier 1
        t1_results, t1_pass = tier1_check(real_df, syn_df, dname)
        t1_icon = "✅ PASS" if t1_pass else "❌ FAIL"
        logger.info(f"  Tier 1: {t1_icon}")

        # Tier 2 (only if Tier 1 schema passes)
        plot_base = os.path.join(PLOT_DIR, dname)
        plot_rel  = f"../reports/plots/{dname}"

        if not t1_results.get("schema_match", {}).get("pass"):
            logger.warning(f"  Skipping Tier 2 for {dname} — schema mismatch.")
            t2_metrics = {}
        else:
            try:
                t2_metrics = tier2_check(real_df, syn_df, dname, plot_base)
                logger.info(f"  Tier 2 complete. TSTR mean acc: {t2_metrics.get('tstr_mean_accuracy')}, "
                            f"KS pass rate: {t2_metrics.get('ks_pass_rate')}")
            except Exception as e:
                logger.error(f"  Tier 2 failed for {dname}: {e}")
                t2_metrics = {}

        # Build and save report
        report_md = build_validation_report(dname, t1_results, t1_pass, t2_metrics, real_df, syn_df, f"../reports/plots/{dname}")
        report_path = os.path.join(OUT_DIR, f"{dname}_validation.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_md)
        logger.info(f"  Report saved: {report_path}")

        # Extract model name and row count from filename
        parts = dname.split("_")
        n_rows_str = parts[-1] if parts[-1].isdigit() else "?"
        model_name = "_".join(parts[:-1]) if parts[-1].isdigit() else dname

        # Experiments row
        exp_row = {
            "dataset_name":     dname,
            "model_name":       model_name,
            "n_rows":           int(n_rows_str) if n_rows_str.isdigit() else None,
            "tier1_pass":       t1_pass,
            "ks_pass_rate":     t2_metrics.get("ks_pass_rate"),
            "ks_mean_pvalue":   t2_metrics.get("ks_mean_pvalue"),
            "mean_kl":          t2_metrics.get("mean_kl_divergence"),
            "mean_wasserstein": t2_metrics.get("mean_wasserstein"),
            "mean_js":          t2_metrics.get("mean_js_divergence"),
            "corr_frobenius":   t2_metrics.get("corr_frobenius_norm"),
            "tstr_mean_acc":    t2_metrics.get("tstr_mean_accuracy"),
            "tstr_mean_f1":     t2_metrics.get("tstr_mean_f1"),
            "trts_mean_acc":    t2_metrics.get("trts_mean_accuracy"),
            "mean_fi_mae":      t2_metrics.get("mean_fi_mae"),
            "if_anomaly_pct":   t2_metrics.get("isolation_forest_anomaly_pct"),
            "anomaly_dist_mean":t2_metrics.get("anomaly_distance_mean"),
            "nn_dist_mean":     t2_metrics.get("nn_distance_mean"),
            "mmd_score":        t2_metrics.get("mmd_score"),
            "discriminator_auc":t2_metrics.get("discriminator_auc"),
            "gmm_log_likelihood":t2_metrics.get("gmm_log_likelihood"),
            "composite_score":  compute_composite_score(t2_metrics) if t2_metrics else None,
            "timestamp":        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        all_experiments.append(exp_row)

    # Save all_experiments.csv
    exp_df = pd.DataFrame(all_experiments)
    exp_path = os.path.join(EXP_DIR, "all_experiments.csv")
    exp_df.to_csv(exp_path, index=False)
    logger.info(f"\nExperiments CSV saved: {exp_path}")

    # Print leaderboard
    logger.info("\n" + "="*70)
    logger.info("LEADERBOARD (sorted by composite score)")
    logger.info("="*70)
    if "composite_score" in exp_df.columns:
        lb = exp_df[exp_df["tier1_pass"] == True].sort_values("composite_score", ascending=False)
        for _, row in lb.iterrows():
            logger.info(f"  {row['dataset_name']:35s} | Score: {row['composite_score']:.4f} | "
                        f"TSTR: {row['tstr_mean_acc']} | KS: {row['ks_pass_rate']}")

    return exp_df


def create_real_splits():
    """Create 80/20 real train/test splits."""
    real_df = pd.read_csv(REAL_PATH)
    n = len(real_df)
    idx = np.random.RandomState(SEED).permutation(n)
    split = int(0.8 * n)
    train_df = real_df.iloc[idx[:split]].reset_index(drop=True)
    test_df  = real_df.iloc[idx[split:]].reset_index(drop=True)
    train_df.to_csv(os.path.join(EXP_DIR, "real_train_split.csv"), index=False)
    test_df.to_csv(os.path.join(EXP_DIR,  "real_test_split.csv"),  index=False)
    logger.info(f"Real splits saved: {split} train, {n-split} test")


if __name__ == "__main__":
    logger.info("Starting Full Validation Pipeline...")
    create_real_splits()
    exp_df = run_all_validations()
    logger.info("\nPipeline complete.")
