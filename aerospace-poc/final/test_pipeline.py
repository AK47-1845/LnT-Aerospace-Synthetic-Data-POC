"""Quick smoke test — runs one experiment of each model type (n=100)."""
import sys, io, os, warnings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

import os as _os
from dotenv import load_dotenv as _ldenv
_ldenv(dotenv_path=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '.env'))

import genuity
_lic = _os.environ.get('GENUITY_LICENSE_KEY', '')
genuity.activate_license(_lic)

from genuity.core_generator import (
    TVAEAPI, TabuDiffBasicAPI, CopulaAPI, MaskedPredictorAPI, CTGANAPI
)
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor

BASE    = os.path.dirname(os.path.abspath(__file__))
PRE_DIR = os.path.join(BASE, 'models', 'preprocessors')
os.makedirs(PRE_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(BASE, '..', 'aerospace_structural_design_dataset.csv'))
df.columns = [c.replace('\u2019', "'") for c in df.columns]
print(f"Loaded {len(df)} rows x {len(df.columns)} cols\n")

def test_model(name, runner):
    try:
        result = runner()
        print(f"  [OK]  {name:25s} -> {len(result)} rows x {len(result.columns)} cols")
        print(f"        columns sample: {list(result.columns)[:4]}")
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")

# ── TabuDiff ────────────────────────────────────────────────────────────────
def test_tabudiff():
    pre = TabularPreprocessor(random_state=42, verbose=False)
    out = pre.fit_transform(df)
    pre.save(os.path.join(PRE_DIR, 'smoke_tabudiff.joblib'))
    X = out["preprocessed"].values
    col_names = list(out["preprocessed"].columns)
    api = TabuDiffBasicAPI()
    api.fit(X)
    syn_matrix = api.generate_dataframe(num_samples=50)
    syn_num = pd.DataFrame(syn_matrix.values, columns=col_names)
    post = TabularPostprocessor(preprocessor_path=os.path.join(PRE_DIR, 'smoke_tabudiff.joblib'),
                                verbose=False)
    return post.inverse_transform_modified_data(syn_num)

test_model("TabuDiff", test_tabudiff)

# ── MaskedPredictor ─────────────────────────────────────────────────────────
def test_masked():
    pre = TabularPreprocessor(random_state=42, verbose=False)
    out = pre.fit_transform(df)
    pre.save(os.path.join(PRE_DIR, 'smoke_masked.joblib'))
    df_num = out["preprocessed"]
    api = MaskedPredictorAPI()
    api.fit(df_num)
    syn_num = api.generate()
    post = TabularPostprocessor(preprocessor_path=os.path.join(PRE_DIR, 'smoke_masked.joblib'),
                                verbose=False)
    return post.inverse_transform_modified_data(syn_num)

test_model("MaskedPredictor", test_masked)

# ── TVAE ────────────────────────────────────────────────────────────────────
def test_tvae():
    pre = TabularPreprocessor(random_state=42, verbose=False)
    out = pre.fit_transform(df)
    pre.save(os.path.join(PRE_DIR, 'smoke_tvae.joblib'))
    df_num = out["preprocessed"]
    col_names = list(df_num.columns)
    api = TVAEAPI()
    api.fit(df_num, epochs=30)
    syn_raw = api.generate(50)
    if not isinstance(syn_raw, pd.DataFrame):
        syn_raw = pd.DataFrame(syn_raw, columns=col_names)
    post = TabularPostprocessor(preprocessor_path=os.path.join(PRE_DIR, 'smoke_tvae.joblib'),
                                verbose=False)
    return post.inverse_transform_modified_data(syn_raw)

test_model("TVAE", test_tvae)

# ── Copula ──────────────────────────────────────────────────────────────────
def test_copula():
    pre = TabularPreprocessor(random_state=42, verbose=False)
    out = pre.fit_transform(df)
    pre.save(os.path.join(PRE_DIR, 'smoke_copula.joblib'))
    X = out["preprocessed"].values
    col_names = list(out["preprocessed"].columns)
    pre2 = TabularPreprocessor.load(os.path.join(PRE_DIR, 'smoke_copula.joblib'))
    output_info = pre2.get_output_info()
    cat_idx = []
    for info in output_info:
        cat_idx.extend(range(info['start_idx'], info['end_idx']))
    cont_idx = [i for i in range(X.shape[1]) if i not in cat_idx]
    model = CopulaAPI()
    model.fit(data=X, continuous_cols=cont_idx, categorical_cols=cat_idx,
              pretransformed=True, output_info=output_info)
    syn_raw = model.generate(n_samples=50)
    syn_num = pd.DataFrame(syn_raw, columns=col_names)
    post = TabularPostprocessor(preprocessor_path=os.path.join(PRE_DIR, 'smoke_copula.joblib'),
                                verbose=False)
    return post.inverse_transform_modified_data(syn_num)

test_model("Copula", test_copula)

# ── CTGAN ───────────────────────────────────────────────────────────────────
def test_ctgan():
    pre = TabularPreprocessor(random_state=42, verbose=False)
    out = pre.fit_transform(df)
    pre.save(os.path.join(PRE_DIR, 'smoke_ctgan.joblib'))
    cont_df = out['continuous']
    cat_df  = out['categorical']
    train   = pd.concat([cont_df, cat_df], axis=1)
    n_cont  = cont_df.shape[1]
    cont_idx = list(range(n_cont))
    cat_idx  = list(range(n_cont, train.shape[1]))
    pre2 = TabularPreprocessor.load(os.path.join(PRE_DIR, 'smoke_ctgan.joblib'))
    output_info = pre2.get_output_info()
    data = train.values.astype(np.float32)
    model = CTGANAPI()
    model.fit(data, continuous_cols=cont_idx, categorical_cols=cat_idx,
              epochs=30, output_info=output_info)
    syn_raw = model.generate(n_samples=50)
    syn_num = pd.DataFrame(syn_raw, columns=list(train.columns))
    post = TabularPostprocessor(preprocessor_path=os.path.join(PRE_DIR, 'smoke_ctgan.joblib'),
                                verbose=False)
    return post.inverse_transform_modified_data(syn_num)

test_model("CTGAN", test_ctgan)

print("\nSmoke test complete.")
