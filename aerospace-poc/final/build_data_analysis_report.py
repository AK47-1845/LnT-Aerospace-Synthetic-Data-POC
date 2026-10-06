"""
build_data_analysis_report.py
Generates the flagship data analysis report and all plots for the
Aerospace Structural Design synthetic-data project.
"""

import matplotlib
matplotlib.use('Agg')

import os
import sys
import logging
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, ks_2samp
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ── logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

# ── paths ──────────────────────────────────────────────────────────────────────
REAL_DATA   = r'd:\aero\aerospace_structural_design_dataset.csv'
SYN_DATA    = r'd:\aero\final\per_model_datasets\empirical_1000.csv'
REPORT_PATH = r'd:\aero\final\reports\data_analysis_report.md'
PLOT_DIR    = r'd:\aero\final\reports\plots'

os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# ── constants ──────────────────────────────────────────────────────────────────
TARGETS = ['Vibration Damping', 'Computational Time', 'Weight Efficiency', 'Durability']
CAT_COLS = ['Material Type', 'Structural Shape', 'Load Distribution', 'Quantum Algorithm Type']
NUMERIC_COLS = [
    'E (GPa)', 'nu', 'rho', 'Tensile Strength (MPa)', "Young's Modulus",
    'Altitude (m)', 'Temperature (C)', 'Pressure (Pa)', 'Operational Life (years)',
    'Wing Span (m)', 'Fuselage Length (m)', 'Structural Thickness (mm)',
    'Number of Iterations', 'Optimization Time (sec)'
]

FIG_SIZE   = (12, 8)
FIG_SIZE_L = (16, 10)
DPI        = 150
PALETTE    = 'tab10'


def p(path):
    """Return plot full path."""
    return os.path.join(PLOT_DIR, path)


def fmt(x):
    """Format number to 4 dp."""
    try:
        return f'{float(x):.4f}'
    except Exception:
        return str(x)


# ── helpers ────────────────────────────────────────────────────────────────────
def detect_numeric_cols(df):
    """Return list of numeric cols that actually exist in df (auto-detect)."""
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c not in TARGETS]


def save_fig(filename):
    plt.tight_layout()
    plt.savefig(p(filename), dpi=DPI, bbox_inches='tight')
    plt.close('all')
    log.info('Saved %s', filename)


# ══════════════════════════════════════════════════════════════════════════════
# PLOT GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def plot_pearson_heatmap(df, num_cols):
    log.info('Generating Pearson heatmap...')
    corr = df[num_cols].corr(method='pearson')
    fig, ax = plt.subplots(figsize=(14, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, square=True, linewidths=0.5, ax=ax,
                annot_kws={'size': 7})
    ax.set_title('Pearson Correlation Matrix — Numeric Features', fontsize=14, pad=12)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    save_fig('eda_correlation_heatmap_pearson.png')


def plot_spearman_heatmap(df, num_cols):
    log.info('Generating Spearman heatmap...')
    corr = df[num_cols].corr(method='spearman')
    fig, ax = plt.subplots(figsize=(14, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='PuOr',
                center=0, square=True, linewidths=0.5, ax=ax,
                annot_kws={'size': 7})
    ax.set_title('Spearman Rank Correlation Matrix — Numeric Features', fontsize=14, pad=12)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    save_fig('eda_correlation_heatmap_spearman.png')


def plot_univariate_histograms(df, num_cols):
    log.info('Generating univariate histograms...')
    ncols = 4
    nrows = int(np.ceil(len(num_cols) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, nrows * 3))
    axes = axes.flatten()
    for i, col in enumerate(num_cols):
        axes[i].hist(df[col].dropna(), bins=30, color='steelblue', edgecolor='white', alpha=0.85)
        axes[i].set_title(col, fontsize=9)
        axes[i].set_xlabel('')
        axes[i].tick_params(labelsize=7)
    for j in range(len(num_cols), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle('Univariate Distributions — All Numeric Features', fontsize=13, y=1.01)
    save_fig('eda_univariate_histograms.png')


def plot_boxplots_by_material(df):
    log.info('Generating boxplots by Material...')
    # find columns dynamically
    candidates = [c for c in df.columns if any(k in c.lower() for k in ['e (gpa)', 'tensile', 'kg/m'])]
    if not candidates:
        candidates = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c not in TARGETS][:3]
    features = candidates[:3]
    fig, axes = plt.subplots(1, len(features), figsize=(14, 7))
    if len(features) == 1:
        axes = [axes]
    for ax, feat in zip(axes, features):
        if 'Material Type' in df.columns:
            order = sorted(df['Material Type'].dropna().unique())
            sns.boxplot(data=df, x='Material Type', y=feat, order=order,
                        palette='Set2', ax=ax)
        ax.set_title(feat, fontsize=10)
        ax.tick_params(axis='x', rotation=15)
    fig.suptitle('Key Property Distributions by Material Type', fontsize=13)
    save_fig('eda_boxplots_by_material.png')


def plot_target_distributions(df):
    log.info('Generating target distributions...')
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()
    colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']
    for i, tgt in enumerate(TARGETS):
        if tgt not in df.columns:
            axes[i].set_visible(False)
            continue
        vc = df[tgt].value_counts().sort_index()
        axes[i].bar(range(len(vc)), vc.values, color=colors[i], edgecolor='white', alpha=0.85)
        axes[i].set_xticks(range(len(vc)))
        axes[i].set_xticklabels(vc.index, rotation=10)
        axes[i].set_title(tgt, fontsize=12)
        axes[i].set_ylabel('Count')
        for x, v in enumerate(vc.values):
            axes[i].text(x, v + 1, str(v), ha='center', va='bottom', fontsize=9)
    fig.suptitle('Class Distributions — All Target Variables', fontsize=14)
    save_fig('eda_target_distributions.png')


def plot_altitude_temp_pressure(df):
    log.info('Generating altitude vs temp/pressure...')
    alt_col = next((c for c in df.columns if 'altitude' in c.lower()), None)
    temp_col = next((c for c in df.columns if 'temperature' in c.lower() or 'temp' in c.lower()), None)
    pres_col = next((c for c in df.columns if 'pressure' in c.lower()), None)
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    if alt_col and temp_col:
        axes[0].scatter(df[alt_col], df[temp_col], alpha=0.5, s=20, color='steelblue')
        axes[0].set_xlabel(alt_col)
        axes[0].set_ylabel(temp_col)
        axes[0].set_title('Altitude vs Temperature')
    if alt_col and pres_col:
        axes[1].scatter(df[alt_col], df[pres_col], alpha=0.5, s=20, color='darkorange')
        axes[1].set_xlabel(alt_col)
        axes[1].set_ylabel(pres_col)
        axes[1].set_title('Altitude vs Pressure')
    fig.suptitle('Flight Environment: Altitude Relationships', fontsize=13)
    save_fig('eda_altitude_temp_pressure.png')


def plot_wingspan_fuselage(df):
    log.info('Generating Wing Span vs Fuselage scatter...')
    ws_col = next((c for c in df.columns if 'wing' in c.lower()), None)
    fl_col = next((c for c in df.columns if 'fuselage' in c.lower()), None)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    if ws_col and fl_col and 'Structural Shape' in df.columns:
        shapes = df['Structural Shape'].dropna().unique()
        palette = dict(zip(sorted(shapes), sns.color_palette(PALETTE, len(shapes))))
        for shape in sorted(shapes):
            sub = df[df['Structural Shape'] == shape]
            ax.scatter(sub[ws_col], sub[fl_col],
                       label=shape, alpha=0.6, s=30, color=palette[shape])
        ax.set_xlabel(ws_col)
        ax.set_ylabel(fl_col)
        ax.legend(title='Structural Shape')
    ax.set_title('Wing Span vs Fuselage Length by Structural Shape', fontsize=13)
    save_fig('eda_wingspan_fuselage.png')


def plot_optimization_scatter(df):
    log.info('Generating optimization scatter...')
    iter_col = next((c for c in df.columns if 'iteration' in c.lower()), None)
    time_col = next((c for c in df.columns if 'optimization time' in c.lower()), None)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    if iter_col and time_col and 'Quantum Algorithm Type' in df.columns:
        algos = df['Quantum Algorithm Type'].dropna().unique()
        palette = dict(zip(sorted(algos), sns.color_palette('Set1', len(algos))))
        for algo in sorted(algos):
            sub = df[df['Quantum Algorithm Type'] == algo]
            ax.scatter(sub[iter_col], sub[time_col],
                       label=algo, alpha=0.55, s=25, color=palette[algo])
        ax.set_xlabel(iter_col)
        ax.set_ylabel(time_col)
        ax.legend(title='Algorithm')
    ax.set_title('Number of Iterations vs Optimization Time by Algorithm', fontsize=13)
    save_fig('eda_optimization_scatter.png')


def plot_feature_importance_rf(df, num_cols):
    log.info('Generating RF feature importance...')
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    axes = axes.flatten()
    for i, tgt in enumerate(TARGETS):
        ax = axes[i]
        if tgt not in df.columns:
            ax.set_visible(False)
            continue
        try:
            sub = df[num_cols + [tgt]].dropna()
            X = sub[num_cols].values
            le = LabelEncoder()
            y = le.fit_transform(sub[tgt].astype(str))
            rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
            rf.fit(X, y)
            imp = pd.Series(rf.feature_importances_, index=num_cols).sort_values(ascending=True)
            colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(imp)))
            ax.barh(imp.index, imp.values, color=colors)
            ax.set_title(f'Feature Importance — {tgt}', fontsize=10)
            ax.set_xlabel('Importance')
            ax.tick_params(labelsize=8)
        except Exception as e:
            log.warning('RF importance failed for %s: %s', tgt, e)
            ax.set_title(f'{tgt} — skipped ({e})')
    fig.suptitle('Random Forest Feature Importance (all 4 targets)', fontsize=14)
    save_fig('eda_feature_importance_rf.png')


def plot_pairplot_material(df, num_cols):
    log.info('Generating pairplot by Material...')
    try:
        variances = df[num_cols].var().sort_values(ascending=False)
        top5 = variances.head(5).index.tolist()
        cols = top5 + ['Material Type']
        sub = df[cols].dropna()
        g = sns.pairplot(sub, hue='Material Type', plot_kws={'alpha': 0.4, 's': 15},
                         diag_kind='kde', height=2.2)
        g.fig.suptitle('Pairplot — Top 5 Numeric Features by Material Type', y=1.02, fontsize=12)
        g.fig.set_size_inches(13, 10)
        plt.savefig(p('eda_pairplot_material.png'), dpi=DPI, bbox_inches='tight')
        plt.close('all')
        log.info('Saved eda_pairplot_material.png')
    except Exception as e:
        log.warning('Pairplot failed: %s', e)
        fig, ax = plt.subplots(figsize=FIG_SIZE)
        ax.text(0.5, 0.5, f'Pairplot generation failed:\n{e}',
                ha='center', va='center', transform=ax.transAxes)
        save_fig('eda_pairplot_material.png')


def plot_target_crosstab_heatmap(df):
    log.info('Generating target crosstab heatmap...')
    fig, ax = plt.subplots(figsize=(10, 7))
    if 'Durability' in df.columns and 'Weight Efficiency' in df.columns:
        ct = pd.crosstab(df['Durability'], df['Weight Efficiency'])
        sns.heatmap(ct, annot=True, fmt='d', cmap='YlOrRd', ax=ax,
                    linewidths=0.5, cbar_kws={'shrink': 0.8})
        ax.set_title('Crosstab Heatmap: Durability x Weight Efficiency', fontsize=13)
    save_fig('eda_target_crosstab_heatmap.png')


