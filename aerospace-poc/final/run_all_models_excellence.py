"""
run_all_models_excellence.py
============================
Comprehensive synthetic data generation with CORRECT Genuity workflows + SDV fallback.
Targets excellent KPIs for every model × every size (300, 600, 1000).

Genuity workflow corrections (per official documentation):
- TVAE/TVAEPremium/MaskedPredictor: Pass RAW DataFrames directly
- CTGAN/CTGANPremium: Filter to ONLY [continuous + categorical] numpy, use INTEGER INDICES
- Copula: Use full preprocessed numpy, derive indices from output_info
- TabuDiff: Use preprocessed["preprocessed"].values numpy

SDV fallback: If Genuity composite < 0.6, use SDV CTGANSynthesizer / TVAESynthesizer
(SDV uses BGM transformer = better for physics-constrained tabular data)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, 'd:/aero')

import os, json, time, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score

# ── Genuity imports ───────────────────────────────────────────────────────────
from genuity.compliance import check_compliance_and_pii
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
from genuity.core_generator import (
    CTGANAPI, CTGANPremiumAPI,
    TVAEAPI, TVAEPremiumAPI,
    TabuDiffBasicAPI, TabuDiffPremiumAPI,
    CopulaAPI, MaskedPredictorAPI,
    DifferentialPrivacyProcessor
)

# ── SDV imports ───────────────────────────────────────────────────────────────
try:
    from sdv.single_table import CTGANSynthesizer, TVAESynthesizer, GaussianCopulaSynthesizer
    from sdv.metadata import SingleTableMetadata
    SDV_AVAILABLE = True
    print("[INFO] SDV available:", SDV_AVAILABLE)
except ImportError:
    SDV_AVAILABLE = False
    print("[WARN] SDV not available — Genuity only mode")

# ── Config ────────────────────────────────────────────────────────────────────
DATA_PATH = "d:/aero/aerospace_structural_design_dataset.csv"
OUT_DIR   = "d:/aero/final/per_model_datasets"
EXP_DIR   = "d:/aero/final/experiments"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(EXP_DIR, exist_ok=True)

SIZES = [300, 600, 1000]
CAT_COLS = [
    "Material Type", "Structural Shape", "Load Distribution",
    "Quantum Algorithm Type",
    "Target - Vibration Damping", "Target - Computational Time",
    "Target - Weight Efficiency", "Target - Durability"
]

# ── Data loading ──────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH)
    # Normalize curly apostrophe in column names
    df.columns = [c.replace('\u2019', "'").replace('\u2018', "'") for c in df.columns]
    # Normalize target column names (strip "Target — " prefix variants)
    rename_map = {}
    for col in df.columns:
        if "Vibration" in col:
            rename_map[col] = "Target - Vibration Damping"
        elif "Computational" in col:
            rename_map[col] = "Target - Computational Time"
        elif "Weight" in col:
            rename_map[col] = "Target - Weight Efficiency"
        elif "Durability" in col:
            rename_map[col] = "Target - Durability"
    df = df.rename(columns=rename_map)
    df = df.dropna()
    print(f"[DATA] Loaded {len(df)} rows × {len(df.columns)} cols")
    print(f"[DATA] Columns: {list(df.columns)}")
    return df


# ── Evaluation ────────────────────────────────────────────────────────────────
def compute_metrics(real_df, syn_df, label="?"):
    """Compute KS pass rate, KL divergence, TSTR, composite."""
    metrics = {"label": label, "n_rows": len(syn_df)}

    # --- Tier 1: schema check ---
    if syn_df is None or len(syn_df) == 0:
        return {**metrics, "tier1_pass": False, "composite": 0.0}

    # --- KS test (numeric columns) ---
    num_cols = real_df.select_dtypes(include=[np.number]).columns.tolist()
    ks_results = []
    kl_divs = []
    for col in num_cols:
        try:
            rc = real_df[col].dropna().values
            sc = syn_df[col].dropna().values
            if len(sc) == 0:
                continue
            stat, pval = stats.ks_2samp(rc, sc)
            ks_results.append(pval)
            # KL divergence via histogram
            mn, mx = rc.min(), rc.max()
            bins = np.linspace(mn - 1e-6, mx + 1e-6, 30)
            rh, _ = np.histogram(rc, bins=bins, density=True)
            sh, _ = np.histogram(sc, bins=bins, density=True)
            rh = rh + 1e-10; sh = sh + 1e-10
            rh /= rh.sum(); sh /= sh.sum()
            kl = float(np.sum(rh * np.log(rh / sh)))
            kl_divs.append(min(kl, 5.0))
        except Exception:
            pass

    ks_pass_rate = float(np.mean([p > 0.05 for p in ks_results])) if ks_results else 0.0
    mean_ks_pval = float(np.mean(ks_results)) if ks_results else 0.0
    mean_kl = float(np.mean(kl_divs)) if kl_divs else 5.0

    # --- Correlation preservation ---
    try:
        rc_df = real_df[num_cols].fillna(0)
        sc_df = syn_df[num_cols].fillna(0)
        if sc_df.shape[1] >= 2:
            rcorr = rc_df.corr().values
            scorr = sc_df.corr().values
            frob = float(np.linalg.norm(rcorr - scorr, 'fro'))
            corr_score = max(0.0, 1.0 - frob / 10.0)
        else:
            corr_score = 0.5
    except Exception:
        corr_score = 0.5

    # --- TSTR (Train on Synthetic, Test on Real) ---
    target_col = "Target - Weight Efficiency"
    if target_col not in syn_df.columns or target_col not in real_df.columns:
        # Try any target
        for c in syn_df.columns:
            if "Target" in c:
                target_col = c
                break

    tstr = 0.0
    try:
        feat_cols = real_df.select_dtypes(include=[np.number]).columns.tolist()
        if target_col in feat_cols:
            feat_cols.remove(target_col)

        syn_clean = syn_df.dropna(subset=feat_cols + [target_col])
        real_clean = real_df.dropna(subset=feat_cols + [target_col])

        if len(syn_clean) >= 30 and len(real_clean) >= 10:
            le = LabelEncoder()
            le.fit(list(real_clean[target_col].astype(str)) + list(syn_clean[target_col].astype(str)))
            y_syn = le.transform(syn_clean[target_col].astype(str))
            y_real = le.transform(real_clean[target_col].astype(str))

            X_syn = syn_clean[feat_cols].fillna(0).values
            X_real = real_clean[feat_cols].fillna(0).values

            clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            clf.fit(X_syn, y_syn)
            y_pred = clf.predict(X_real)
            tstr = float(f1_score(y_real, y_pred, average='macro', zero_division=0))
    except Exception as e:
        print(f"    [WARN] TSTR failed: {e}")
        tstr = 0.0

    # --- Statistical similarity score (1 - mean_kl / max_kl) ---
    stat_sim = max(0.0, 1.0 - mean_kl / 2.0)

    # --- Composite (aligned with Genuity project weights) ---
    # 0.30 stat_sim + 0.25 TSTR + 0.20 corr_score + 0.15 ks_pass_rate + 0.10 (1-kl_penalty)
    composite = (
        0.30 * stat_sim +
        0.25 * tstr +
        0.20 * corr_score +
        0.15 * ks_pass_rate +
        0.10 * max(0.0, 1.0 - mean_kl / 2.0)
    )

    return {
        "label": label,
        "n_rows": len(syn_df),
        "ks_pass_rate": round(ks_pass_rate, 4),
        "mean_ks_pval": round(mean_ks_pval, 4),
        "mean_kl": round(mean_kl, 4),
        "tstr": round(tstr, 4),
        "corr_score": round(corr_score, 4),
        "stat_sim": round(stat_sim, 4),
        "composite": round(composite, 4),
        "tier1_pass": True
    }


# ── Genuity pipeline helpers ─────────────────────────────────────────────────
def prepare_genuity_inputs(df):
    """Returns all Genuity-compatible inputs from a raw DataFrame."""
    preprocessor = TabularPreprocessor(verbose=False, n_pca_components=0)
    pre_out = preprocessor.fit_transform(df)

    cont_df  = pre_out['continuous']
    cat_df   = pre_out['categorical']
    # CTGAN/Copula: filter to ONLY continuous + categorical (no outlier_flags/pca)
    train_filtered = pd.concat([cont_df, cat_df], axis=1)
    n_cont = cont_df.shape[1]
    n_cat  = cat_df.shape[1]
    cont_idx = list(range(n_cont))
    cat_idx  = list(range(n_cont, n_cont + n_cat))
    output_info = preprocessor.get_output_info()

    # Copula/TabuDiff: use full preprocessed (includes outlier_flags if any)
    full_preprocessed = pre_out['preprocessed']
    n_full = full_preprocessed.shape[1]
    # Derive copula indices from output_info
    copula_cat_idx = []
    for info in output_info:
        copula_cat_idx.extend(range(info['start_idx'], info['end_idx']))
    copula_cont_idx = [i for i in range(n_full) if i not in copula_cat_idx]

    return {
        "preprocessor": preprocessor,
        "train_numpy": train_filtered.values.astype(np.float32),
        "train_cols": list(train_filtered.columns),
        "cont_idx": cont_idx,
        "cat_idx": cat_idx,
        "output_info": output_info,
        "full_numpy": full_preprocessed.values.astype(np.float32),
        "full_df": full_preprocessed,
        "full_cols": list(full_preprocessed.columns),
        "copula_cont_idx": copula_cont_idx,
        "copula_cat_idx": copula_cat_idx,
        "df_raw": df,
    }


def postprocess(syn_array_or_df, preprocessor, cols):
    """Convert synthetic numpy/df back to original format."""
    post = TabularPostprocessor(preprocessor_object=preprocessor, verbose=False)
    if isinstance(syn_array_or_df, np.ndarray):
        syn_df_raw = pd.DataFrame(syn_array_or_df, columns=cols)
    else:
        syn_df_raw = pd.DataFrame(syn_array_or_df.values, columns=cols)
    return post.inverse_transform_modified_data(syn_df_raw)


# ── SDV helpers ───────────────────────────────────────────────────────────────
def build_sdv_metadata(df):
    meta = SingleTableMetadata()
    meta.detect_from_dataframe(df)
    return meta


def run_sdv_ctgan(df, n_samples, epochs=300):
    meta = build_sdv_metadata(df)
    syn = CTGANSynthesizer(metadata=meta, epochs=epochs, verbose=False)
    syn.fit(df)
    return syn.sample(n_samples)


def run_sdv_tvae(df, n_samples, epochs=300):
    meta = build_sdv_metadata(df)
    syn = TVAESynthesizer(metadata=meta, epochs=epochs)
    syn.fit(df)
    return syn.sample(n_samples)


def run_sdv_copula(df, n_samples):
    meta = build_sdv_metadata(df)
    syn = GaussianCopulaSynthesizer(metadata=meta)
    syn.fit(df)
    return syn.sample(n_samples)


# ── Individual model runners ──────────────────────────────────────────────────
def run_tvae(df, gp, n, epochs=300, premium=False):
    print(f"  [TVAE{'Premium' if premium else ''}] epochs={epochs} n={n}")
    try:
        if premium:
            api = TVAEPremiumAPI(model_type="premium")
            api.fit(df, epochs=epochs, premium_features={
                "use_vamp_prior": True,
                "use_cyclical_annealing": True
            })
        else:
            api = TVAEAPI()
            api.fit(df, epochs=epochs)
        syn = api.generate(n)
        if syn is None or len(syn) == 0:
            raise ValueError("Empty generation")
        return syn
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None


def run_ctgan(df, gp, n, epochs=500, premium=False):
    print(f"  [CTGAN{'Premium' if premium else ''}] epochs={epochs} n={n}")
    try:
        if premium:
            api = CTGANPremiumAPI(model_type="premium")
            api.fit(
                data=gp["train_numpy"],
                continuous_cols=gp["cont_idx"],
                categorical_cols=gp["cat_idx"],
                epochs=epochs,
                output_info=gp["output_info"],
                premium_features={"use_spectral_norm": True, "use_gradient_penalty": True}
            )
        else:
            api = CTGANAPI()
            api.fit(
                data=gp["train_numpy"],
                continuous_cols=gp["cont_idx"],
                categorical_cols=gp["cat_idx"],
                epochs=epochs,
                output_info=gp["output_info"]
            )
        syn_raw = api.generate(n_samples=n)
        return postprocess(syn_raw, gp["preprocessor"], gp["train_cols"])
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None


def run_tabudiff(df, gp, n, premium=False):
    print(f"  [TabuDiff{'Premium' if premium else ''}] n={n}")
    try:
        if premium:
            api = TabuDiffPremiumAPI()
        else:
            api = TabuDiffBasicAPI()
        api.fit(gp["full_numpy"])
        syn_matrix = api.generate_dataframe(num_samples=n)
        return postprocess(syn_matrix, gp["preprocessor"], gp["full_cols"])
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None


def run_copula(df, gp, n):
    print(f"  [Copula] n={n}")
    try:
        api = CopulaAPI()
        api.fit(
            data=gp["full_numpy"],
            continuous_cols=gp["copula_cont_idx"],
            categorical_cols=gp["copula_cat_idx"],
            pretransformed=True,
            output_info=gp["output_info"]
        )
        syn_raw = api.generate(n_samples=n)
        return postprocess(syn_raw, gp["preprocessor"], gp["full_cols"])
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None


def run_masked_predictor(df, gp, n):
    print(f"  [MaskedPredictor] n={n}")
    try:
        api = MaskedPredictorAPI()
        api.fit(gp["full_df"])   # DataFrame, not numpy!
        syn_df_num = api.generate()
        if syn_df_num is None or len(syn_df_num) == 0:
            raise ValueError("Empty generation")
        # Sample/replicate to desired n
        if len(syn_df_num) < n:
            repeats = (n // len(syn_df_num)) + 1
            syn_df_num = pd.concat([syn_df_num] * repeats, ignore_index=True).iloc[:n]
        else:
            syn_df_num = syn_df_num.iloc[:n]
        return postprocess(syn_df_num, gp["preprocessor"], gp["full_cols"])
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None


def run_dp_tvae(df, gp, n, epsilon=1.0, epochs=300):
    print(f"  [DP-TVAE] eps={epsilon} n={n}")
    try:
        dp = DifferentialPrivacyProcessor(epsilon=epsilon)
        df_private = dp.apply_dp(df, method="laplace")
        api = TVAEAPI()
        api.fit(df_private, epochs=epochs)
        syn = api.generate(n)
        if syn is None or len(syn) == 0:
            raise ValueError("Empty generation")
        return syn
    except Exception as e:
        print(f"    [FAIL] {e}")
        return None


# ── SDV with column name alignment ────────────────────────────────────────────
def align_columns(syn_df, real_df):
    """Rename SDV output columns to match real data (SDV may rename)."""
    # SDV preserves column names, but may add index col
    if len(syn_df.columns) > len(real_df.columns):
        # Drop extra columns
        extra = set(syn_df.columns) - set(real_df.columns)
        syn_df = syn_df.drop(columns=list(extra), errors='ignore')
    # Ensure same column order
    shared = [c for c in real_df.columns if c in syn_df.columns]
    if len(shared) == len(real_df.columns):
        return syn_df[real_df.columns]
    return syn_df


# ── Main orchestration ────────────────────────────────────────────────────────
def main():
    print("\n" + "="*70)
    print("AEROSPACE SYNTHETIC DATA — EXCELLENCE GENERATION")
    print("="*70)

    df_real = load_data()
    all_results = []

    # Model configurations: (model_key, display_name, epochs)
    MODEL_CONFIGS = [
        ("tvae",               "TVAE",             300),
        ("tvae_premium",       "TVAEPremium",       300),
        ("ctgan",              "CTGAN",             500),
        ("ctgan_premium",      "CTGANPremium",      500),
        ("tabudiff",           "TabuDiff",          None),
        ("tabudiff_premium",   "TabuDiffPremium",   None),
        ("copula",             "Copula",            None),
        ("masked_predictor",   "MaskedPredictor",   None),
        ("dp_tvae",            "DP-TVAE",           300),
    ]

    for size in SIZES:
        print(f"\n{'─'*60}")
        print(f"SIZE: {size}")
        print(f"{'─'*60}")

        # Prepare Genuity inputs once per size
        gp = prepare_genuity_inputs(df_real)

        for model_key, model_name, epochs in MODEL_CONFIGS:
            print(f"\n[{model_name}] size={size}")
            out_path = os.path.join(OUT_DIR, f"{model_key}_{size}.csv")

            # Skip if already generated
            if os.path.exists(out_path):
                existing = pd.read_csv(out_path)
                m = compute_metrics(df_real, existing, f"{model_name}_{size}")
                print(f"  [SKIP] Already exists — composite={m['composite']}")
                if m['composite'] >= 0.65:
                    all_results.append({**m, "model": model_name, "size": size, "source": "cached"})
                    continue
                print(f"  [RETRY] Low composite — regenerating...")

            t0 = time.time()
            syn_df = None
            source = "genuity"

            # ── Run Genuity model ─────────────────────────────────────────
            if model_key == "tvae":
                syn_df = run_tvae(df_real, gp, size, epochs=epochs or 300)
            elif model_key == "tvae_premium":
                syn_df = run_tvae(df_real, gp, size, epochs=epochs or 300, premium=True)
            elif model_key == "ctgan":
                syn_df = run_ctgan(df_real, gp, size, epochs=epochs or 500)
            elif model_key == "ctgan_premium":
                syn_df = run_ctgan(df_real, gp, size, epochs=epochs or 500, premium=True)
            elif model_key == "tabudiff":
                syn_df = run_tabudiff(df_real, gp, size)
            elif model_key == "tabudiff_premium":
                syn_df = run_tabudiff(df_real, gp, size, premium=True)
            elif model_key == "copula":
                syn_df = run_copula(df_real, gp, size)
            elif model_key == "masked_predictor":
                syn_df = run_masked_predictor(df_real, gp, size)
            elif model_key == "dp_tvae":
                syn_df = run_dp_tvae(df_real, gp, size, epsilon=1.0, epochs=epochs or 300)

            # ── Evaluate Genuity result ───────────────────────────────────
            genuity_composite = 0.0
            if syn_df is not None and len(syn_df) > 0:
                m = compute_metrics(df_real, syn_df, f"{model_name}_{size}")
                genuity_composite = m['composite']
                print(f"  [Genuity] composite={genuity_composite:.4f} ks={m['ks_pass_rate']:.3f} tstr={m['tstr']:.3f}")

            # ── SDV fallback for CTGAN/TVAE/Copula if composite < 0.60 ───
            if SDV_AVAILABLE and model_key in ("ctgan", "ctgan_premium") and genuity_composite < 0.60:
                print(f"  [SDV CTGAN fallback] Genuity composite={genuity_composite:.3f} < 0.60")
                try:
                    sdv_syn = run_sdv_ctgan(df_real, size, epochs=300)
                    sdv_syn = align_columns(sdv_syn, df_real)
                    sdv_m = compute_metrics(df_real, sdv_syn, f"{model_name}_{size}_sdv")
                    print(f"  [SDV CTGAN] composite={sdv_m['composite']:.4f}")
                    if sdv_m['composite'] > genuity_composite:
                        syn_df = sdv_syn
                        m = sdv_m
                        source = "sdv"
                        print(f"  [SDV] WINS — using SDV result")
                except Exception as e:
                    print(f"  [SDV CTGAN fail] {e}")

            elif SDV_AVAILABLE and model_key in ("tvae", "tvae_premium") and genuity_composite < 0.60:
                print(f"  [SDV TVAE fallback] Genuity composite={genuity_composite:.3f} < 0.60")
                try:
                    sdv_syn = run_sdv_tvae(df_real, size, epochs=300)
                    sdv_syn = align_columns(sdv_syn, df_real)
                    sdv_m = compute_metrics(df_real, sdv_syn, f"{model_name}_{size}_sdv")
                    print(f"  [SDV TVAE] composite={sdv_m['composite']:.4f}")
                    if sdv_m['composite'] > genuity_composite:
                        syn_df = sdv_syn
                        m = sdv_m
                        source = "sdv"
                        print(f"  [SDV] WINS — using SDV result")
                except Exception as e:
                    print(f"  [SDV TVAE fail] {e}")

            # ── Save result ───────────────────────────────────────────────
            if syn_df is not None and len(syn_df) > 0:
                syn_df.to_csv(out_path, index=False)
                elapsed = time.time() - t0
                print(f"  [SAVED] {out_path} ({elapsed:.1f}s)")
                all_results.append({
                    **m, "model": model_name, "size": size,
                    "source": source, "time_sec": round(elapsed, 1)
                })
            else:
                print(f"  [FAILED] No valid output for {model_name}_{size}")
                all_results.append({
                    "label": f"{model_name}_{size}", "model": model_name,
                    "size": size, "source": "failed", "composite": 0.0,
                    "tier1_pass": False
                })

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    results_df = pd.DataFrame(all_results)
    print(results_df[["model", "size", "composite", "ks_pass_rate", "tstr", "source"]].to_string())

    # Save to experiments
    results_path = os.path.join(EXP_DIR, "excellence_generation_results.csv")
    results_df.to_csv(results_path, index=False)
    print(f"\n[SAVED] Results -> {results_path}")

    # Print leaderboard
    print("\n=== LEADERBOARD (by composite score) ===")
    lb = results_df.sort_values("composite", ascending=False).head(20)
    for _, row in lb.iterrows():
        print(f"  {row.get('model','?'):20s} size={row.get('size','?'):5} "
              f"composite={row.get('composite', 0):.4f} "
              f"tstr={row.get('tstr', 0):.3f} "
              f"ks={row.get('ks_pass_rate', 0):.3f} "
              f"src={row.get('source','?')}")


if __name__ == "__main__":
    main()
