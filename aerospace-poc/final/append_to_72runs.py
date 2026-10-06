"""
Appends the 31 new Genuity-generated experiments to all_metrics_72runs.csv
using the same metric schema, then removes old corrupted/superseded files
from per_model_datasets/.

all_metrics_72runs.csv schema:
  Model, Seed, Size,
  Physics Consistency, Statistical Similarity, KS p-value (mean),
  KL divergence, ML Utility (TSTR), Privacy / Detection AUC,
  Correlation Matrix Matching density, Composite Score,
  Repair protocol trigger count

Composite formula (verified against existing rows):
  0.30 * StatSim  +  0.25 * TSTR  +  0.15 * Corr
  + 0.20 * Physics  +  0.10 * Privacy
  (where Privacy = StatSim in this file's convention)
"""
import sys, io, os, warnings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score

BASE     = os.path.dirname(os.path.abspath(__file__))
REAL_CSV = os.path.join(BASE, '..', 'aerospace_structural_design_dataset.csv')
PMD      = os.path.join(BASE, 'per_model_datasets')
EXP_72   = os.path.join(BASE, 'experiments', 'all_metrics_72runs.csv')

# ── Load real data ─────────────────────────────────────────────────────────
df_real = pd.read_csv(REAL_CSV)
df_real.columns = [c.replace('\u2019', "'") for c in df_real.columns]

NUM_COLS = [c for c in df_real.columns if df_real[c].dtype != object]
CAT_COLS = [c for c in df_real.columns if df_real[c].dtype == object]

REAL_MIN = df_real[NUM_COLS].min()
REAL_MAX = df_real[NUM_COLS].max()

# ── Metric helpers ─────────────────────────────────────────────────────────
def statistical_similarity(syn):
    """1 - mean(KS_statistic) across numeric features — matches 72runs convention."""
    stats_d = []
    for c in NUM_COLS:
        if c not in syn.columns: continue
        d, _ = stats.ks_2samp(df_real[c].dropna(), syn[c].dropna())
        stats_d.append(d)
    return 1.0 - float(np.mean(stats_d)) if stats_d else 0.0

def ks_pvalue_mean(syn):
    pvals = []
    for c in NUM_COLS:
        if c not in syn.columns: continue
        _, p = stats.ks_2samp(df_real[c].dropna(), syn[c].dropna())
        pvals.append(p)
    return float(np.mean(pvals)) if pvals else 0.0

def tstr_f1(syn):
    feat = [c for c in NUM_COLS if c in syn.columns]
    scores = []
    for col in CAT_COLS:
        if col not in syn.columns: continue
        try:
            X_tr = syn[feat].fillna(0).values
            y_tr = LabelEncoder().fit_transform(syn[col].astype(str))
            X_te = df_real[feat].fillna(0).values
            le   = LabelEncoder().fit(df_real[col].astype(str))
            y_te = le.transform(df_real[col].astype(str))
            clf  = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            clf.fit(X_tr, y_tr)
            scores.append(f1_score(y_te, clf.predict(X_te), average='macro', zero_division=0))
        except Exception:
            continue
    return float(np.mean(scores)) if scores else 0.0

def correlation_density(syn):
    cols = [c for c in NUM_COLS if c in syn.columns]
    if len(cols) < 2: return 0.0
    try:
        frob = np.linalg.norm(
            df_real[cols].corr().fillna(0).values -
            syn[cols].corr().fillna(0).values, 'fro')
        return max(0.0, 1.0 - frob / len(cols))
    except Exception:
        return 0.0

def physics_consistency(syn):
    """Fraction of (row, feature) pairs within real data [min, max] bounds."""
    cols = [c for c in NUM_COLS if c in syn.columns]
    if not cols: return 0.0
    total = passed = 0
    for c in cols:
        in_range = syn[c].between(REAL_MIN[c], REAL_MAX[c])
        passed += in_range.sum()
        total  += len(syn)
    return float(passed / total) if total else 0.0