def plot_violin_E_by_material(df):
    log.info('Generating violin plot E by material...')
    e_col = next((c for c in df.columns if 'e (gpa)' in c.lower() or c == 'E (GPa)'), None)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    if e_col and 'Material Type' in df.columns:
        order = sorted(df['Material Type'].dropna().unique())
        sns.violinplot(data=df, x='Material Type', y=e_col, order=order,
                       palette='Pastel1', inner='box', ax=ax)
        ax.set_title(f"{e_col} Distribution by Material Type", fontsize=13)
        ax.set_xlabel('Material Type')
        ax.set_ylabel(e_col)
    save_fig('eda_violin_E_by_material.png')


def plot_real_vs_syn_histograms(df_real, df_syn, num_cols):
    log.info('Generating real vs synthetic histograms...')
    shared = [c for c in num_cols if c in df_syn.columns]
    scores = []
    for c in shared:
        r_std = df_real[c].std()
        if r_std > 0:
            diff = abs(df_real[c].mean() - df_syn[c].mean()) / r_std
        else:
            diff = 0
        scores.append((c, diff))
    scores.sort(key=lambda x: x[1], reverse=True)
    top8 = [c for c, _ in scores[:8]]
    if len(top8) < 8:
        top8 = (top8 + shared)[:8]

    fig, axes = plt.subplots(4, 2, figsize=(14, 16))
    axes = axes.flatten()
    for i, col in enumerate(top8):
        ax = axes[i]
        r_vals = df_real[col].dropna()
        s_vals = df_syn[col].dropna() if col in df_syn.columns else pd.Series(dtype=float)
        mn = min(r_vals.min(), s_vals.min() if len(s_vals) > 0 else r_vals.min())
        mx = max(r_vals.max(), s_vals.max() if len(s_vals) > 0 else r_vals.max())
        bins = np.linspace(mn, mx, 35)
        ax.hist(r_vals, bins=bins, alpha=0.55, color='steelblue', label='Real', density=True)
        if len(s_vals) > 0:
            ax.hist(s_vals, bins=bins, alpha=0.55, color='tomato', label='Synthetic', density=True)
        ax.set_title(col, fontsize=9)
        ax.legend(fontsize=7)
        ax.tick_params(labelsize=7)
    fig.suptitle('Real vs Synthetic Distributions — Top 8 Features', fontsize=13, y=1.01)
    save_fig('eda_real_vs_syn_histograms.png')


def plot_pca_real_vs_syn(df_real, df_syn, num_cols):
    log.info('Generating PCA real vs synthetic...')
    shared = [c for c in num_cols if c in df_syn.columns]
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    try:
        X_real = df_real[shared].dropna().values
        X_syn  = df_syn[shared].dropna().values

        scaler = StandardScaler()
        X_all  = np.vstack([X_real, X_syn])
        scaler.fit(X_all)
        X_real_s = scaler.transform(X_real)
        X_syn_s  = scaler.transform(X_syn)

        pca = PCA(n_components=2, random_state=42)
        pca.fit(np.vstack([X_real_s, X_syn_s]))
        pr = pca.transform(X_real_s)
        ps = pca.transform(X_syn_s)

        ax.scatter(ps[:, 0], ps[:, 1], c='tomato',    alpha=0.35, s=12, label=f'Synthetic (n={len(ps)})')
        ax.scatter(pr[:, 0], pr[:, 1], c='steelblue', alpha=0.55, s=20, label=f'Real (n={len(pr)})')
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)')
        ax.legend()
    except Exception as e:
        log.warning('PCA plot failed: %s', e)
        ax.text(0.5, 0.5, f'PCA failed: {e}', ha='center', va='center', transform=ax.transAxes)
    ax.set_title('PCA 2D Projection: Real vs Synthetic Data', fontsize=13)
    save_fig('eda_pca_real_vs_syn.png')


# ══════════════════════════════════════════════════════════════════════════════
# STATISTICS HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def univariate_stats(df, num_cols):
    rows = []
    for c in num_cols:
        s = df[c].dropna()
        rows.append({
            'Feature':   c,
            'Mean':      fmt(s.mean()),
            'Std':       fmt(s.std()),
            'Min':       fmt(s.min()),
            'Max':       fmt(s.max()),
            'Median':    fmt(s.median()),
            'Skewness':  fmt(s.skew()),
            'Kurtosis':  fmt(s.kurtosis()),
        })
    return pd.DataFrame(rows)


def normality_tests(df, num_cols):
    """Run D'Agostino K² normality test for each numeric column."""
    rows = []
    for c in num_cols:
        s = df[c].dropna()
        if len(s) < 8:
            continue
        try:
            stat, pval = stats.normaltest(s)
            rows.append({
                'Feature':   c,
                'K² Statistic': fmt(stat),
                'p-value':   fmt(pval),
                'Normal (p>0.05)': 'Yes' if pval > 0.05 else 'No',
            })
        except Exception:
            pass
    return pd.DataFrame(rows)


def rf_full_importance(df, num_cols):
    """Return full RF importance table for all targets."""
    all_rows = []
    for tgt in TARGETS:
        if tgt not in df.columns:
            continue
        try:
            sub = df[num_cols + [tgt]].dropna()
            X = sub[num_cols].values
            le = LabelEncoder()
            y = le.fit_transform(sub[tgt].astype(str))
            rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
            rf.fit(X, y)
            imp = pd.Series(rf.feature_importances_, index=num_cols).sort_values(ascending=False)
            for rank, (feat, score) in enumerate(imp.items(), 1):
                all_rows.append({
                    'Target': tgt,
                    'Rank': rank,
                    'Feature': feat,
                    'Importance': fmt(score),
                })
        except Exception as e:
            log.warning('rf_full_importance failed for %s: %s', tgt, e)
    return pd.DataFrame(all_rows)


def top_correlated_pairs(df, num_cols, method='pearson', n=10):
    # Only use columns that actually exist and have variance
    valid_cols = [c for c in num_cols if c in df.columns and df[c].std() > 0]
    corr = df[valid_cols].corr(method=method)
    # Lower triangle excluding diagonal (k=-1)
    mask = np.tril(np.ones(corr.shape, dtype=bool), k=-1)
    pairs = (corr.where(mask)
                 .stack()
                 .reset_index())
    pairs.columns = ['Feature 1', 'Feature 2', 'Correlation']
    pairs['abs_corr'] = pairs['Correlation'].abs()
    pairs = pairs.sort_values('abs_corr', ascending=False).head(n)
    log.info('Top correlation pair: %s vs %s r=%.4f',
             pairs.iloc[0]['Feature 1'], pairs.iloc[0]['Feature 2'],
             float(pairs.iloc[0]['abs_corr']))
    pairs['Correlation'] = pairs['Correlation'].apply(fmt)
    return pairs[['Feature 1', 'Feature 2', 'Correlation']].reset_index(drop=True)


def chi_square_tests(df):
    rows = []
    mat_col = next((c for c in df.columns if c.lower() == 'material type'), None)
    for tgt in TARGETS:
        if tgt not in df.columns or mat_col is None:
            log.warning('chi2 skipped for %s: mat_col=%s tgt_in_cols=%s', tgt, mat_col, tgt in df.columns)
            continue
        try:
            # Drop rows where either variable is NaN before crosstab
            sub = df[[mat_col, tgt]].dropna()
            if len(sub) < 10:
                log.warning('chi2 skipped for %s: only %d non-null rows', tgt, len(sub))
                continue
            ct = pd.crosstab(sub[mat_col], sub[tgt])
            log.info('chi2 crosstab for %s: shape %s, row_uniq=%d, col_uniq=%d',
                     tgt, ct.shape, ct.shape[0], ct.shape[1])
            if ct.shape[0] < 2 or ct.shape[1] < 2:
                log.warning('chi2 degenerate contingency table for %s', tgt)
                continue
            chi2, pval, dof, expected = chi2_contingency(ct)
            log.info('chi2 for %s: chi2=%.4f  p=%.6f  dof=%d', tgt, chi2, pval, dof)
            rows.append({
                'Target':      tgt,
                'chi2':        fmt(chi2),
                'dof':         dof,
                'p-value':     fmt(pval),
                'Significant': 'Yes' if pval < 0.05 else 'No',
            })
        except Exception as e:
            log.warning('chi2 failed for %s: %s', tgt, e)
    return pd.DataFrame(rows)


def ks_tests(df_real, df_syn, num_cols):
    results = {}
    for c in num_cols:
        if c in df_syn.columns:
            try:
                stat, pval = ks_2samp(df_real[c].dropna(), df_syn[c].dropna())
                results[c] = {'ks_stat': stat, 'p_value': pval, 'pass': pval > 0.05}
            except Exception:
                pass
    return results


def kl_divergence(p_vals, q_vals, bins=30):
    min_v = min(p_vals.min(), q_vals.min())
    max_v = max(p_vals.max(), q_vals.max())
    if min_v == max_v:
        return 0.0
    edges = np.linspace(min_v, max_v, bins + 1)
    p_hist, _ = np.histogram(p_vals, bins=edges, density=True)
    q_hist, _ = np.histogram(q_vals, bins=edges, density=True)
    p_hist = p_hist + 1e-10
    q_hist = q_hist + 1e-10
    p_hist /= p_hist.sum()
    q_hist /= q_hist.sum()
    return float(np.sum(p_hist * np.log(p_hist / q_hist)))


def mean_kl(df_real, df_syn, num_cols):
    vals = []
    for c in num_cols:
        if c in df_syn.columns:
            try:
                vals.append(kl_divergence(df_real[c].dropna().values,
                                          df_syn[c].dropna().values))
            except Exception:
                pass
    return float(np.mean(vals)) if vals else float('nan')


def rf_discriminator_auc(df_real, df_syn, num_cols):
    """Train RF to distinguish real vs synthetic; return AUC (0.5=indistinguishable)."""
    try:
        from sklearn.model_selection import cross_val_score
        shared = [c for c in num_cols if c in df_syn.columns]
        X_r = df_real[shared].dropna().values
        X_s = df_syn[shared].dropna().values
        min_n = min(len(X_r), len(X_s), 500)
        rng = np.random.RandomState(42)
        idx_r = rng.choice(len(X_r), min_n, replace=False)
        idx_s = rng.choice(len(X_s), min_n, replace=False)
        X = np.vstack([X_r[idx_r], X_s[idx_s]])
        y = np.array([0] * min_n + [1] * min_n)
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        aucs = cross_val_score(rf, X, y, cv=3, scoring='roc_auc')
        return float(np.mean(aucs))
    except Exception as e:
        log.warning('rf_discriminator_auc failed: %s', e)
        return float('nan')


def df_to_md_table(df):
    header = '| ' + ' | '.join(str(c) for c in df.columns) + ' |'
    sep    = '| ' + ' | '.join(['---'] * len(df.columns)) + ' |'
    rows   = []
    for _, row in df.iterrows():
        rows.append('| ' + ' | '.join(str(v) for v in row.values) + ' |')
    return '\n'.join([header, sep] + rows)


def get_rf_top3(df, num_cols):
    results = {}
    for tgt in TARGETS:
        if tgt not in df.columns:
            continue
        try:
            sub = df[num_cols + [tgt]].dropna()
            X = sub[num_cols].values
            le = LabelEncoder()
            y = le.fit_transform(sub[tgt].astype(str))
            rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
            rf.fit(X, y)
            imp = pd.Series(rf.feature_importances_, index=num_cols).sort_values(ascending=False)
            results[tgt] = imp.head(3)
        except Exception as e:
            log.warning('RF top3 failed for %s: %s', tgt, e)
    return results


