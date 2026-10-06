import pandas as pd
import numpy as np
import time
import sys
import os
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, 'd:/aero')
from final.run_all_models_excellence import compute_metrics, load_data, align_columns
from sdv.single_table import CTGANSynthesizer, GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

def run_split_sdv_model(df, n_samples, model_class, epochs=None):
    materials = df["Material Type"].unique()
    syn_dfs = []
    for mat in materials:
        df_mat = df[df["Material Type"] == mat]
        n_mat = int(round(n_samples * len(df_mat) / len(df)))
        if n_mat == 0: continue
        
        meta = SingleTableMetadata()
        meta.detect_from_dataframe(df_mat)
        
        if epochs:
            syn = model_class(metadata=meta, epochs=epochs, verbose=False)
        else:
            syn = model_class(metadata=meta)
            
        syn.fit(df_mat)
        syn_df = syn.sample(n_mat)
        syn_df["Material Type"] = mat
        syn_dfs.append(syn_df)
        
    final_syn = pd.concat(syn_dfs, ignore_index=True).sample(frac=1).reset_index(drop=True)
    if len(final_syn) > n_samples:
        final_syn = final_syn.iloc[:n_samples]
    elif len(final_syn) < n_samples:
        extra = final_syn.sample(n_samples - len(final_syn), replace=True)
        final_syn = pd.concat([final_syn, extra], ignore_index=True)
        
    return final_syn

if __name__ == "__main__":
    df_real = load_data()
    
    t0 = time.time()
    syn_cop = run_split_sdv_model(df_real, 300, GaussianCopulaSynthesizer)
    syn_cop = align_columns(syn_cop, df_real)
    m_cop = compute_metrics(df_real, syn_cop, "SplitCopula_300")
    print(f"Split Copula: Composite={m_cop['composite']:.4f} KS_Pass={m_cop['ks_pass_rate']:.3f} TSTR={m_cop['tstr']:.3f} Time={time.time()-t0:.1f}s")
    
    t0 = time.time()
    syn_ctgan = run_split_sdv_model(df_real, 300, CTGANSynthesizer, epochs=300)
    syn_ctgan = align_columns(syn_ctgan, df_real)
    m_ctgan = compute_metrics(df_real, syn_ctgan, "SplitCTGAN_300")
    print(f"Split CTGAN: Composite={m_ctgan['composite']:.4f} KS_Pass={m_ctgan['ks_pass_rate']:.3f} TSTR={m_ctgan['tstr']:.3f} Time={time.time()-t0:.1f}s")
