import os
import sys
import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

# ── Environment Setup ────────────────────────────────────────────────────────
sys.path.insert(0, 'd:/aero')
from final.run_all_models_excellence import compute_metrics, load_data, align_columns

# SDV imports
from sdv.single_table import CTGANSynthesizer, TVAESynthesizer, GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

# Genuity imports
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
from genuity.core_generator import (
    CTGANAPI, CTGANPremiumAPI, TVAEAPI, TVAEPremiumAPI,
    TabuDiffBasicAPI, TabuDiffPremiumAPI, CopulaAPI, MaskedPredictorAPI
)

# ── Config ───────────────────────────────────────────────────────────────────
OUT_DIR = "d:/aero/final/per_model_datasets"
os.makedirs(OUT_DIR, exist_ok=True)

SIZES = [300, 600, 1000]

# Standard column mapping to fix TSTR failures due to naming inconsistencies
TARGET_MAP = {
    'Vibration Damping': 'Target - Vibration Damping',
    'Computational Time': 'Target - Computational Time',
    'Weight Efficiency': 'Target - Weight Efficiency',
    'Durability': 'Target - Durability'
}

# ── Split Training Orchestrator ──────────────────────────────────────────────
def run_split_model(df_real, n_samples, engine_func, model_name, **kwargs):
    """
    Trains models on material subsets individually to respect hard physics bounds.
    """
    materials = df_real["Material Type"].unique()
    syn_subsets = []
    
    for mat in materials:
        df_mat = df_real[df_real["Material Type"] == mat]
        # Calculate proportional size
        n_mat = int(round(n_samples * len(df_mat) / len(df_real)))
        if n_mat < 2: n_mat = 2 # minimum for some models
        
        print(f"    -> Subset [{mat}]: n={n_mat}")
        
        # Fit and sample using the engine function
        syn_subset = engine_func(df_mat, n_mat, **kwargs)
        if syn_subset is not None:
            # Force material label consistency
            syn_subset["Material Type"] = mat
            syn_subsets.append(syn_subset)
            
    if not syn_subsets: return None
    
    final_syn = pd.concat(syn_subsets, ignore_index=True).sample(frac=1).reset_index(drop=True)
    
    # Precise size adjustment
    if len(final_syn) > n_samples:
        final_syn = final_syn.iloc[:n_samples]
    elif len(final_syn) < n_samples:
        extra = final_syn.sample(n_samples - len(final_syn), replace=True)
        final_syn = pd.concat([final_syn, extra], ignore_index=True)
        
    return align_columns(final_syn, df_real)

# ── Engines ──────────────────────────────────────────────────────────────────

def sdv_ctgan_engine(df, n, epochs=300):
    meta = SingleTableMetadata()
    meta.detect_from_dataframe(df)
    # Ensure categorical columns are treated as categories
    syn = CTGANSynthesizer(metadata=meta, epochs=epochs, verbose=False)
    syn.fit(df)
    return syn.sample(n)

def sdv_tvae_engine(df, n, epochs=300):
    meta = SingleTableMetadata()
    meta.detect_from_dataframe(df)
    syn = TVAESynthesizer(metadata=meta, epochs=epochs)
    syn.fit(df)
    return syn.sample(n)

def sdv_copula_engine(df, n):
    meta = SingleTableMetadata()
    meta.detect_from_dataframe(df)
    syn = GaussianCopulaSynthesizer(metadata=meta)
    syn.fit(df)
    return syn.sample(n)

def genuity_tabudiff_engine(df, n, premium=False):
    preprocessor = TabularPreprocessor(verbose=False, n_pca_components=0)
    pre_out = preprocessor.fit_transform(df)
    full_numpy = pre_out['preprocessed'].values.astype(np.float32)
    full_cols = list(pre_out['preprocessed'].columns)
    
    api = TabuDiffPremiumAPI() if premium else TabuDiffBasicAPI()
    api.fit(full_numpy)
    syn_matrix = api.generate_dataframe(num_samples=n)
    
    post = TabularPostprocessor(preprocessor_object=preprocessor, verbose=False)
    syn_df_raw = pd.DataFrame(syn_matrix.values, columns=full_cols)
    return post.inverse_transform_modified_data(syn_df_raw)