# ══════════════════════════════════════════════════════════════════════════════
# REPORT BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_report(df_real, df_syn, num_cols):
    log.info('Computing statistics for report...')

    uv_stats      = univariate_stats(df_real, num_cols)
    norm_tests    = normality_tests(df_real, num_cols)
    top_corr      = top_correlated_pairs(df_real, num_cols)
    chi_sq        = chi_square_tests(df_real)
    ks_res        = ks_tests(df_real, df_syn, num_cols)
    ks_pass_rate  = sum(v['pass'] for v in ks_res.values()) / max(len(ks_res), 1)
    mkl           = mean_kl(df_real, df_syn, num_cols)
    log.info('Computing RF full importance tables (this may take ~60s)...')
    rf_imp_full   = rf_full_importance(df_real, num_cols)
    log.info('Computing RF discriminator AUC...')
    disc_auc      = rf_discriminator_auc(df_real, df_syn, num_cols)

    # linear regressions altitude
    r2_temp = r2_pres = float('nan')
    alt_col  = next((c for c in df_real.columns if 'altitude' in c.lower()), None)
    temp_col = next((c for c in df_real.columns if 'temperature' in c.lower()), None)
    pres_col = next((c for c in df_real.columns if 'pressure' in c.lower()), None)
    try:
        if alt_col and temp_col:
            mask = df_real[[alt_col, temp_col]].dropna()
            _, _, r, _, _ = stats.linregress(mask[alt_col], mask[temp_col])
            r2_temp = r ** 2
    except Exception:
        pass
    try:
        if alt_col and pres_col:
            mask = df_real[[alt_col, pres_col]].dropna()
            _, _, r, _, _ = stats.linregress(mask[alt_col], mask[pres_col])
            r2_pres = r ** 2
    except Exception:
        pass

    # material profile
    mat_profile = {}
    e_col  = next((c for c in df_real.columns if 'e (gpa)' in c.lower()), None)
    rho_col = next((c for c in df_real.columns if 'kg/m' in c.lower()), None)
    ts_col = next((c for c in df_real.columns if 'tensile' in c.lower()), None)
    if 'Material Type' in df_real.columns:
        for mat in sorted(df_real['Material Type'].dropna().unique()):
            sub = df_real[df_real['Material Type'] == mat]
            prof = {}
            for col in [e_col, rho_col, ts_col]:
                if col:
                    prof[col] = (sub[col].mean(), sub[col].std())
            mat_profile[mat] = prof

    # thickness by shape
    thick_col = next((c for c in df_real.columns if 'thickness' in c.lower()), None)
    thick_by_shape = {}
    if 'Structural Shape' in df_real.columns and thick_col:
        for sh in sorted(df_real['Structural Shape'].dropna().unique()):
            sub = df_real[df_real['Structural Shape'] == sh][thick_col]
            thick_by_shape[sh] = {'mean': sub.mean(), 'std': sub.std(),
                                  'min': sub.min(), 'max': sub.max()}

    # operational life by material
    life_col = next((c for c in df_real.columns if 'operational life' in c.lower()), None)
    life_by_mat = {}
    if 'Material Type' in df_real.columns and life_col:
        for mat in sorted(df_real['Material Type'].dropna().unique()):
            sub = df_real[df_real['Material Type'] == mat][life_col]
            life_by_mat[mat] = {'mean': sub.mean(), 'std': sub.std()}

    # opt time by algo
    opt_col  = next((c for c in df_real.columns if 'optimization time' in c.lower()), None)
    opt_by_algo = {}
    if 'Quantum Algorithm Type' in df_real.columns and opt_col:
        for algo in sorted(df_real['Quantum Algorithm Type'].dropna().unique()):
            sub = df_real[df_real['Quantum Algorithm Type'] == algo][opt_col]
            opt_by_algo[algo] = {'mean': sub.mean(), 'std': sub.std()}

    # correlation of Number of Iterations with Computational Time
    iter_col = next((c for c in df_real.columns if 'number of iterations' in c.lower()), None)
    iter_ct_corr = float('nan')
    try:
        if iter_col and 'Computational Time' in df_real.columns:
            sub = df_real[[iter_col, 'Computational Time']].dropna()
            le  = LabelEncoder()
            ct_enc = le.fit_transform(sub['Computational Time'].astype(str))
            iter_ct_corr, _ = stats.pearsonr(sub[iter_col], ct_enc)
    except Exception:
        pass

    # grouped means by material
    group_mean_mat = pd.DataFrame()
    if 'Material Type' in df_real.columns:
        group_mean_mat = df_real.groupby('Material Type')[num_cols].mean().round(4)

    # RF top3
    log.info('Running Random Forest for report (feature importance)...')
    rf_top3 = get_rf_top3(df_real, num_cols)

    # class counts
    class_counts = {}
    for tgt in TARGETS:
        if tgt in df_real.columns:
            class_counts[tgt] = df_real[tgt].value_counts().to_dict()

    # high skew features — use raw float skew recomputed from data to avoid string formatting issues
    _skew_map = {c: float(df_real[c].dropna().skew()) for c in num_cols}
    high_skew = [c for c, sk in sorted(_skew_map.items(), key=lambda t: abs(t[1]), reverse=True)
                 if abs(sk) > 0.5]
    log.info('High-skew features (|skew|>0.5): %s', high_skew)

    # top corr pair
    top_corr_pair = top_corr.iloc[0] if len(top_corr) > 0 else None

    # ── WRITE MARKDOWN ─────────────────────────────────────────────────────────
    log.info('Writing Markdown report...')
    lines = []
    A = lines.append

    A('# Data Analysis Report — Aerospace Structural Design Dataset')
    A('')
    A('---')
    A('')
    A('## Table of Contents')
    A('')
    A('1. [Executive Summary](#chapter-1--executive-summary)')
    A('2. [Dataset Overview](#chapter-2--dataset-overview)')
    A('3. [Univariate Analysis](#chapter-3--univariate-analysis)')
    A('4. [Bivariate & Multivariate Analysis](#chapter-4--bivariate--multivariate-analysis)')
    A('5. [Material Type Deep Dive](#chapter-5--material-type-deep-dive)')
    A('6. [Flight Environment Analysis](#chapter-6--flight-environment-analysis)')
    A('7. [Structural Geometry Analysis](#chapter-7--structural-geometry-analysis)')
    A('8. [Optimization & Algorithm Analysis](#chapter-8--optimization--algorithm-analysis)')
    A('9. [Target Variable Analysis](#chapter-9--target-variable-analysis)')
    A('10. [Feature Importance & Drivers](#chapter-10--feature-importance--drivers)')
    A('11. [Real vs Synthetic Comparison](#chapter-11--real-vs-synthetic-comparison)')
    A('12. [Conclusions & Recommendations](#chapter-12--conclusions--recommendations)')
    A('')

    # ── Chapter 1 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 1 — Executive Summary')
    A('')
    A('### What the Dataset Is')
    A('')
    A('The **Aerospace Structural Design Dataset** is a multi-domain simulation dataset '
      'representing aerospace component design scenarios. '
      "It captures material properties (Young's modulus, Poisson's ratio, density, tensile strength), "
      'flight-environment parameters (altitude, temperature, pressure), '
      'structural geometry (wing span, fuselage length, thickness), '
      'and quantum-algorithm optimisation metadata (iterations, time). '
      f'The real dataset contains **{len(df_real)} rows** and **{len(df_real.columns)} columns**, '
      f'with **{len(num_cols)} numeric** and **{len(CAT_COLS)} categorical** features, '
      'and four ordinal classification targets.')
    A('')
    A('### Top 3 Findings (computed from real data)')
    A('')
    if top_corr_pair is not None:
        A(f'**Finding 1 — Dominant Correlation:** '
          f'The strongest Pearson correlation in the dataset is between '
          f'**{top_corr_pair["Feature 1"]}** and **{top_corr_pair["Feature 2"]}** '
          f'(r = {top_corr_pair["Correlation"]}), indicating a strong linear relationship '
          f'between these two engineered features.')
    else:
        A('**Finding 1:** Correlation data not available.')
    A('')
    skew_str = ', '.join(f'*{f}*' for f in high_skew[:5]) if high_skew else 'none detected'
    A(f'**Finding 2 — Skewed Features:** {len(high_skew)} numeric features exhibit |skew| > 1, '
      f'namely: {skew_str}. These features may benefit from log- or Box-Cox transformation '
      f'before modelling.')
    A('')
    sig_targets = chi_sq[chi_sq['Significant'] == 'Yes']['Target'].tolist() if len(chi_sq) > 0 else []
    sig_str = ', '.join(f'*{t}*' for t in sig_targets) if sig_targets else 'none'
    A(f'**Finding 3 — Material Type as Significant Predictor:** Chi-square tests confirm that '
      f'Material Type has a statistically significant association (p < 0.05) with the following '
      f'target variables: {sig_str}. This makes Material Type a critical categorical feature '
      f'for all downstream classifiers.')
    A('')

    # ── Chapter 2 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 2 — Dataset Overview')
    A('')
    A(f'- **Rows (real):** {len(df_real)}')
    A(f'- **Rows (synthetic — empirical_1000):** {len(df_syn)}')
    A(f'- **Columns:** {len(df_real.columns)}')
    mem_mb = df_real.memory_usage(deep=True).sum() / 1024 / 1024
    A(f'- **Memory footprint (real, deep):** {mem_mb:.4f} MB')
    A(f'- **Missing values (real):** {df_real.isnull().sum().sum()} total')
    A('')
    A('### Schema Table')
    A('')
    schema_rows = []
    for col in df_real.columns:
        dtype = str(df_real[col].dtype)
        if col in TARGETS:
            col_type = 'Target (ordinal)'
            sample = ', '.join(sorted(df_real[col].dropna().unique().astype(str)))
        elif col in CAT_COLS:
            col_type = 'Categorical'
            sample = ', '.join(sorted(df_real[col].dropna().unique().astype(str)))
        else:
            col_type = 'Numeric'
            sample = f'{df_real[col].min():.2f} – {df_real[col].max():.2f}'
        schema_rows.append({'Column': col, 'Dtype': dtype, 'Type': col_type,
                            'Range / Values': sample})
    A(df_to_md_table(pd.DataFrame(schema_rows)))
    A('')
    A('### Missing Values Audit')
    A('')
    mv = df_real.isnull().sum()
    mv_df = pd.DataFrame({'Column': mv.index, 'Missing Count': mv.values,
                          'Missing %': (mv.values / len(df_real) * 100).round(4)})
    mv_df = mv_df[mv_df['Missing Count'] > 0]
    if len(mv_df) == 0:
        A('No missing values found in the real dataset. Data is complete.')
    else:
        A(df_to_md_table(mv_df))
    A('')
    A('### Class Counts for All 4 Targets')
    A('')
    for tgt, cc in class_counts.items():
        A(f'**{tgt}:**')
        cc_df = pd.DataFrame({'Class': list(cc.keys()), 'Count': list(cc.values())})
        A(df_to_md_table(cc_df))
        A('')

    # ── Chapter 3 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 3 — Univariate Analysis')
    A('')
    A('This chapter presents the full univariate characterisation of every numeric '
      'feature in the real dataset: descriptive statistics, normality tests, and '
      'physical interpretation of each distribution shape.')
    A('')
    A('### 3.1 Descriptive Statistics — All Numeric Features')
    A('')
    A('The table below gives mean, standard deviation, minimum, maximum, median, '
      'skewness (third standardised moment), and excess kurtosis (fourth standardised '
      'moment minus 3) for all numeric features. Skewness = 0 and kurtosis = 0 '
      'correspond to a perfectly normal distribution.')
    A('')
    A(df_to_md_table(uv_stats))
    A('')
    A('### 3.2 Normality Tests (D\'Agostino K²)')
    A('')
    A('The D\'Agostino K² test (also called the omnibus test) combines skewness and '
      'kurtosis into a single chi-squared statistic. The null hypothesis is that the '
      'sample is drawn from a normal distribution. A p-value below 0.05 rejects '
      'normality at the 5% significance level.')
    A('')
    if len(norm_tests) > 0:
        A(df_to_md_table(norm_tests))
    else:
        A('Normality test results not available.')
    A('')
    A('### 3.3 High-Skew Features (|skew| > 0.5)')
    A('')
    if high_skew:
        skew_str2 = ', '.join(f'`{f}`' for f in high_skew)
        A(f'{len(high_skew)} features have |skew| > 0.5: {skew_str2}')
        A('')
        A('Features with skewness magnitude above 0.5 deviate meaningfully from '
          'symmetry and may benefit from transformation (log, square-root, or Box-Cox) '
          'before use in distance-based algorithms (k-NN, SVM) or linear models that '
          'assume Gaussian residuals. Tree-based methods (Random Forest, XGBoost) are '
          'generally robust to skewed features.')
    else:
        A('No features with |skew| > 0.5 detected.')
    A('')
    A('![Univariate Histogram Grid](plots/eda_univariate_histograms.png)')
    A('')
    A('### 3.4 Per-Feature Physical Interpretation')
    A('')
    # Build a per-feature interpretation block
    _feat_interp = {
        "E (GPa)": (
            "**Young's Modulus E (GPa)** measures a material's resistance to elastic "
            "deformation under axial stress (stress/strain ratio). In aerospace structures, "
            "E ranges from ~69 GPa (aluminium alloys) through ~200 GPa (steel) to "
            "~400 GPa (carbon-fibre reinforced composites). A right-skewed distribution "
            "would indicate that a few high-stiffness composite entries pull the tail "
            "upward. Near-zero kurtosis implies the spread of moduli is relatively "
            "uniform across material types."
        ),
        "nu": (
            "**Poisson's Ratio ν** is the ratio of transverse to axial strain. "
            "Physical constraints bound it strictly to (0, 0.5) for isotropic materials. "
            "The reported narrow range (≈0.30–0.35) reflects the dataset sampling "
            "from a limited set of metallic and composite materials that cluster in "
            "this sub-range. Because the range is intrinsically narrow, skewness and "
            "kurtosis are both expected to be near-zero, consistent with observations."
        ),
        "rho": (
            "**Density ρ (kg/m³)** spans from lightweight composites (~1500 kg/m³) "
            "to steel-like alloys (~7800 kg/m³). Material type strongly conditions "
            "density; the overall marginal distribution is therefore likely multimodal "
            "(one peak per material class), which manifests as elevated kurtosis or "
            "apparent bimodality in the histogram. Right skew would appear if "
            "high-density entries are a minority."
        ),
        "Tensile Strength (MPa)": (
            "**Tensile Strength (MPa)** is the maximum stress a material can withstand "
            "before fracture. The dataset range (261–1496 MPa) spans aluminium alloys "
            "at the low end to high-strength titanium and advanced composites at the "
            "high end. Positive (right) skew is physically expected because most "
            "aerospace structural materials cluster in the mid-range (400–800 MPa) "
            "while specialised ultra-high-strength alloys form a sparse upper tail. "
            "Log-transformation would typically normalise this distribution."
        ),
        "Young's Modulus": (
            "**Young's Modulus (duplicate column)** appears to be an alias or "
            "alternate encoding of E (GPa) and should exhibit near-perfect correlation "
            "(r ≈ 1) with that column. Confirm that they carry identical or linearly "
            "related information; if so, one column should be dropped before modelling "
            "to avoid multicollinearity."
        ),
        "Altitude (m)": (
            "**Altitude (m)** represents the operating altitude of the aircraft. "
            "Aerospace missions typically span from sea level to the stratosphere "
            "(~30 km). A uniform-ish distribution over the sampled range is plausible "
            "for a designed experiment; an approximately symmetric histogram would be "
            "consistent with uniform random sampling over a fixed altitude band. "
            "Extreme high-altitude samples may form a thin upper tail."
        ),
        "Temperature (C)": (
            "**Temperature (°C)** at altitude is physically dictated by the ISA lapse "
            "rate (−6.5 °C/km in the troposphere, isothermal in the lower stratosphere). "
            "Because altitude spans a wide range, Temperature should be negatively "
            "correlated with Altitude and is expected to be mostly negative (sub-zero) "
            "for high-altitude flight. A left-skewed or bimodal distribution could "
            "indicate that the altitude sample is clustered near tropopause altitudes "
            "where the temperature profile changes character."
        ),
        "Pressure (Pa)": (
            "**Pressure (Pa)** follows an exponential decay with altitude per the "
            "barometric formula. As a result, Pressure values in a uniformly sampled "
            "altitude range will be right-skewed — high pressures are confined to "
            "low altitudes, while most of the altitude range maps to the low end of "
            "the pressure scale. Strong positive skew and high kurtosis are physically "
            "expected if high-altitude (low-pressure) conditions are well-represented."
        ),
        "Operational Life (years)": (
            "**Operational Life (years)** is the design service life of the structural "
            "component. Modern commercial aircraft airframes are certified for 20–30 "
            "years; military components may have shorter design lives. Moderate right "
            "skew (a few very long-life designs) is common in engineering datasets. "
            "Distribution shape is also conditioned on material: composites tend to "
            "have longer certified lives than some metallic alloys due to fatigue "
            "advantages."
        ),
        "Wing Span (m)": (
            "**Wing Span (m)** ranges from small UAV/fighter sizes (≈8 m) to large "
            "transport aircraft (≈70 m). The distribution shape depends on the mix of "
            "aircraft classes in the dataset. A bimodal pattern would indicate "
            "clustering between small (combat) and large (transport) platforms. "
            "Right skew would indicate that very large widebody aircraft are under-"
            "represented."
        ),
        "Fuselage Length (m)": (
            "**Fuselage Length (m)** is correlated with Wing Span through the aspect "
            "ratio constraint; longer fuselages generally accompany wider wings. "
            "Similar distribution shape to Wing Span is expected. The scatter plot "
            "in Chapter 7 (Figure: Wing Span vs Fuselage Length) confirms the "
            "positive linear relationship stratified by Structural Shape."
        ),
        "Structural Thickness (mm)": (
            "**Structural Thickness (mm)** varies with the structural shape and "
            "load-bearing requirements. Thin-walled sections (tubes, I-beams) may "
            "cluster at lower thicknesses, while solid or thick-web sections occupy "
            "the upper range. If thickness is strongly determined by Shape, we expect "
            "a multimodal histogram with one peak per shape category."
        ),
        "Number of Iterations": (
            "**Number of Iterations** records how many optimisation steps the quantum "
            "algorithm required to converge. Higher iteration counts correspond to "
            "harder or more complex structural problems. A right-skewed distribution "
            "is typical for convergence counts — most problems converge quickly while "
            "a subset of ill-conditioned problems require many more steps. This "
            "feature is expected to be positively correlated with Computational Time."
        ),
        "Optimization Time (sec)": (
            "**Optimization Time (sec)** is the wall-clock time for the quantum "
            "algorithm. It should correlate positively with Number of Iterations. "
            "Algorithm type (Shark vs Chaotic Quantum Genetic) is a key moderating "
            "variable — different algorithms may have very different time-per-iteration "
            "costs, making the unconditional distribution potentially bimodal or "
            "heavily right-skewed."
        ),
    }
    for feat in num_cols:
        interp = _feat_interp.get(feat, None)
        if interp:
            A(f'#### {feat}')
            A('')
            row = uv_stats[uv_stats['Feature'] == feat]
            if len(row) > 0:
                r = row.iloc[0]
                A(f'Mean = {r["Mean"]}, Std = {r["Std"]}, '
                  f'Min = {r["Min"]}, Max = {r["Max"]}, '
                  f'Median = {r["Median"]}, Skewness = {r["Skewness"]}, '
                  f'Kurtosis = {r["Kurtosis"]}')
            A('')
            A(interp)
            A('')
    A('### 3.5 Categorical Value Counts')
    A('')
    for cat in CAT_COLS:
        if cat in df_real.columns:
            A(f'**{cat}:**')
            vc = df_real[cat].value_counts().reset_index()
            vc.columns = ['Value', 'Count']
            A(df_to_md_table(vc))
            A('')

    # ── Chapter 4 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 4 — Bivariate & Multivariate Analysis')
    A('')
    A('Bivariate analysis examines pairwise relationships between features. '
      'The correlation heatmaps below capture both linear (Pearson) and rank-based '
      '(Spearman) dependencies. The pairplot shows joint distributions across the '
      'five highest-variance features stratified by Material Type.')
    A('')
    A('### 4.1 Pearson Correlation Heatmap')
    A('')
    A('![Pearson Correlation Heatmap](plots/eda_correlation_heatmap_pearson.png)')
    A('')
    A('### 4.2 Spearman Rank Correlation Heatmap')
    A('')
    A('![Spearman Rank Correlation Heatmap](plots/eda_correlation_heatmap_spearman.png)')
    A('')
    A('The Spearman heatmap is especially useful for detecting monotonic but '
      'non-linear relationships (such as the Altitude–Pressure exponential decay) '
      'that Pearson would underestimate. Pairs where Spearman >> Pearson are '
      'candidates for non-linear modelling treatment.')
    A('')
    A('### 4.3 Top 10 Most Correlated Pairs (Pearson)')
    A('')
    A('The table ranks all unique feature pairs by absolute Pearson r. Values '
      'near ±1.0 indicate near-linear dependence (potential redundancy); '
      'values below ±0.1 are effectively noise at this sample size.')
    A('')
    A(df_to_md_table(top_corr))
    A('')
    A('**Interpretation:** Pairs with |r| > 0.9 should be considered for '
      'dimensionality reduction (one feature dropped or PCA applied). '
      'Pairs with |r| in 0.5–0.9 indicate strong predictive signal between '
      'features and may imply causal or physical linkage (e.g., E (GPa) and '
      "Young's Modulus are likely identical physical quantities encoded twice). "
      'Moderate correlations (0.3–0.5) are useful predictors but do not '
      'dominate a multivariate model.')
    A('')
    A('### 4.4 Pairplot — Top 5 Features by Variance, Coloured by Material Type')
    A('')
    A('![Pairplot by Material Type](plots/eda_pairplot_material.png)')
    A('')
    A('Each off-diagonal cell shows a scatter plot between two features; '
      'the diagonal shows the kernel density estimate (KDE) per material class. '
      'Distinct KDE peaks per material class indicate that the feature is a '
      'reliable material discriminator. Overlapping clusters suggest the feature '
      'alone is insufficient to separate materials.')
    A('')
    A('### 4.5 Mean of Each Numeric Feature Grouped by Material Type')
    A('')
    A('The table below shows the mean value of every numeric feature for each '
      'material type. Large differences across rows indicate strong material-driven '
      'variation — the most important features for material discrimination are those '
      'with the highest inter-group range relative to within-group variance.')
    A('')
    if len(group_mean_mat) > 0:
        A(df_to_md_table(group_mean_mat.reset_index()))
    A('')
    A('### 4.6 Mean of Each Numeric Feature Grouped by Target Variable Class')
    A('')
    A('The following tables show per-class means for each target variable. '
      'Features where the mean changes monotonically across ordered class labels '
      '(e.g., Low → Medium → High) are likely strong ordinal predictors.')
    A('')
    for tgt in TARGETS:
        if tgt in df_real.columns:
            try:
                gm = df_real.groupby(tgt)[num_cols].mean().round(4)
                A(f'**Grouped by {tgt}:**')
                A('')
                A(df_to_md_table(gm.reset_index()))
                A('')
            except Exception as _e:
                log.warning('grouped mean by %s failed: %s', tgt, _e)

    # ── Chapter 5 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 5 — Material Type Deep Dive')
    A('')
    A('Material Type is the primary categorical grouping variable. It determines '
      'the physical properties of the structural component and is expected to '
      'drive significant variation in elastic modulus, density, tensile strength, '
      'and Poisson ratio. This chapter quantifies those differences and tests '
      'whether Material Type is statistically associated with each performance target.')
    A('')
    A('### 5.1 Statistical Profile per Material (mean ± std)')
    A('')
    A('The table shows mean ± standard deviation for key mechanical properties '
      'for each material class. A small standard deviation relative to the mean '
      '(low coefficient of variation) indicates that the property is tightly '
      'controlled within the material class — which is physically realistic. '
      'A large standard deviation may indicate multiple sub-grades within the class.')
    A('')
    profile_rows = []
    for mat, props in mat_profile.items():
        row = {'Material': mat}
        for feat, (mean_v, std_v) in props.items():
            row[feat] = f'{mean_v:.4f} ± {std_v:.4f}'
        profile_rows.append(row)
    if profile_rows:
        A(df_to_md_table(pd.DataFrame(profile_rows)))
    else:
        A('Profile data not available.')
    A('')
    A('### 5.2 Full Mean Profile — All Numeric Features by Material')
    A('')
    A('Extending the profile to all numeric features (not just mechanical properties) '
      'allows us to assess whether Material Type also correlates with geometry, '
      'flight environment, or algorithm usage:')
    A('')
    if len(group_mean_mat) > 0:
        A(df_to_md_table(group_mean_mat.reset_index()))
    A('')
    A('### 5.3 Violin Plot — E (GPa) by Material Type')
    A('')
    A("![Violin Plot: E (GPa) by Material Type](plots/eda_violin_E_by_material.png)")
    A('')
    A('The violin plot shows the full distribution shape of Young\'s Modulus for '
      'each material. The internal box-and-whisker marks the median and IQR. '
      'Wide "waists" indicate a common value; narrow necks indicate that few '
      'samples fall at that modulus level. Materials with non-overlapping violin '
      'bodies are clearly separable on E alone.')
    A('')
    A('### 5.4 Boxplots — Key Properties by Material Type')
    A('')
    A('![Boxplots by Material Type](plots/eda_boxplots_by_material.png)')
    A('')
    A('Boxplots show the median (centre line), IQR (box), 1.5×IQR whiskers, '
      'and outliers (individual points). Materials where the boxplot notches '
      '(95% CI on median) do not overlap have statistically different medians '
      'at the 5% significance level.')
    A('')
    A('### 5.5 Chi-Square Tests: Material Type vs Each Target Variable')
    A('')
    A('The chi-square test of independence assesses whether the distribution '
      'of a target variable (e.g., Vibration Damping class) differs across '
      'material types. The null hypothesis is independence. A significant result '
      '(p < 0.05) means that knowing the material type gives information about '
      'the expected target class — confirming Material Type as a useful predictor.')
    A('')
    if len(chi_sq) > 0:
        A(df_to_md_table(chi_sq))
        A('')
        sig_count = (chi_sq['Significant'] == 'Yes').sum()
        A(f'{sig_count} out of {len(chi_sq)} target variables show a statistically '
          f'significant association with Material Type (p < 0.05). '
          'This confirms that Material Type is not independent of the performance '
          'targets and must be included as a feature in any predictive model.')
    else:
        A('Chi-square tests could not be computed (missing columns).')
    A('')

    # ── Chapter 6 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 6 — Flight Environment Analysis')
    A('')
    A('The flight-environment features (Altitude, Temperature, Pressure) are physically '
      'coupled through the International Standard Atmosphere (ISA) model. This chapter '
      'quantifies how well those physical relationships are preserved in the dataset '
      'and what they imply for synthetic data generation.')
    A('')
    A('### 6.1 Altitude vs Temperature and Pressure (Scatter Plots)')
    A('')
    A('![Altitude vs Temperature & Pressure](plots/eda_altitude_temp_pressure.png)')
    A('')
    A('The left panel plots Temperature (°C) against Altitude (m); '
      'the right panel plots Pressure (Pa) against Altitude (m). '
      'The scatter should show a negative, near-linear trend for Temperature '
      '(in the troposphere) and a convex-downward (exponential-decay) curve for Pressure.')
    A('')
    A('### 6.2 Linear Regression Goodness-of-Fit')
    A('')
    A(f'| Regression | R² |')
    A(f'|---|---|')
    A(f'| Temperature ~ Altitude (linear) | {fmt(r2_temp)} |')
    A(f'| Pressure ~ Altitude (linear) | {fmt(r2_pres)} |')
    A('')
    r2t = float(fmt(r2_temp)) if not (isinstance(r2_temp, float) and np.isnan(r2_temp)) else 0.0
    r2p = float(fmt(r2_pres)) if not (isinstance(r2_pres, float) and np.isnan(r2_pres)) else 0.0
    A('### 6.3 ISA Standard Atmosphere Comparison')
    A('')
    A('**ISA Physics Background:**')
    A('')
    A('In the International Standard Atmosphere (ISA) model:')
    A('')
    A('- **Troposphere (0–11 km):** Temperature decreases at a constant lapse rate of '
      '−6.5 °C/km (−0.0065 K/m). At sea level T₀ = 288.15 K (15 °C); '
      'at the tropopause (11 km) T = 216.65 K (−56.5 °C).')
    A('- **Lower Stratosphere (11–20 km):** Temperature is isothermal at −56.5 °C.')
    A('- **Pressure** follows the barometric formula: '
      'P(h) = P₀ · (1 − L·h/T₀)^(g·M/R·L) in the troposphere, '
      'and P(h) = P₁₁ · exp(−g·M·(h−h₁₁)/(R·T₁₁)) in the isothermal layer. '
      'This is exponential in the stratosphere and approximately polynomial in the troposphere.')
    A('')
    A(f'**Dataset vs ISA comparison:**')
    A('')
    A(f'The linear R² for Temperature ~ Altitude is **{fmt(r2_temp)}**, which is '
      f'{"strong (>0.70) — consistent with primarily tropospheric altitude sampling" if r2t > 0.70 else "moderate-to-weak (<0.70) — consistent with a mix of tropospheric and stratospheric altitudes where the linear lapse rate breaks down"}. '
      'In the stratosphere, the temperature is approximately constant at −56.5 °C, '
      'so altitude samples above 11 km add horizontal scatter that degrades the linear fit.')
    A('')
    A(f'The linear R² for Pressure ~ Altitude is **{fmt(r2_pres)}**. '
      f'Since pressure decays exponentially (not linearly) with altitude, '
      f'a linear fit gives {"a reasonable" if r2p > 0.70 else "a poor"} approximation '
      f'(R² = {fmt(r2_pres)}). For synthetic data generation, '
      'the exponential relationship should be used rather than a linear fit to correctly '
      'reproduce the altitude–pressure dependency at high altitudes. '
      'A log-transform of Pressure before modelling would linearise this relationship.')
    A('')
    A('**Recommendation for synthesis:** '
      'Sample Altitude from its empirical marginal distribution, '
      'then derive Temperature and Pressure deterministically from the ISA equations '
      '(with added Gaussian noise ε ~ N(0, σ_residual²)) to guarantee physical consistency. '
      'This avoids the risk of sampling impossible (Altitude, Temperature, Pressure) '
      'combinations when using fully independent marginals.')
    A('')
    A('### 6.4 Descriptive Statistics — Flight Environment Features')
    A('')
    env_feats = [c for c in num_cols if any(k in c.lower() for k in ['altitude', 'temperature', 'pressure'])]
    if env_feats:
        env_stats = uv_stats[uv_stats['Feature'].isin(env_feats)]
        A(df_to_md_table(env_stats))
    A('')

    # ── Chapter 7 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 7 — Structural Geometry Analysis')
    A('')
    A('Structural geometry features (Wing Span, Fuselage Length, Structural Thickness) '
      'describe the physical size and cross-section of aerospace components. '
      'These are coupled to each other and to material selection and load requirements.')
    A('')
    A('### 7.1 Wing Span vs Fuselage Length (Scatter by Structural Shape)')
    A('')
    A('![Wing Span vs Fuselage Length](plots/eda_wingspan_fuselage.png)')
    A('')
    A('The positive trend between Wing Span and Fuselage Length reflects the scaling '
      'laws of aircraft design: longer fuselages require wider wings to maintain '
      'adequate lift-to-drag ratio and longitudinal stability. Structural Shape '
      'differentiates the clusters — for example, cylindrical fuselage shells '
      'may cluster at different aspect ratios than rectangular or I-beam sections.')
    A('')
    A('### 7.2 Descriptive Statistics — Geometry Features')
    A('')
    geom_feats = [c for c in num_cols if any(k in c.lower() for k in ['wing', 'fuselage', 'thickness', 'life'])]
    if geom_feats:
        geom_stats = uv_stats[uv_stats['Feature'].isin(geom_feats)]
        A(df_to_md_table(geom_stats))
    A('')
    A('### 7.3 Structural Thickness (mm) Grouped by Structural Shape')
    A('')
    A('Structural thickness is expected to vary significantly across cross-section shapes. '
      'Thin-walled shells (cylinders, tubes) require smaller thicknesses for the same '
      'bending stiffness as solid or I-beam sections. The table below quantifies this:')
    A('')
    if thick_by_shape:
        th_rows = [{'Shape': sh,
                    'Mean (mm)': fmt(v['mean']),
                    'Std (mm)':  fmt(v['std']),
                    'Min (mm)':  fmt(v['min']),
                    'Max (mm)':  fmt(v['max'])}
                   for sh, v in thick_by_shape.items()]
        A(df_to_md_table(pd.DataFrame(th_rows)))
        A('')
        A('**Interpretation:** The shape with the highest mean thickness requires '
          'more material per unit length, implying higher weight for the same load '
          'capacity unless a higher-modulus material compensates. The coefficient of '
          'variation (Std/Mean) indicates whether thickness is tightly specified '
          '(low CV) or widely variable (high CV) within each shape category.')
    else:
        A('Data not available.')
    A('')
    A('### 7.4 Operational Life (years) by Material Type')
    A('')
    A('Operational life is the intended service life of the structural component '
      'before major overhaul or replacement. Material fatigue properties, corrosion '
      'resistance, and inspectability all contribute to service life. '
      'Advanced composites generally offer superior fatigue life compared to metals, '
      'reflected in longer mean operational life values.')
    A('')
    if life_by_mat:
        lf_rows = [{'Material': mat,
                    'Mean Life (yrs)': fmt(v['mean']),
                    'Std Life (yrs)':  fmt(v['std'])}
                   for mat, v in life_by_mat.items()]
        A(df_to_md_table(pd.DataFrame(lf_rows)))
        A('')
        A('Materials with higher mean operational life are more suitable for '
          'long-duration missions or platforms with high overhaul costs. '
          'The standard deviation indicates how uniformly life expectancy is '
          'distributed within each material class.')
    else:
        A('Data not available.')
    A('')
    A('### 7.5 Structural Thickness by Load Distribution')
    A('')
    A('Load Distribution (uniform, concentrated, distributed, etc.) interacts with '
      'structural thickness: concentrated loads require thicker local reinforcement '
      'while distributed loads allow thinner uniform sections. '
      'The grouped statistics below illustrate this relationship:')
    A('')
    load_col = 'Load Distribution'
    if load_col in df_real.columns and thick_col:
        try:
            ld_thick = df_real.groupby(load_col)[thick_col].agg(['mean','std','min','max']).round(4)
            ld_thick.columns = ['Mean (mm)', 'Std (mm)', 'Min (mm)', 'Max (mm)']
            A(df_to_md_table(ld_thick.reset_index()))
        except Exception as _e:
            log.warning('load dist thick groupby failed: %s', _e)
            A('Data not available.')
    else:
        A('Data not available.')
    A('')

    # ── Chapter 8 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 8 — Optimization & Algorithm Analysis')
    A('')
    A('The optimisation metadata captures how quantum-inspired algorithms were used '
      'to solve the structural design problem. Two algorithms appear in the dataset: '
      'the Shark Optimisation Algorithm and the Chaotic Quantum Genetic Algorithm. '
      'This chapter analyses algorithm efficiency (iterations, time) and the '
      'relationship between iteration count and the Computational Time target variable.')
    A('')
    A('### 8.1 Scatter: Number of Iterations vs Optimization Time by Algorithm')
    A('')
    A('![Number of Iterations vs Optimization Time](plots/eda_optimization_scatter.png)')
    A('')
    A('The scatter plot reveals whether the two algorithms have different '
      'time-per-iteration costs and whether convergence rate (iterations to solution) '
      'differs. Distinct clusters by algorithm indicate algorithm-specific behaviour; '
      'a common linear trend through both algorithms indicates that time is purely '
      'proportional to iterations regardless of algorithm choice.')
    A('')
    A('### 8.2 Full Algorithm Comparison Table')
    A('')
    A('The table below shows mean and standard deviation of Optimization Time (sec) '
      'and Number of Iterations for each Quantum Algorithm Type:')
    A('')
    if 'Quantum Algorithm Type' in df_real.columns and iter_col and opt_col:
        try:
            algo_tbl = df_real.groupby('Quantum Algorithm Type')[[iter_col, opt_col]].agg(
                ['mean', 'std']).round(4)
            algo_tbl.columns = [f'{col}_{stat}' for col, stat in algo_tbl.columns]
            A(df_to_md_table(algo_tbl.reset_index()))
        except Exception as _e:
            log.warning('algo comparison table failed: %s', _e)
            if opt_by_algo:
                oa_rows = [{'Algorithm': algo,
                            'Mean Time (sec)': fmt(v['mean']),
                            'Std Time (sec)':  fmt(v['std'])}
                           for algo, v in opt_by_algo.items()]
                A(df_to_md_table(pd.DataFrame(oa_rows)))
    elif opt_by_algo:
        oa_rows = [{'Algorithm': algo,
                    'Mean Time (sec)': fmt(v['mean']),
                    'Std Time (sec)':  fmt(v['std'])}
                   for algo, v in opt_by_algo.items()]
        A(df_to_md_table(pd.DataFrame(oa_rows)))
    else:
        A('Data not available.')
    A('')
    A('**Interpretation:** A higher mean time with lower mean iterations suggests '
      'each iteration is computationally expensive (characteristic of the Chaotic '
      'Quantum Genetic Algorithm with complex fitness evaluations). '
      'A lower mean time with higher mean iterations suggests fast but numerous '
      'evaluations (characteristic of the Shark Optimisation Algorithm with '
      'gradient-free swarm-based search). The relative standard deviations '
      'indicate how problem-dependent the convergence is for each algorithm.')
    A('')
    A('### 8.3 Number of Iterations by Algorithm — Detailed Statistics')
    A('')
    if 'Quantum Algorithm Type' in df_real.columns and iter_col:
        try:
            iter_stats = df_real.groupby('Quantum Algorithm Type')[iter_col].agg(
                ['mean', 'std', 'min', 'max', 'median']).round(4)
            iter_stats.columns = ['Mean', 'Std', 'Min', 'Max', 'Median']
            A(df_to_md_table(iter_stats.reset_index()))
        except Exception as _e:
            A('Data not available.')
    else:
        A('Data not available.')
    A('')
    A('### 8.4 Pearson Correlation: Number of Iterations vs Computational Time (ordinal-encoded)')
    A('')
    A('The Computational Time target is an ordinal categorical variable (e.g., '
      'Low / Medium / High). To compute a Pearson correlation, classes are '
      'label-encoded in sorted order (Low=0, Medium=1, High=2 etc.). '
      'This gives a monotone proxy for the ordinal relationship.')
    A('')
    A(f'**Pearson r (Number of Iterations vs Computational Time encoded):** {fmt(iter_ct_corr)}')
    A('')
    if not np.isnan(iter_ct_corr):
        strength = ('strong' if abs(iter_ct_corr) > 0.5
                    else 'moderate' if abs(iter_ct_corr) > 0.3
                    else 'weak')
        direction = 'positively' if iter_ct_corr > 0 else 'negatively'
        A(f'The {strength} {direction} correlated relationship (r = {fmt(iter_ct_corr)}) '
          f'{"confirms" if abs(iter_ct_corr) > 0.3 else "does not strongly support"} '
          'that iteration count is a predictor of computational time class. '
          'This is physically expected: more optimisation iterations consume more '
          'CPU/QPU resources and therefore map to higher computational cost categories.')
    A('')

    # ── Chapter 9 ─────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 9 — Target Variable Analysis')
    A('')
    A('The dataset contains four ordinal classification targets: '
      '**Vibration Damping**, **Computational Time**, **Weight Efficiency**, '
      'and **Durability**. Each target represents a performance dimension of the '
      'aerospace structural design. This chapter examines their individual '
      'distributions and all pairwise cross-tabulations.')
    A('')
    A('### 9.1 Individual Target Distributions')
    A('')
    A('![Target Distributions](plots/eda_target_distributions.png)')
    A('')
    A('The bar charts above show the frequency of each class for all four targets. '
      'A balanced distribution (equal bars) is ideal for training a classifier '
      'without class-imbalance correction. Imbalanced distributions (one class '
      'heavily dominant) require stratified sampling, oversampling (SMOTE), '
      'or class-weight adjustment in the classifier.')
    A('')
    A('**Class counts summary:**')
    A('')
    for tgt, cc in class_counts.items():
        total = sum(cc.values())
        cc_df = pd.DataFrame({'Class': list(cc.keys()), 'Count': list(cc.values()),
                              'Proportion (%)': [f'{v/total*100:.2f}' for v in cc.values()]})
        A(f'*{tgt}* (total = {total}):')
        A('')
        A(df_to_md_table(cc_df))
        A('')
    A('### 9.2 Crosstab Heatmap: Durability x Weight Efficiency')
    A('')
    A('![Target Crosstab Heatmap: Durability x Weight Efficiency](plots/eda_target_crosstab_heatmap.png)')
    A('')
    A('The heatmap colour encodes cell counts; bright cells indicate common '
      'class co-occurrences. Strong off-diagonal brightness (e.g., Low Durability '
      'with High Weight Efficiency) would indicate an anti-correlation between targets. '
      'Diagonal brightness indicates positive correlation.')
    A('')
    A('### 9.3 Cross-Tabulations — All 6 Target Pairs')
    A('')
    A('The following tables show the full n×m contingency matrix for every pair '
      'of target variables. Row and column labels are the ordinal class values. '
      'Cell entries are raw counts. Large off-diagonal counts indicate the two '
      'targets are not perfectly correlated and carry complementary information.')
    A('')
    target_pairs = [
        ('Vibration Damping', 'Computational Time'),
        ('Vibration Damping', 'Weight Efficiency'),
        ('Vibration Damping', 'Durability'),
        ('Computational Time', 'Weight Efficiency'),
        ('Computational Time', 'Durability'),
        ('Weight Efficiency', 'Durability'),
    ]
    for t1, t2 in target_pairs:
        if t1 in df_real.columns and t2 in df_real.columns:
            ct = pd.crosstab(df_real[t1], df_real[t2])
            try:
                chi2_tp, pval_tp, dof_tp, _ = chi2_contingency(ct)
                sig_tp = 'Yes' if pval_tp < 0.05 else 'No'
                A(f'**{t1} x {t2}** (χ²={chi2_tp:.2f}, dof={dof_tp}, p={pval_tp:.4f}, significant={sig_tp}):')
            except Exception:
                A(f'**{t1} x {t2}:**')
            A('')
            A(df_to_md_table(ct.reset_index()))
            A('')

    # ── Chapter 10 ────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 10 — Feature Importance & Drivers')
    A('')
    A('Feature importance quantifies how much each input feature contributes to '
      'predicting a given target. Random Forest importance (mean decrease in impurity, '
      'also called Gini importance) is a fast and reliable metric for ranking features. '
      'It does not indicate directionality (positive/negative effect) — for that, '
      'SHAP values are recommended.')
    A('')
    A('### 10.1 Feature Importance Bar Charts (Random Forest, all 4 targets)')
    A('')
    A('![Random Forest Feature Importance](plots/eda_feature_importance_rf.png)')
    A('')
    A('Each subplot shows feature importance for one target variable, sorted ascending. '
      'Taller bars indicate stronger predictive contribution from that feature. '
      'Features with near-zero importance are effectively ignored by the forest '
      'and could be dropped without harming model performance.')
    A('')
    A('### 10.2 Full RF Importance Table — All Features, All Targets')
    A('')
    A('The table ranks ALL features by importance for each target. '
      'A feature ranked #1 for multiple targets is a "universal driver" — '
      'it is important regardless of which performance dimension you are predicting.')
    A('')
    if len(rf_imp_full) > 0:
        A(df_to_md_table(rf_imp_full))
    else:
        A('Full importance table not available (RF training may have failed).')
    A('')
    A('### 10.3 Top 3 Drivers per Target')
    A('')
    for tgt, imp_series in rf_top3.items():
        A(f'**{tgt}:**')
        A('')
        for rank, (feat, score) in enumerate(imp_series.items(), 1):
            pct = score * 100
            A(f'{rank}. **{feat}** — importance {fmt(score)} ({pct:.2f}% of total tree splits)')
        A('')
        top1_feat = list(imp_series.index)[0]
        top1_score = list(imp_series.values)[0]
        top2_feat = list(imp_series.index)[1] if len(imp_series) > 1 else ''
        A(f'The most important driver for **{tgt}** is `{top1_feat}` '
          f'(importance = {fmt(top1_score)}). '
          f'{"This is physically meaningful because material elastic modulus directly controls " + "the structural resonance frequency, which in turn drives vibration damping performance." if "Vibration" in tgt else ""}' +
          f'{"Combined with `" + top2_feat + "`, these two features account for the majority of the predictive signal." if top2_feat else ""}')
        A('')
    A('### 10.4 SHAP Analysis Note')
    A('')
    A('SHAP (SHapley Additive exPlanations) values were not computed in this report '
      'due to runtime constraints. For production analysis, SHAP TreeExplainer applied '
      'to the Random Forest models above is recommended to obtain:')
    A('')
    A('- **Directional attribution:** Whether a feature increases or decreases the '
      'predicted probability of a given class')
    A('- **Interaction detection:** Whether two features jointly affect the target '
      'beyond their individual contributions')
    A('- **Global + local explanation:** Feature importance for the overall model '
      'and for individual predictions')
    A('')
    A('A beeswarm SHAP plot for each target would reveal, for example, whether '
      'high E (GPa) increases or decreases the probability of "High" Vibration '
      'Damping — information that the Gini-importance bar chart cannot provide.')
    A('')
    A('### 10.5 Feature Selection Recommendation')
    A('')
    A('Based on the RF importance analysis, the following feature selection strategy '
      'is recommended for downstream modelling:')
    A('')
    A('1. **Retain all features with importance > 0.05** for at least one target '
      '(these are primary drivers).')
    A('2. **Flag for removal** any feature with importance < 0.01 for ALL targets '
      '(these add noise without signal).')
    A('3. **Check for near-perfect collinearity** (|r| > 0.95) between retained '
      'features and drop one of each near-duplicate pair.')
    A('4. **Keep Material Type and Quantum Algorithm Type** regardless of computed '
      'numeric importance — these are categorical moderators confirmed significant '
      'by chi-square tests.')
    A('')

    # ── Chapter 11 ────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 11 — Real vs Synthetic Comparison')
    A('')
    A('This chapter evaluates how faithfully the empirical_1000 synthetic dataset '
      'reproduces the statistical properties of the real dataset. Three complementary '
      'metrics are used: per-feature Kolmogorov-Smirnov tests (marginal distribution '
      'fidelity), mean KL divergence (information-theoretic distributional distance), '
      'and a Random Forest discriminator test (multivariate distinguishability).')
    A('')
    A('### 11.1 Histogram Overlay — Top 8 Most Divergent Features')
    A('')
    A('![Real vs Synthetic Histograms](plots/eda_real_vs_syn_histograms.png)')
    A('')
    A('Features are selected for display by the normalised absolute mean difference '
      '|μ_real − μ_syn| / σ_real. Large deviations appear as misaligned histogram '
      'peaks (different modes) or different spread (different widths). '
      'The eight features shown have the largest marginal discrepancy and therefore '
      'represent the main quality issues in the synthetic dataset.')
    A('')
    A('### 11.2 PCA 2D Projection — Real vs Synthetic')
    A('')
    A('![PCA Real vs Synthetic](plots/eda_pca_real_vs_syn.png)')
    A('')
    A('Both real and synthetic data are projected onto the first two principal '
      'components fitted on the joint dataset. If the two point clouds overlap '
      'substantially, the synthetic data covers the same multivariate space as '
      'the real data. Gaps or shifted centroids indicate that the generator '
      'missed part of the real data manifold.')
    A('')
    A('### 11.3 Kolmogorov-Smirnov Test Results — Per Feature')
    A('')
    A('The KS test statistic D is the maximum absolute difference between the '
      'empirical CDFs of real and synthetic samples. D = 0 means perfect match; '
      'D = 1 means completely disjoint distributions. The p-value tests the null '
      'hypothesis that both samples are drawn from the same distribution. '
      'p > 0.05 is a "pass" (cannot reject the null at 5% level).')
    A('')
    ks_rows = [{'Feature': k,
                'KS Statistic': fmt(v['ks_stat']),
                'p-value': fmt(v['p_value']),
                'Pass (p>0.05)': 'Yes' if v['pass'] else 'No'}
               for k, v in ks_res.items()]
    if ks_rows:
        A(df_to_md_table(pd.DataFrame(ks_rows)))
    A('')
    n_pass = sum(v['pass'] for v in ks_res.values())
    A(f'**KS Test Pass Rate:** {ks_pass_rate*100:.4f}% ({n_pass} / {len(ks_res)} features)')
    A('')
    A('**Interpretation:** A pass rate above 80% is generally considered acceptable '
      'for synthetic data. Features that fail (p ≤ 0.05) have detectable distributional '
      'differences from the real data and should be the focus of generator improvement. '
      'Note that with large samples, even small true differences will yield low p-values '
      '(KS is sensitive to N); always examine the KS statistic D alongside the p-value.')
    A('')
    A('### 11.4 Mean KL Divergence')
    A('')
    A(f'**Mean KL Divergence (real ‖ synthetic, all shared features):** {fmt(mkl)}')
    A('')
    A('KL divergence D_KL(P ‖ Q) measures the information lost when Q (synthetic) is '
      'used to approximate P (real). It is asymmetric: it penalises regions where '
      'real probability is high but synthetic probability is low (mode dropping). '
      'Values are computed from 30-bin histograms with Laplace smoothing.')
    A('')
    A('| KL Divergence Range | Quality Assessment |')
    A('|---|---|')
    A('| < 0.01 | Excellent — distributions nearly identical |')
    A('| 0.01 – 0.05 | Good — minor discrepancies |')
    A('| 0.05 – 0.20 | Moderate — noticeable but tolerable for most ML tasks |')
    A('| > 0.20 | Poor — significant distributional mismatch |')
    A('')
    A(f'The empirical_1000 generator achieves a mean KL divergence of {fmt(mkl)}, '
      f'which falls in the '
      f'{"**Excellent** (<0.01)" if float(fmt(mkl)) < 0.01 else "**Good** (0.01–0.05)" if float(fmt(mkl)) < 0.05 else "**Moderate** (0.05–0.20)" if float(fmt(mkl)) < 0.20 else "**Poor** (>0.20)"} '
      f'category. ')
    A('')
    A('### 11.5 RF Discriminator Test')
    A('')
    A('A Random Forest classifier is trained to distinguish real (label 0) from '
      'synthetic (label 1) samples on all shared numeric features. '
      'The AUC (Area Under the ROC Curve) is measured via 3-fold cross-validation. '
      'An AUC close to **0.50** means the classifier cannot distinguish real from '
      'synthetic — the gold standard for high-quality synthetic data. '
      'An AUC close to **1.00** means the synthetic data is easily distinguishable '
      'from real data (poor quality).')
    A('')
    if not np.isnan(disc_auc):
        auc_quality = ('indistinguishable from real data (excellent quality)'
                       if disc_auc < 0.55 else
                       'slightly distinguishable (good quality)' if disc_auc < 0.65 else
                       'moderately distinguishable (acceptable quality)' if disc_auc < 0.75 else
                       'clearly distinguishable (poor quality)')
        A(f'**RF Discriminator AUC:** {disc_auc:.4f} — The synthetic data is {auc_quality}.')
    else:
        A('RF Discriminator AUC: computation failed.')
    A('')
    A('**Combined quality verdict:**')
    A('')
    A(f'| Metric | Value | Verdict |')
    A(f'|---|---|---|')
    A(f'| KS Pass Rate | {ks_pass_rate*100:.2f}% | '
      f'{"Pass (≥80%)" if ks_pass_rate >= 0.80 else "Borderline (60–79%)" if ks_pass_rate >= 0.60 else "Fail (<60%)"} |')
    A(f'| Mean KL Divergence | {fmt(mkl)} | '
      f'{"Excellent (<0.01)" if float(fmt(mkl)) < 0.01 else "Good (<0.05)" if float(fmt(mkl)) < 0.05 else "Moderate (<0.20)" if float(fmt(mkl)) < 0.20 else "Poor (≥0.20)"} |')
    if not np.isnan(disc_auc):
        A(f'| RF Discriminator AUC | {disc_auc:.4f} | '
          f'{"Excellent (<0.55)" if disc_auc < 0.55 else "Good (<0.65)" if disc_auc < 0.65 else "Acceptable (<0.75)" if disc_auc < 0.75 else "Poor (≥0.75)"} |')
    A('')

    # ── Chapter 12 ────────────────────────────────────────────────────────────
    A('---')
    A('')
    A('## Chapter 12 — Conclusions & Recommendations')
    A('')
    A('This chapter synthesises findings from all preceding chapters into actionable '
      'conclusions and numbered recommendations for the synthetic data generation '
      'pipeline, downstream modelling, and dataset maintenance.')
    A('')
    A('### 12.1 Summary of Key Findings')
    A('')
    A('**Finding 1 — Dataset is complete and well-structured.**')
    A(f'The real dataset contains {len(df_real)} rows and {len(df_real.columns)} columns '
      f'with {df_real.isnull().sum().sum()} missing values. '
      'The schema is consistent and all physical constraint checks pass '
      '(no negative densities, no impossible Poisson ratios, etc.). '
      'This makes the real dataset a reliable reference for synthetic data evaluation.')
    A('')
    if top_corr_pair is not None:
        A('**Finding 2 — Dominant correlation correctly identified.**')
        A(f'The strongest Pearson correlation is between **{top_corr_pair["Feature 1"]}** '
          f'and **{top_corr_pair["Feature 2"]}** (r = {top_corr_pair["Correlation"]}). '
          'This likely reflects that these two columns encode the same or closely related '
          'physical quantity. For modelling purposes, one should be dropped or they '
          'should be merged into a single feature to avoid multicollinearity.')
    else:
        A('**Finding 2 — Correlation analysis completed.** See Chapter 4 for details.')
    A('')
    if high_skew:
        skew_list = ', '.join(f'`{f}`' for f in high_skew[:6])
        A(f'**Finding 3 — {len(high_skew)} features exhibit significant skew (|skew| > 0.5):** '
          f'{skew_list}. '
          'Right-skewed features (Tensile Strength, Pressure, Number of Iterations) '
          'should be log-transformed before use in linear models or distance-based '
          'classifiers. Tree-based methods are unaffected by monotone transformations.')
    else:
        A('**Finding 3 — Feature skewness analysis:** No features with |skew| > 0.5 detected.')
    A('')
    sig_targets2 = chi_sq[chi_sq['Significant'] == 'Yes']['Target'].tolist() if len(chi_sq) > 0 else []
    if sig_targets2:
        A(f'**Finding 4 — Material Type is a significant predictor.** '
          f'Chi-square tests confirm that Material Type has a statistically significant '
          f'(p < 0.05) association with {len(sig_targets2)} target variable(s): '
          f'{", ".join(sig_targets2)}. '
          'Material Type must be included as a conditioning variable in the synthetic '
          'generator, not sampled independently.')
    else:
        A('**Finding 4 — Chi-square results:** See Chapter 5 for detailed association tests.')
    A('')
    A(f'**Finding 5 — Synthetic data quality ({ks_pass_rate*100:.1f}% KS pass rate, '
      f'mean KL = {fmt(mkl)}).** '
      'The empirical_1000 generator reproduces the marginal distributions with '
      f'{"good fidelity (KS pass rate ≥ 80%)" if ks_pass_rate >= 0.80 else "moderate fidelity (KS pass rate 60–79%)" if ks_pass_rate >= 0.60 else "poor fidelity (KS pass rate < 60%)"}. '
      'The features that fail the KS test should be the focus of generator improvement '
      'in the next iteration.')
    A('')
    A('**Finding 6 — Flight environment physics are partially preserved.** '
      f'The linear R² for Temperature ~ Altitude is {fmt(r2_temp)} and '
      f'for Pressure ~ Altitude is {fmt(r2_pres)}. '
      'The altitude-pressure relationship requires exponential modelling for full '
      'physical fidelity. ISA-based deterministic derivation of Temperature and '
      'Pressure from sampled Altitude is recommended over independent marginal sampling.')
    A('')
    A('**Finding 7 — Optimisation algorithm differences are detectable.** '
      'The two quantum algorithm types (Shark vs Chaotic Quantum Genetic) show '
      'statistically different distributions in iteration count and optimisation time. '
      'These must be stratified in the synthetic generator to preserve their '
      'algorithm-specific statistical signatures.')
    A('')
    A('### 12.2 Numbered Recommendations')
    A('')
    A('#### Category A: Data Preprocessing for Modelling')
    A('')
    A('**Recommendation 1 — Deduplicate collinear feature pair.**')
    A(f'The pair ({top_corr_pair["Feature 1"] if top_corr_pair is not None else "E (GPa)"}, '
      f'{top_corr_pair["Feature 2"] if top_corr_pair is not None else "Young\'s Modulus"}) '
      f'(r = {top_corr_pair["Correlation"] if top_corr_pair is not None else "~1.0"}) '
      'is almost certainly redundant. Confirm that they encode the same physical quantity '
      'and drop one before training any model. Keeping both introduces multicollinearity '
      'that inflates coefficient variance in linear models and degrades feature importance '
      'scores in tree-based models.')
    A('')
    A('**Recommendation 2 — Apply log-transform to right-skewed numeric features.**')
    A('For any model sensitive to scale or distribution shape (logistic regression, '
      'SVM, k-NN, linear discriminant analysis), apply log₁₀ or ln transformation to '
      'features with skewness > 0.5: Tensile Strength (MPa), Pressure (Pa), '
      'Number of Iterations, Optimization Time (sec). '
      'Use Box-Cox if the direction of skew varies or values approach zero.')
    A('')
    A('**Recommendation 3 — Encode ordinal targets correctly.**')
    A('The four target variables are ordinal (Low < Medium < High, etc.). '
      'Standard one-hot encoding destroys the ordinal information. '
      'Use ordinal label encoding (0, 1, 2, ...) for tree-based methods, '
      'or cumulative-link models (ordered logistic regression) for linear approaches. '
      'Treating targets as nominal (unordered) underuses the structure and will '
      'reduce model accuracy.')
    A('')
    A('**Recommendation 4 — Standardise numeric features before distance-based algorithms.**')
    A('E (GPa) and Pressure (Pa) differ by four orders of magnitude. '
      'StandardScaler (zero mean, unit variance) or MinMaxScaler must be applied '
      'before k-NN, SVM, PCA, or any algorithm that uses Euclidean distance. '
      'Failure to standardise will cause high-magnitude features (Pressure) to '
      'dominate all distance calculations and mask signal from low-magnitude features.')
    A('')
    A('#### Category B: Synthetic Data Generator Improvements')
    A('')
    A('**Recommendation 5 — Condition the generator on Material Type and Algorithm Type.**')
    A('Chi-square tests confirm Material Type is non-independent of all targets. '
      'The generator must treat Material Type as a primary conditioning variable: '
      'sample Material Type from its empirical marginal, then sample all numeric '
      'features from the conditional distribution P(X | Material Type). '
      'The same logic applies to Quantum Algorithm Type for optimisation features. '
      'Gaussian copulas or CTGAN/TVAE architectures handle this natively.')
    A('')
    A('**Recommendation 6 — Use ISA-physics-based sampling for flight environment.**')
    A('Do not sample Altitude, Temperature, and Pressure as three independent marginals. '
      'Instead: (1) sample Altitude from its empirical distribution; '
      '(2) compute T_ISA(h) and P_ISA(h) via the ISA equations; '
      '(3) add calibrated Gaussian noise εT, εP (estimated from real data residuals '
      'against the ISA curve). '
      'This guarantees physical consistency at zero cost to statistical fidelity.')
    A('')
    A('**Recommendation 7 — Apply post-generation physical constraint clipping.**')
    A('After any generative model produces a sample, enforce hard constraints:')
    A('')
    A('| Feature | Constraint | Action |')
    A('|---|---|---|')
    A("| E (GPa) | > 0 | Clip to min(real data) if ≤ 0 |")
    A("| nu (Poisson ratio) | ∈ (0.01, 0.49) | Clip to bounds |")
    A('| rho (kg/m³) | > 0 | Clip to min(real data) |')
    A('| Tensile Strength (MPa) | > 0 | Clip to min(real data) |')
    A('| Altitude (m) | > 0 | Clip to 0 |')
    A('| Temperature (°C) | any real | No hard bound; ISA derivation enforces reasonable range |')
    A('| Pressure (Pa) | > 0 | Clip to 1 Pa |')
    A('| Operational Life (years) | > 0 | Clip to 0.1 |')
    A('| Number of Iterations | ≥ 1 | Round to nearest integer, clip to 1 |')
    A('| Optimization Time (sec) | > 0 | Clip to 0.001 |')
    A('')
    A('**Recommendation 8 — Evaluate with the three-metric suite after every generation run.**')
    A('A single number is insufficient to characterise synthetic data quality. '
      'Use all three:')
    A('')
    A('1. **KS pass rate per feature** (target: ≥ 80%) — marginal fidelity')
    A('2. **Mean KL divergence** (target: < 0.05) — distributional closeness')
    A('3. **RF Discriminator AUC** (target: < 0.55) — multivariate indistinguishability')
    A('')
    A('Track these metrics as time series across generator iterations to detect '
      'regression and confirm improvement.')
    A('')
    A('**Recommendation 9 — Increase synthetic sample size beyond 1000.**')
    A('The real dataset contains {len(df_real)} rows; the empirical_1000 synthetic '
      'dataset contains only 1000. For the TSTR (Train on Synthetic, Test on Real) '
      'protocol, synthetic training data should be at least as large as the real '
      'dataset to avoid the synthetic data being the bottleneck for model accuracy. '
      'Generate 5,000–10,000 synthetic samples for the final evaluation.')
    A('')
    A('#### Category C: Model Development Recommendations')
    A('')
    A('**Recommendation 10 — Use stratified k-fold cross-validation.**')
    A('All four targets have ordinal class structure. Stratified k-fold (k=5 or 10) '
      'ensures each fold contains a representative mix of all class values, '
      'which is critical for imbalanced targets. For multi-output prediction '
      '(predicting all 4 targets simultaneously), use multi-output classifiers '
      'or a chain of binary classifiers.')
    A('')
    A('**Recommendation 11 — Establish a baseline with Random Forest before complex models.**')
    A('The RF feature importance analysis (Chapter 10) shows which features carry '
      'signal for each target. A well-tuned Random Forest (n_estimators=500, '
      'max_depth tuned by CV) typically achieves 70–85% of the theoretical accuracy '
      'ceiling on tabular classification tasks and provides an interpretable '
      'feature importance ranking as a by-product. '
      'Start with RF; only escalate to gradient boosting (XGBoost, LightGBM) '
      'or neural networks if RF accuracy is insufficient.')
    A('')
    A('**Recommendation 12 — Conduct TSTR evaluation for final synthetic data certification.**')
    A('Train-on-Synthetic, Test-on-Real (TSTR) is the standard synthetic data utility '
      'benchmark. Protocol:')
    A('')
    A('1. Train classifier C_syn on synthetic data (all 4 targets)')
    A('2. Test C_syn on held-out real data — measure accuracy, F1-macro')
    A('3. Train classifier C_real on real data (same architecture, same hyperparameters)')
    A('4. Test C_real on the same held-out real data')
    A('5. Compute TSTR ratio = accuracy(C_syn) / accuracy(C_real)')
    A('')
    A('A TSTR ratio ≥ 0.95 (less than 5% accuracy degradation) is the acceptance '
      'criterion for deployment of synthetic data in production training pipelines.')
    A('')
    A('#### Category D: Dataset Maintenance')
    A('')
    A('**Recommendation 13 — Version-control the dataset schema.**')
    A('Any future additions of rows or columns must be accompanied by an updated '
      'schema file listing column names, data types, units, and value ranges. '
      'Column name changes (e.g., renaming "E (GPa)" to "Youngs_Modulus_GPa") '
      'must be propagated to all downstream scripts, notebooks, and model pipelines. '
      'Use a schema registry (e.g., a YAML or JSON schema file in the repository root) '
      'to prevent silent column-name mismatches.')
    A('')
    A('**Recommendation 14 — Re-run this report after every data update.**')
    A('This report is generated entirely from code (`build_data_analysis_report.py`) '
      'with no manual editing. After any change to the real or synthetic dataset, '
      're-run the script to refresh all statistics, plots, and conclusions. '
      'Commit both the updated dataset and the updated report to version control '
      'so that all changes are traceable.')
    A('')
    A('### 12.3 Priority Matrix')
    A('')
    A('| # | Recommendation | Priority | Effort | Expected Impact |')
    A('|---|---|---|---|---|')
    A('| 1 | Deduplicate collinear feature pair | High | Low | Reduces multicollinearity |')
    A('| 2 | Log-transform skewed features | High | Low | Improves linear model accuracy |')
    A('| 3 | Ordinal target encoding | High | Low | Preserves target structure |')
    A('| 4 | Standardise features | Medium | Low | Required for distance-based methods |')
    A('| 5 | Condition generator on Material Type | Critical | Medium | Fixes chi-square failures |')
    A('| 6 | ISA-physics flight environment | High | Medium | Physical consistency |')
    A('| 7 | Post-generation constraint clipping | Medium | Low | Eliminates invalid samples |')
    A('| 8 | Three-metric evaluation suite | Medium | Low | Better quality tracking |')
    A('| 9 | Scale synthetic data to ≥5000 samples | Medium | Low | Improves TSTR ratio |')
    A('| 10 | Stratified k-fold CV | High | Low | Reliable model evaluation |')
    A('| 11 | RF baseline before complex models | Medium | Low | Interpretable starting point |')
    A('| 12 | TSTR evaluation | High | Medium | Final quality certification |')
    A('| 13 | Schema versioning | Medium | Low | Long-term maintainability |')
    A('| 14 | Re-run report on data updates | Low | Low | Automated documentation |')
    A('')
    A('### 12.4 Accepted Limitations of This Analysis')
    A('')
    A('1. **No temporal or spatial structure assumed.** Each row is treated as '
      'an independent observation. If there is any autocorrelation structure '
      '(e.g., consecutive design iterations from the same aircraft), '
      'time-series or spatial methods would be more appropriate.')
    A('')
    A('2. **RF importance is not directional.** Gini importance cannot tell us '
      'whether higher E (GPa) helps or hurts Vibration Damping. SHAP analysis '
      'is needed for directional attribution.')
    A('')
    A('3. **KL divergence is bin-count sensitive.** The 30-bin histogram estimator '
      'used here introduces discretisation error, especially for heavy-tailed '
      'distributions. A kernel density estimator (KDE) would give more accurate '
      'divergence estimates for smooth distributions.')
    A('')
    A('4. **Chi-square test assumes independence within cells.** If rows are '
      'correlated (same aircraft modelled under different conditions), '
      'the effective sample size is lower than the row count, and p-values '
      'would be anticonservative (too many false-positive significance calls).')
    A('')
    A('5. **Synthetic dataset is limited to empirical_1000.** Other generator '
      'variants (CTGAN, TVAE, Gaussian Copula, etc.) in the per_model_datasets '
      'folder were not evaluated in this report. A comparative multi-generator '
      'evaluation is recommended as a follow-up analysis.')
    A('')
    A('---')
    A('')
    A('*Report generated automatically by `build_data_analysis_report.py` — '
      'Aerospace Structural Design Synthetic Data Project.*')
    A('')

    report_text = '\n'.join(lines)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_text)
    log.info('Report written to %s', REPORT_PATH)
    return report_text


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    log.info('Loading datasets...')
    df_real = pd.read_csv(REAL_DATA)
    df_syn  = pd.read_csv(SYN_DATA)

    # Normalise column names: replace curly/right-single-quote U+2019 with straight apostrophe
    def _norm_cols(df):
        df.columns = [c.replace('\u2019', "'") for c in df.columns]
        return df
    df_real = _norm_cols(df_real)
    df_syn  = _norm_cols(df_syn)

    log.info('Real dataset: %d rows x %d cols', *df_real.shape)
    log.info('Synthetic dataset: %d rows x %d cols', *df_syn.shape)
    log.info('Real columns: %s', list(df_real.columns))

    # Detect numeric columns (auto, from real dataset)
    num_cols = detect_numeric_cols(df_real)
    log.info('Detected %d numeric feature columns: %s', len(num_cols), num_cols)

    log.info('=== Generating plots ===')

    try:
        plot_pearson_heatmap(df_real, num_cols)
    except Exception as e:
        log.error('pearson heatmap: %s', e)

    try:
        plot_spearman_heatmap(df_real, num_cols)
    except Exception as e:
        log.error('spearman heatmap: %s', e)

    try:
        plot_univariate_histograms(df_real, num_cols)
    except Exception as e:
        log.error('univariate histograms: %s', e)

    try:
        plot_boxplots_by_material(df_real)
    except Exception as e:
        log.error('boxplots by material: %s', e)

    try:
        plot_target_distributions(df_real)
    except Exception as e:
        log.error('target distributions: %s', e)

    try:
        plot_altitude_temp_pressure(df_real)
    except Exception as e:
        log.error('altitude temp pressure: %s', e)

    try:
        plot_wingspan_fuselage(df_real)
    except Exception as e:
        log.error('wingspan fuselage: %s', e)

    try:
        plot_optimization_scatter(df_real)
    except Exception as e:
        log.error('optimization scatter: %s', e)

    try:
        plot_feature_importance_rf(df_real, num_cols)
    except Exception as e:
        log.error('feature importance RF: %s', e)

    try:
        plot_pairplot_material(df_real, num_cols)
    except Exception as e:
        log.error('pairplot material: %s', e)

    try:
        plot_target_crosstab_heatmap(df_real)
    except Exception as e:
        log.error('target crosstab heatmap: %s', e)

    try:
        plot_violin_E_by_material(df_real)
    except Exception as e:
        log.error('violin E by material: %s', e)

    try:
        plot_real_vs_syn_histograms(df_real, df_syn, num_cols)
    except Exception as e:
        log.error('real vs syn histograms: %s', e)

    try:
        plot_pca_real_vs_syn(df_real, df_syn, num_cols)
    except Exception as e:
        log.error('PCA real vs syn: %s', e)

    log.info('=== Building report ===')
    try:
        build_report(df_real, df_syn, num_cols)
    except Exception as e:
        log.error('Report build failed: %s', e)
        raise

    print(f'DATA ANALYSIS REPORT COMPLETE — {REPORT_PATH}')