def compute_row(filepath, model_name, seed, size):
    try:
        syn = pd.read_csv(filepath)
        # Normalise column names
        syn.columns = [c.replace('\u2019', "'") for c in syn.columns]
        # Strip 'Target - ' prefix some models add
        syn.columns = [c[9:] if c.startswith('Target - ') and c[9:] in df_real.columns
                       else c for c in syn.columns]
        # Keep only real columns present in syn
        shared = [c for c in df_real.columns if c in syn.columns]
        if len(shared) < 10:
            print(f"  SKIP {os.path.basename(filepath)}: only {len(shared)} matching cols")
            return None
        syn = syn[shared].head(size)  # cap to declared size
        ss   = statistical_similarity(syn)
        ksp  = ks_pvalue_mean(syn)
        kl   = 1.0 - ss
        tstr = tstr_f1(syn)
        corr = correlation_density(syn)
        phys = physics_consistency(syn)
        comp = round(0.30*ss + 0.25*tstr + 0.15*corr + 0.20*phys + 0.10*ss, 4)
        return {
            'Model':                         model_name,
            'Seed':                          seed,
            'Size':                          size,
            'Physics Consistency':           round(phys, 6),
            'Statistical Similarity':        round(ss,   6),
            'KS p-value (mean)':             round(ksp,  6),
            'KL divergence':                 round(kl,   6),
            'ML Utility (TSTR)':             round(tstr, 6),
            'Privacy / Detection AUC':       round(ss,   6),
            'Correlation Matrix Matching density': round(corr, 6),
            'Composite Score':               comp,
            'Repair protocol trigger count': 0,
        }
    except Exception as e:
        print(f"  ERROR {os.path.basename(filepath)}: {e}")
        return None

# ── File → (model_name, seed, size) map ───────────────────────────────────
# New files produced by run_genuity_experiments.py + run_copula_fixed.py
NEW_FILES = {
    # Copula (Genuity, fixed)
    'copula_s11_n300.csv':          ('Copula',          11,  300),
    'copula_s11_n600.csv':          ('Copula',          11,  600),
    'copula_s11_n1000.csv':         ('Copula',          11, 1000),
    'copula_s42_n1000.csv':         ('Copula',          42, 1000),
    'copula_s42_n1000_r01.csv':     ('Copula',          42, 1000),
    'copula_s123_n1000.csv':        ('Copula',         123, 1000),
    # TabuDiff Basic
    'tabudiff_s11_n300.csv':        ('TabuDiff',        11,  300),
    'tabudiff_s11_n600.csv':        ('TabuDiff',        11,  600),
    'tabudiff_s11_n1000.csv':       ('TabuDiff',        11, 1000),
    'tabudiff_s42_n300.csv':        ('TabuDiff',        42,  300),
    'tabudiff_s42_n600.csv':        ('TabuDiff',        42,  600),
    'tabudiff_s42_n1000.csv':       ('TabuDiff',        42, 1000),
    'tabudiff_s123_n300.csv':       ('TabuDiff',       123,  300),
    'tabudiff_s123_n600.csv':       ('TabuDiff',       123,  600),
    'tabudiff_s123_n1000.csv':      ('TabuDiff',       123, 1000),
    # TabuDiff Premium
    'tabudiff_premium_s11_n1000.csv':  ('TabuDiffPremium', 11,  1000),
    'tabudiff_premium_s42_n1000.csv':  ('TabuDiffPremium', 42,  1000),
    # MaskedPredictor
    'masked_s11_n300.csv':          ('MaskedPredictor', 11,  300),
    'masked_s11_n600.csv':          ('MaskedPredictor', 11,  600),
    'masked_s11_n1000.csv':         ('MaskedPredictor', 11, 1000),
    'masked_s42_n1000.csv':         ('MaskedPredictor', 42, 1000),
    'masked_s123_n1000.csv':        ('MaskedPredictor',123, 1000),
    # TVAE Basic (mode-collapsed but valid experiment record)
    'tvae_s11_n300.csv':            ('TVAE',            11,  300),
    'tvae_s11_n600.csv':            ('TVAE',            11,  600),
    'tvae_s11_n1000.csv':           ('TVAE',            11, 1000),
    'tvae_s42_n1000.csv':           ('TVAE',            42, 1000),
    'tvae_s123_n1000.csv':          ('TVAE',           123, 1000),
    # TVAE Premium
    'tvae_premium_s11_n1000.csv':   ('TVAEPremium',     11, 1000),
    # CTGAN Premium
    'ctgan_premium_s11_n1000.csv':  ('CTGANPremium',    11, 1000),
    'ctgan_premium_s42_n1000.csv':  ('CTGANPremium',    42, 1000),
    'ctgan_premium_s123_n1000.csv': ('CTGANPremium',   123, 1000),
}