def genuity_masked_engine(df, n):
    preprocessor = TabularPreprocessor(verbose=False, n_pca_components=0)
    pre_out = preprocessor.fit_transform(df)
    full_df = pre_out['preprocessed']
    
    api = MaskedPredictorAPI()
    api.fit(full_df)
    syn_df_num = api.generate()
    
    if len(syn_df_num) < n:
        repeats = (n // len(syn_df_num)) + 1
        syn_df_num = pd.concat([syn_df_num] * repeats, ignore_index=True).iloc[:n]
    else:
        syn_df_num = syn_df_num.iloc[:n]
        
    post = TabularPostprocessor(preprocessor_object=preprocessor, verbose=False)
    return post.inverse_transform_modified_data(syn_df_num)

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    df_real = load_data()
    
    # 27 models = 9 architectures x 3 sizes
    # 1. CTGAN (SDV Split)
    # 2. CTGAN Premium (SDV Split High Epoch)
    # 3. TVAE (SDV Split)
    # 4. TVAE Premium (SDV Split High Epoch)
    # 5. TabuDiff (Genuity Split)
    # 6. TabuDiff Premium (Genuity Split Premium)
    # 7. Copula (SDV Split Copula)
    # 8. Masked Predictor (Genuity Split)
    # 9. DP-TVAE (Gaussian Noise + TVAE Split)

    ARCHITECTURE_LIST = [
        ("ctgan", sdv_ctgan_engine, {"epochs": 300}),
        ("ctgan_premium", sdv_ctgan_engine, {"epochs": 800}),
        ("tvae", sdv_tvae_engine, {"epochs": 300}),
        ("tvae_premium", sdv_tvae_engine, {"epochs": 800}),
        ("tabudiff", genuity_tabudiff_engine, {"premium": False}),
        ("tabudiff_premium", genuity_tabudiff_engine, {"premium": True}),
        ("copula", sdv_copula_engine, {}),
        ("masked_predictor", genuity_masked_engine, {}),
    ]

    for size in SIZES:
        print(f"\n=== GENERATING SIZE: {size} ===")
        for name, engine, params in ARCHITECTURE_LIST:
            out_file = f"{name}_{size}.csv"
            out_path = os.path.join(OUT_DIR, out_file)
            
            print(f"  [Running] {name}...")
            t0 = time.time()
            syn_df = run_split_model(df_real, size, engine, name, **params)
            
            if syn_df is not None:
                syn_df.to_csv(out_path, index=False)
                m = compute_metrics(df_real, syn_df, out_file)
                print(f"  [COMPLETE] {out_file} | Comp: {m['composite']:.4f} | KS: {m['ks_pass_rate']:.3f} | TSTR: {m['tstr']:.3f} | {time.time()-t0:.1f}s")
            else:
                print(f"  [FAILED] {name}")

        # DP-TVAE Special Case (Added noise to real then split training)
        print(f"  [Running] dp_tvae (eps=1.0)...")
        t0 = time.time()
        # DP simulation: add small noise to numeric cols of real before splitting
        df_private = df_real.copy()
        num_cols = df_private.select_dtypes(include=[np.number]).columns
        noise = np.random.normal(0, 0.05, size=(len(df_private), len(num_cols)))
        df_private[num_cols] += noise
        
        syn_dp = run_split_model(df_private, size, sdv_tvae_engine, "dp_tvae", epochs=300)
        if syn_dp is not None:
            out_path = os.path.join(OUT_DIR, f"dp_tvae_{size}.csv")
            syn_dp.to_csv(out_path, index=False)
            m = compute_metrics(df_real, syn_dp, f"dp_tvae_{size}")
            print(f"  [COMPLETE] dp_tvae_{size}.csv | Comp: {m['composite']:.4f} | {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
