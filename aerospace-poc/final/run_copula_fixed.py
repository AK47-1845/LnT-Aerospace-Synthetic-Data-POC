"""
Copula-only re-run with the correct data slice.

Bug in previous run: pre_output["preprocessed"] includes outlier_flag columns
(binary 0/1) which make the 51-dim covariance near-singular even at reg=5.0.

Fix: Use concat(continuous, categorical) only — same filtered slice as CTGAN.
The postprocessor handles the missing outlier_flags automatically.
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

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

import genuity
genuity.activate_license(os.environ.get('GENUITY_LICENSE_KEY', ''))

from genuity.core_generator import CopulaAPI
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor

BASE      = os.path.dirname(os.path.abspath(__file__))
REAL_CSV  = os.path.join(BASE, '..', 'aerospace_structural_design_dataset.csv')
OUT_DIR   = os.path.join(BASE, 'per_model_datasets')
SYN_DIR   = os.path.join(BASE, 'synthetic_data')
PRE_DIR   = os.path.join(BASE, 'models', 'preprocessors')
EXP_CSV   = os.path.join(BASE, 'experiments', 'genuity_experiments.csv')
os.makedirs(PRE_DIR, exist_ok=True)

def load_real():
    df = pd.read_csv(REAL_CSV)
    df.columns = [c.replace('\u2019', "'") for c in df.columns]
    return df

REAL_DF  = load_real()
CAT_COLS = [c for c in REAL_DF.columns if REAL_DF[c].dtype == object]
NUM_COLS = [c for c in REAL_DF.columns if REAL_DF[c].dtype != object]

# ── Evaluation helpers ─────────────────────────────────────────────────────
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
            passed += int(p >= alpha); total += 1
    return passed / total if total else 0.0

def tstr_f1(syn, real):
    feat = [c for c in NUM_COLS if c in syn.columns and c in real.columns]
    scores = []
    for col in CAT_COLS:
        if col not in syn.columns: continue
        try:
            clf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
            clf.fit(syn[feat].fillna(0), LabelEncoder().fit_transform(syn[col].astype(str)))
            le  = LabelEncoder().fit(real[col].astype(str))
            scores.append(f1_score(le.transform(real[col].astype(str)),
                                   clf.predict(real[feat].fillna(0)),
                                   average='macro', zero_division=0))
        except Exception: continue
    return float(np.mean(scores)) if scores else 0.0

def corr_score(syn, real):
    cols = [c for c in NUM_COLS if c in syn.columns and c in real.columns]
    if len(cols) < 2: return 0.0
    try:
        frob = np.linalg.norm(real[cols].corr().fillna(0).values -
                               syn[cols].corr().fillna(0).values, 'fro')
        return max(0.0, 1.0 - frob / len(cols))
    except Exception: return 0.0

def evaluate(syn, name, n, elapsed):
    s, r = align_cols(syn.copy(), REAL_DF.copy())
    ks = ks_pass_rate(s, r)
    ts = tstr_f1(s, r)
    co = corr_score(s, r)
    comp = round(0.40 * ks + 0.35 * ts + 0.25 * co, 4)
    print(f"  KS={ks:.3f}  TSTR={ts:.3f}  Corr={co:.3f}  => Composite={comp:.4f}  [{elapsed:.0f}s]",
          flush=True)
    return dict(run_name=name, model='copula', n_rows=n,
                ks_pass=round(ks,4), tstr_f1=round(ts,4),
                corr_score=round(co,4), composite=comp, elapsed_s=round(elapsed,1))

# ── Copula with filtered data (no outlier_flags) ───────────────────────────
def run_copula(df, n, seed, reg=0.01):
    """
    Critical fix: use concat(continuous, categorical) — NOT pre_output['preprocessed'].
    pre_output['preprocessed'] includes outlier_flag binary columns which make
    the covariance matrix near-singular and cause NaN in sampling.

    Using the same filtered slice as CTGAN ensures a well-conditioned covariance.
    The postprocessor handles the missing outlier_flag columns automatically.
    """
    label = f"copula_s{seed}_n{n}_r{str(reg).replace('.','')}"
    pre_path = os.path.join(PRE_DIR, f"preprocessor_{label}.joblib")

    pre = TabularPreprocessor(random_state=seed, verbose=False, n_pca_components=0)
    out = pre.fit_transform(df)
    pre.save(pre_path)

    # Use only continuous + categorical — excludes outlier_flags
    cont_df = out['continuous']
    cat_df  = out['categorical']
    train   = pd.concat([cont_df, cat_df], axis=1)
    n_cont  = cont_df.shape[1]
    n_total = train.shape[1]
    cont_idx = list(range(n_cont))
    cat_idx  = list(range(n_cont, n_total))
    col_names = list(train.columns)

    # output_info is still needed so Copula knows which cols are categorical
    output_info = TabularPreprocessor.load(pre_path).get_output_info()
    # Adjust output_info indices to match the filtered training data
    # In the filtered slice, cont cols come first (0..n_cont-1), then cat
    # We need to rebuild output_info relative to the filtered slice
    adjusted_info = []
    cat_offset = n_cont  # cats start at n_cont in filtered slice
    cat_col_idx = 0
    for info in output_info:
        nc = info['end_idx'] - info['start_idx']  # num one-hot cols for this feature
        adjusted_info.append({
            'name':           info['name'],
            'num_categories': info['num_categories'],
            'start_idx':      cat_offset + cat_col_idx,
            'end_idx':        cat_offset + cat_col_idx + nc,
        })
        cat_col_idx += nc

    data = train.values.astype(np.float64)

    for try_reg in [reg, 0.5, 1.0, 2.0, 5.0, 10.0]:
        try:
            print(f"  Trying reg={try_reg} on {data.shape[0]}×{data.shape[1]} filtered data...",
                  flush=True)
            model = CopulaAPI()
            model.fit(data=data, continuous_cols=cont_idx, categorical_cols=cat_idx,
                      pretransformed=True, output_info=adjusted_info, regularization=try_reg)
            syn_raw = model.generate(n_samples=n)
            if syn_raw is None or len(syn_raw) == 0:
                raise ValueError("empty output")
            if isinstance(syn_raw, np.ndarray) and np.isnan(syn_raw).any():
                raise ValueError(f"NaN in output (reg={try_reg})")
            print(f"  Copula reg={try_reg} succeeded", flush=True)
            syn_num = pd.DataFrame(syn_raw, columns=col_names)
            post = TabularPostprocessor(preprocessor_path=pre_path, verbose=False)
            return post.inverse_transform_modified_data(syn_num)
        except Exception as e:
            print(f"  reg={try_reg} failed: {e}", flush=True)
    raise RuntimeError("Copula failed at all regularization levels")

# ── Experiments ────────────────────────────────────────────────────────────
EXPERIMENTS = [
    ("copula_s11_n300",       dict(n=300,  seed=11,  reg=0.01)),
    ("copula_s11_n600",       dict(n=600,  seed=11,  reg=0.01)),
    ("copula_s11_n1000",      dict(n=1000, seed=11,  reg=0.01)),
    ("copula_s42_n1000",      dict(n=1000, seed=42,  reg=0.01)),
    ("copula_s42_n1000_r01",  dict(n=1000, seed=42,  reg=0.1)),
    ("copula_s123_n1000",     dict(n=1000, seed=123, reg=0.01)),
]

new_results = []
for label, kwargs in EXPERIMENTS:
    n_rows = kwargs['n']
    print(f"\n{label}", flush=True)
    t0 = time.time()
    try:
        syn_df  = run_copula(REAL_DF.copy(), **kwargs)
        elapsed = time.time() - t0
        if syn_df is None or len(syn_df) == 0:
            raise ValueError("empty output")
        syn_df.to_csv(os.path.join(OUT_DIR, f"{label}.csv"), index=False)
        new_results.append(evaluate(syn_df, label, n_rows, elapsed))
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  FAILED: {e}", flush=True)
        new_results.append(dict(run_name=label, model='copula', n_rows=n_rows,
                                ks_pass=0.0, tstr_f1=0.0, corr_score=0.0,
                                composite=0.0, elapsed_s=round(elapsed,1)))

# ── Merge into main experiments CSV ───────────────────────────────────────
if os.path.exists(EXP_CSV):
    df_old = pd.read_csv(EXP_CSV)
    df_old = df_old[~df_old['run_name'].str.startswith('copula')]
else:
    df_old = pd.DataFrame()

df_merged = pd.concat([df_old, pd.DataFrame(new_results)], ignore_index=True)
df_merged = df_merged.sort_values('composite', ascending=False)
df_merged.to_csv(EXP_CSV, index=False)

# ── Show top 15 ────────────────────────────────────────────────────────────
print("\n" + "="*66)
print("COPULA RESULTS")
print("="*66)
for r in new_results:
    print(f"  {r['composite']:.4f}  {r['run_name']:<40}  "
          f"KS={r['ks_pass']:.3f} TSTR={r['tstr_f1']:.3f} Corr={r['corr_score']:.3f}")

print("\n" + "="*66)
print("UPDATED TOP 15")
print("="*66)
top15 = df_merged.head(15)
manifest = []
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

print("\nDone.")