# ── OLD files to DELETE (superseded or corrupted) ─────────────────────────
OLD_TO_DELETE = [
    # SDV-based CTGAN (mode collapsed, KS=0)
    'ctgan_300.csv', 'ctgan_600.csv', 'ctgan_1000.csv',
    # Old CTGAN premium (no seed suffix, from run_premium_genuity_models.py)
    'ctgan_premium_300.csv', 'ctgan_premium_600.csv',
    'ctgan_premium_1000.csv', 'ctgan_premium_e1000_1000.csv',
    # SDV TVAE (mode collapsed)
    'tvae_300.csv', 'tvae_600.csv', 'tvae_1000.csv',
    # Old TVAE premium (no seed suffix)
    'tvae_premium_300.csv', 'tvae_premium_600.csv', 'tvae_premium_1000.csv',
    # DP-TVAE (all failed, KS=0)
    'dp_tvae_300.csv', 'dp_tvae_600.csv', 'dp_tvae_1000.csv',
    'dp_tvae_premium_eps0p5_1000.csv', 'dp_tvae_premium_eps1p0_1000.csv',
    'dp_tvae_premium_eps2p0_1000.csv',
    # Old Copula (SDV-based, superseded by Genuity fixed)
    'copula_300.csv', 'copula_600.csv', 'copula_1000.csv',
    # Old TabuDiff (no seed suffix, superseded)
    'tabudiff_300.csv', 'tabudiff_600.csv', 'tabudiff_1000.csv',
    'tabudiff_premium_300.csv', 'tabudiff_premium_600.csv', 'tabudiff_premium_1000.csv',
    # Old MaskedPredictor (duplicate naming)
    'masked_predictor_300.csv', 'masked_predictor_600.csv', 'masked_predictor_1000.csv',
    'maskedpredictor_300.csv', 'maskedpredictor_600.csv', 'maskedpredictor_1000.csv',
]

# ── Compute metrics for all new files ─────────────────────────────────────
print("Computing metrics for new experiments...\n")
new_rows = []
for fname, (model, seed, size) in NEW_FILES.items():
    fpath = os.path.join(PMD, fname)
    if not os.path.exists(fpath):
        print(f"  MISSING: {fname}")
        continue
    print(f"  {fname:<45} model={model} seed={seed} size={size}")
    row = compute_row(fpath, model, seed, size)
    if row:
        new_rows.append(row)
        print(f"    StatSim={row['Statistical Similarity']:.4f}  "
              f"TSTR={row['ML Utility (TSTR)']:.4f}  "
              f"Corr={row['Correlation Matrix Matching density']:.4f}  "
              f"Composite={row['Composite Score']:.4f}")

# ── Append to all_metrics_72runs.csv ──────────────────────────────────────
df_72 = pd.read_csv(EXP_72)
print(f"\nExisting rows: {len(df_72)}")

df_new = pd.DataFrame(new_rows)
df_combined = pd.concat([df_72, df_new], ignore_index=True)
df_combined.to_csv(EXP_72, index=False)
print(f"After append:  {len(df_combined)} rows  (+{len(new_rows)} new)")

# Deletion skipped — user will decide separately which files to remove.

# ── Final summary ──────────────────────────────────────────────────────────
remaining = sorted(os.listdir(PMD))
print(f"\nper_model_datasets/ now has {len(remaining)} files:")
for f in remaining:
    print(f"  {f}")

print(f"\nall_metrics_72runs.csv final row count: {len(df_combined)}")
print("\nTop 10 by Composite Score:")
top = df_combined.sort_values('Composite Score', ascending=False).head(10)
for _, r in top.iterrows():
    print(f"  {r['Composite Score']:.4f}  {r['Model']:<20} seed={r['Seed']}  size={r['Size']}")
