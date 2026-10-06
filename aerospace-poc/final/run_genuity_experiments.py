"""
Genuity Experiments — Full pipeline using TabularPreprocessor/PostProcessor
with save() / load() per DOCUMENTATION.md.

Pipeline for every model:
  1. TabularPreprocessor.fit_transform(df) → save("preprocessor.joblib")
  2. Extract correct slice for each model, train, generate
  3. TabularPostprocessor(preprocessor_path="preprocessor.joblib")
       .inverse_transform_modified_data(syn_df) → original format

Per-model input rules (DOCUMENTATION.md API table):
  TabuDiff Basic/Premium : pre_output["preprocessed"].values  (numpy)
  MaskedPredictor        : pre_output["preprocessed"]          (DataFrame)
  CTGAN / CTGANPremium   : concat(continuous, categorical)     (numpy float32 + INDICES)
  Copula                 : pre_output["preprocessed"].values   (numpy + INDICES from output_info)
  TVAE / TVAEPremium     : pre_output["preprocessed"]          (DataFrame — bypasses internal MinMaxScaler)
"""
import sys, io, os, warnings, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score

import os as _os
from dotenv import load_dotenv as _ldenv
_ldenv(dotenv_path=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '.env'))

import genuity
_lic = _os.environ.get('GENUITY_LICENSE_KEY', '')
genuity.activate_license(_lic)

from genuity.core_generator import (
    TVAEAPI, TVAEPremiumAPI,
    TabuDiffBasicAPI, TabuDiffPremiumAPI,
    CTGANAPI, CTGANPremiumAPI,
    CopulaAPI,
    MaskedPredictorAPI,
)
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor

# ── Paths ──────────────────────────────────────────────────────────────────
BASE         = os.path.dirname(os.path.abspath(__file__))
REAL_CSV     = os.path.join(BASE, '..', 'aerospace_structural_design_dataset.csv')
OUT_DIR      = os.path.join(BASE, 'per_model_datasets')
SYN_DIR      = os.path.join(BASE, 'synthetic_data')
PRE_DIR      = os.path.join(BASE, 'models', 'preprocessors')
EXP_CSV      = os.path.join(BASE, 'experiments', 'genuity_experiments.csv')
for d in [OUT_DIR, SYN_DIR, PRE_DIR]:
    os.makedirs(d, exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────
def load_real():
    df = pd.read_csv(REAL_CSV)
    df.columns = [c.replace('\u2019', "'") for c in df.columns]
    return df

REAL_DF  = load_real()
CAT_COLS = [c for c in REAL_DF.columns if REAL_DF[c].dtype == object]
NUM_COLS = [c for c in REAL_DF.columns if REAL_DF[c].dtype != object]
print(f"Real: {len(REAL_DF)} rows x {len(REAL_DF.columns)} cols | "
      f"{len(NUM_COLS)} numeric, {len(CAT_COLS)} categorical", flush=True)

# ── Preprocessing helpers ──────────────────────────────────────────────────
def preprocess_and_save(df, run_label, seed=42):
    """
    Fit TabularPreprocessor, save to disk, return (pre_output_dict, joblib_path).
    Using save() so postprocessor can load from path (cleaner, avoids object state issues).
    """
    pre_path = os.path.join(PRE_DIR, f"preprocessor_{run_label}.joblib")
    pre = TabularPreprocessor(random_state=seed, verbose=False, n_pca_components=0)
    out = pre.fit_transform(df)
    pre.save(pre_path)                   # <- TabularPreprocessor.save()
    return out, pre_path

def postprocess(syn_numeric_df, pre_path):
    """
    Reconstruct original format using saved preprocessor path.
    Uses TabularPostprocessor(preprocessor_path=...) pattern from docs.
    """
    post = TabularPostprocessor(preprocessor_path=pre_path, verbose=False)
    return post.inverse_transform_modified_data(syn_numeric_df)

# ── Evaluation ─────────────────────────────────────────────────────────────
def align_cols(syn, real):
    rename = {c: c[9:] for c in syn.columns
              if c.startswith('Target - ') and c[9:] in real.columns}
    syn = syn.rename(columns=rename)
    shared = [c for c in real.columns if c in syn.columns]
    return syn[shared], real[shared]

def ks_pass_rate(syn, real, alpha=0.05):
    passed = total = 0
    for c in NUM_COLS:
        if c in syn.columns and c in real.columns:
            _, p = stats.ks_2samp(real[c].dropna().values, syn[c].dropna().values)
            passed += int(p >= alpha)
            total  += 1
    return passed / total if total else 0.0

def tstr_f1(syn, real):
    feat   = [c for c in NUM_COLS if c in syn.columns and c in real.columns]
    scores = []
    if len(feat) < 3:
        return 0.0
    for col in CAT_COLS:
        if col not in syn.columns:
            continue
        try:
            X_tr = syn[feat].fillna(0).values
            y_tr = LabelEncoder().fit_transform(syn[col].astype(str))
            X_te = real[feat].fillna(0).values
            le   = LabelEncoder().fit(real[col].astype(str))
            y_te = le.transform(real[col].astype(str))
            clf  = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
            clf.fit(X_tr, y_tr)
            scores.append(f1_score(y_te, clf.predict(X_te), average='macro',
                                   zero_division=0))
        except Exception:
            continue
    return float(np.mean(scores)) if scores else 0.0

def corr_score(syn, real):
    cols = [c for c in NUM_COLS if c in syn.columns and c in real.columns]
    if len(cols) < 2:
        return 0.0
    try:
        frob = np.linalg.norm(real[cols].corr().fillna(0).values -
                               syn[cols].corr().fillna(0).values, 'fro')
        return max(0.0, 1.0 - frob / len(cols))
    except Exception:
        return 0.0

def evaluate(syn, name, model, n, elapsed):
    s, r = align_cols(syn.copy(), REAL_DF.copy())
    ks   = ks_pass_rate(s, r)
    ts   = tstr_f1(s, r)
    co   = corr_score(s, r)
    comp = round(0.40 * ks + 0.35 * ts + 0.25 * co, 4)
    print(f"  KS={ks:.3f}  TSTR={ts:.3f}  Corr={co:.3f}  => Composite={comp:.4f}  [{elapsed:.0f}s]",
          flush=True)
    return dict(run_name=name, model=model, n_rows=n,
                ks_pass=round(ks,4), tstr_f1=round(ts,4),
                corr_score=round(co,4), composite=comp, elapsed_s=round(elapsed,1))

# ── Model runners ──────────────────────────────────────────────────────────

def run_tabudiff(df, n, seed, premium=False):
    """
    TabuDiff workflow:
      preprocess → X = pre_output["preprocessed"].values (numpy)
      → TabuDiffBasicAPI.fit(X)
      → generate_dataframe(n) → DataFrame with preprocessed cols
      → postprocess(pre_path)
    """
    label = f"td_{'p' if premium else 'b'}_s{seed}"
    out, pre_path = preprocess_and_save(df, label, seed)
    X         = out["preprocessed"].values
    col_names = list(out["preprocessed"].columns)
    api = TabuDiffPremiumAPI() if premium else TabuDiffBasicAPI()
    api.fit(X)
    syn_matrix = api.generate_dataframe(num_samples=n)
    # Attach preprocessed column names before postprocessing
    syn_num = pd.DataFrame(syn_matrix.values, columns=col_names)
    return postprocess(syn_num, pre_path)


def run_masked_predictor(df, n, seed):
    """
    MaskedPredictor workflow:
      preprocess → df_numeric = pre_output["preprocessed"] (DataFrame)
      → MaskedPredictorAPI.fit(df_numeric)
      → generate() → postprocess(pre_path)
    """
    label = f"mp_s{seed}"
    out, pre_path = preprocess_and_save(df, label, seed)
    df_numeric = out["preprocessed"]
    api = MaskedPredictorAPI()
    api.fit(df_numeric)
    parts, needed = [], n
    while needed > 0:
        chunk = api.generate()
        parts.append(chunk)
        needed -= len(chunk)
    syn_num = pd.concat(parts, ignore_index=True).head(n)
    return postprocess(syn_num, pre_path)


def run_tvae(df, n, seed, epochs=500, premium=False):
    """
    TVAE workflow:
      preprocess with QuantileTransformer (avoids internal MinMaxScaler mode collapse)
      → TVAE.fit(pre_output["preprocessed"])  (DataFrame)
      → generate(n) → postprocess(pre_path)
    """
    label = f"tv_{'p' if premium else 'b'}_s{seed}"
    out, pre_path = preprocess_and_save(df, label, seed)
    df_numeric = out["preprocessed"]
    col_names  = list(df_numeric.columns)
    if premium:
        api = TVAEPremiumAPI(model_type="premium")
        api.fit(df_numeric, epochs=epochs,
                premium_features={"use_vamp_prior": True,
                                   "use_cyclical_annealing": True})
    else:
        api = TVAEAPI()
        api.fit(df_numeric, epochs=epochs)
    syn_raw = api.generate(n)
    if not isinstance(syn_raw, pd.DataFrame):
        syn_raw = pd.DataFrame(syn_raw, columns=col_names)
    return postprocess(syn_raw, pre_path)


def run_copula(df, n, seed, reg=0.01):
    """
    Copula workflow:
      preprocess → X = pre_output["preprocessed"].values (numpy)
      → extract cat_indices from output_info (pretransformed=True)
      → CopulaAPI.fit(X, cont_idx, cat_idx)
      → generate(n) → postprocess(pre_path)
    Falls back to higher regularization values if covariance is ill-conditioned.
    """
    label = f"cop_s{seed}_r{str(reg).replace('.','')}"
    out, pre_path = preprocess_and_save(df, label, seed)
    X           = out["preprocessed"].values
    col_names   = list(out["preprocessed"].columns)
    output_info = TabularPreprocessor.load(pre_path).get_output_info()
    cat_idx = []
    for info in output_info:
        cat_idx.extend(range(info['start_idx'], info['end_idx']))
    cont_idx = [i for i in range(X.shape[1]) if i not in cat_idx]
    # Try increasing regularization until generation succeeds (NaN guard for ill-conditioned covariance)
    for try_reg in [reg, 0.5, 1.0, 2.0, 5.0]:
        try:
            model = CopulaAPI()
            model.fit(data=X, continuous_cols=cont_idx, categorical_cols=cat_idx,
                      pretransformed=True, output_info=output_info, regularization=try_reg)
            syn_raw = model.generate(n_samples=n)
            if syn_raw is None or (hasattr(syn_raw, '__len__') and len(syn_raw) == 0):
                raise ValueError("empty generate output")
            if isinstance(syn_raw, np.ndarray) and np.isnan(syn_raw).any():
                raise ValueError("NaN in generated data")
            print(f"  Copula: reg={try_reg} succeeded", flush=True)
            syn_num = pd.DataFrame(syn_raw, columns=col_names)
            return postprocess(syn_num, pre_path)
        except Exception as e:
            print(f"  Copula reg={try_reg} failed: {e} — trying higher", flush=True)
    raise RuntimeError("Copula failed at all regularization levels")


def run_ctgan(df, n, seed, epochs=600, premium=False):
    """
    CTGAN workflow (CRITICAL — no outlier_flags, no pca):
      preprocess → concat(continuous, categorical) only
      → numpy float32 + INTEGER INDICES
      → CTGANAPI.fit(data, cont_idx, cat_idx, output_info)
      → generate(n) → postprocess(pre_path)
    Note: postprocessor handles the filtered columns automatically.
    """
    label = f"ctgan_{'p' if premium else 'b'}_s{seed}"
    out, pre_path = preprocess_and_save(df, label, seed)
    cont_df = out['continuous']
    cat_df  = out['categorical']
    train   = pd.concat([cont_df, cat_df], axis=1)
    n_cont  = cont_df.shape[1]
    cont_idx = list(range(n_cont))
    cat_idx  = list(range(n_cont, train.shape[1]))
    output_info = TabularPreprocessor.load(pre_path).get_output_info()
    data = train.values.astype(np.float32)
    if premium:
        model = CTGANPremiumAPI(model_type="premium")
        model.fit(data, continuous_cols=cont_idx, categorical_cols=cat_idx,
                  epochs=epochs, output_info=output_info,
                  premium_features={"use_spectral_norm": True,
                                    "use_gradient_penalty": True})
    else:
        model = CTGANAPI()
        model.fit(data, continuous_cols=cont_idx, categorical_cols=cat_idx,
                  epochs=epochs, output_info=output_info)
    syn_raw = model.generate(n_samples=n)
    syn_num = pd.DataFrame(syn_raw, columns=list(train.columns))
    return postprocess(syn_num, pre_path)

# ── Experiment plan ────────────────────────────────────────────────────────
EXPERIMENTS = [
    # TabuDiff — best deep Genuity model
    ("tabudiff_s11_n300",          run_tabudiff,        dict(n=300,  seed=11)),
    ("tabudiff_s11_n600",          run_tabudiff,        dict(n=600,  seed=11)),
    ("tabudiff_s11_n1000",         run_tabudiff,        dict(n=1000, seed=11)),
    ("tabudiff_s42_n300",          run_tabudiff,        dict(n=300,  seed=42)),
    ("tabudiff_s42_n600",          run_tabudiff,        dict(n=600,  seed=42)),
    ("tabudiff_s42_n1000",         run_tabudiff,        dict(n=1000, seed=42)),
    ("tabudiff_s123_n300",         run_tabudiff,        dict(n=300,  seed=123)),
    ("tabudiff_s123_n600",         run_tabudiff,        dict(n=600,  seed=123)),
    ("tabudiff_s123_n1000",        run_tabudiff,        dict(n=1000, seed=123)),
    # TabuDiff Premium
    ("tabudiff_premium_s11_n1000", run_tabudiff,        dict(n=1000, seed=11,  premium=True)),
    ("tabudiff_premium_s42_n1000", run_tabudiff,        dict(n=1000, seed=42,  premium=True)),
    # Copula — strong correlation preservation
    ("copula_s11_n300",            run_copula,          dict(n=300,  seed=11,  reg=0.01)),
    ("copula_s11_n600",            run_copula,          dict(n=600,  seed=11,  reg=0.01)),
    ("copula_s11_n1000",           run_copula,          dict(n=1000, seed=11,  reg=0.01)),
    ("copula_s42_n1000",           run_copula,          dict(n=1000, seed=42,  reg=0.01)),
    ("copula_s42_n1000_r01",       run_copula,          dict(n=1000, seed=42,  reg=0.1)),
    ("copula_s123_n1000",          run_copula,          dict(n=1000, seed=123, reg=0.01)),
    # TVAE (preprocessed input bypasses MinMaxScaler collapse)
    ("tvae_s11_n300",              run_tvae,            dict(n=300,  seed=11,  epochs=500)),
    ("tvae_s11_n600",              run_tvae,            dict(n=600,  seed=11,  epochs=500)),
    ("tvae_s11_n1000",             run_tvae,            dict(n=1000, seed=11,  epochs=500)),
    ("tvae_s42_n1000",             run_tvae,            dict(n=1000, seed=42,  epochs=500)),
    ("tvae_s123_n1000",            run_tvae,            dict(n=1000, seed=123, epochs=500)),
    # TVAE Premium
    ("tvae_premium_s11_n1000",     run_tvae,            dict(n=1000, seed=11,  epochs=400, premium=True)),
    # MaskedPredictor
    ("masked_s11_n300",            run_masked_predictor,dict(n=300,  seed=11)),
    ("masked_s11_n600",            run_masked_predictor,dict(n=600,  seed=11)),
    ("masked_s11_n1000",           run_masked_predictor,dict(n=1000, seed=11)),
    ("masked_s42_n1000",           run_masked_predictor,dict(n=1000, seed=42)),
    ("masked_s123_n1000",          run_masked_predictor,dict(n=1000, seed=123)),
    # CTGAN Premium
    ("ctgan_premium_s11_n1000",    run_ctgan,           dict(n=1000, seed=11,  epochs=600, premium=True)),
    ("ctgan_premium_s42_n1000",    run_ctgan,           dict(n=1000, seed=42,  epochs=600, premium=True)),
    ("ctgan_premium_s123_n1000",   run_ctgan,           dict(n=1000, seed=123, epochs=600, premium=True)),
]

# ── Run all experiments ────────────────────────────────────────────────────
results = []
TOTAL   = len(EXPERIMENTS)

for i, (label, fn, kwargs) in enumerate(EXPERIMENTS):
    model_tag = label.split('_')[0] + ('_premium' if 'premium' in label else '')
    n_rows    = kwargs.get('n', 1000)
    print(f"\n[{i+1}/{TOTAL}] {label}", flush=True)
    t0 = time.time()
    try:
        syn_df  = fn(REAL_DF.copy(), **kwargs)
        elapsed = time.time() - t0
        if syn_df is None or len(syn_df) == 0:
            raise ValueError("empty output")
        syn_df.to_csv(os.path.join(OUT_DIR, f"{label}.csv"), index=False)
        results.append(evaluate(syn_df, label, model_tag, n_rows, elapsed))
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  FAILED: {e}", flush=True)
        results.append(dict(run_name=label, model=model_tag, n_rows=n_rows,
                            ks_pass=0.0, tstr_f1=0.0, corr_score=0.0,
                            composite=0.0, elapsed_s=round(elapsed,1)))

# ── Save results & pick top 15 ─────────────────────────────────────────────
df_res = pd.DataFrame(results).sort_values('composite', ascending=False)
df_res.to_csv(EXP_CSV, index=False)

print("\n" + "="*66)
print("ALL RESULTS")
print("="*66)
for _, r in df_res.iterrows():
    print(f"  {r['composite']:.4f}  {r['run_name']:<40}  "
          f"KS={r['ks_pass']:.3f} TSTR={r['tstr_f1']:.3f} Corr={r['corr_score']:.3f}")

top15 = df_res.head(15)
manifest = []
print("\n" + "="*66)
print("TOP 15  ->  synthetic_data/")
print("="*66)
for rank, (_, row) in enumerate(top15.iterrows(), 1):
    src = os.path.join(OUT_DIR, f"{row['run_name']}.csv")
    dst = os.path.join(SYN_DIR, f"top{rank:02d}_{row['run_name']}.csv")
    if os.path.exists(src):
        pd.read_csv(src).to_csv(dst, index=False)
    manifest.append(dict(rank=rank, file=os.path.basename(dst),
                         composite=row['composite'], model=row['model'],
                         n_rows=row['n_rows']))
    print(f"  #{rank:2d}  {row['composite']:.4f}  {row['run_name']}")

with open(os.path.join(BASE, 'experiments', 'top15_manifest.json'), 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"\nResults saved: {EXP_CSV}")
print("Done.")
