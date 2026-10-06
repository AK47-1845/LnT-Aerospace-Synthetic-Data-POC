import os
import sys
import pandas as pd
import numpy as np
import time

sys.path.insert(0, 'd:/aero')
from final.run_all_models_excellence import compute_metrics, load_data, align_columns

# Thresholds for acceptance
TARGET_KPI = {
    'ctgan': {'ks': 0.70, 'composite': 0.70},
    'tvae': {'ks': 0.70, 'composite': 0.70},
    'copula': {'ks': 0.85, 'composite': 0.75},
    'tabudiff': {'ks': 0.60, 'composite': 0.65},
    'masked_predictor': {'ks': 0.50, 'composite': 0.55},
    'dp_tvae': {'ks': 0.60, 'composite': 0.60}
}

def analyze_datasets():
    df_real = load_data()
    out_dir = "d:/aero/final/per_model_datasets"
    
    results = []
    
    print("\n--- ANALYZING EXISTING DATASETS ---")
    for file in os.listdir(out_dir):
        if not file.endswith('.csv'): continue
        if 'empirical' in file: continue # user explicitly asked to drop empirical
        path = os.path.join(out_dir, file)
        df_syn = pd.read_csv(path)
        
        # determine model tier for target mapping
        model_base = None
        for key in TARGET_KPI:
            if key in file.lower() or key.replace('_', '') in file.lower():
                model_base = key
                break
        
        if not model_base:
            model_base = 'masked_predictor' # default lowest bar
            
        m = compute_metrics(df_real, df_syn, file.replace('.csv', ''))
        
        target = TARGET_KPI[model_base]
        passed = (m['composite'] >= target['composite']) and (m['ks_pass_rate'] >= target['ks'])
        status = "PASSED" if passed else "FAILED"
        
        results.append({
            'file': file,
            'model': file.split('_')[0] if not 'premium' in file else file.split('_')[0] + '_premium',
            'size': len(df_syn),
            'composite': m['composite'],
            'ks': m['ks_pass_rate'],
            'tstr': m['tstr'],
            'target_composite': target['composite'],
            'passed': passed
        })
        print(f"{status:6s} | {file:30s} | Comp: {m['composite']:.3f} (Req: {target['composite']:.2f}) | KS: {m['ks_pass_rate']:.3f} | TSTR: {m['tstr']:.3f}")
        
    df_res = pd.DataFrame(results)
    
    print(f"\n--- ANALYSIS SUMMARY ---")
    print(f"Total Reviewed: {len(df_res)}")
    print(f"Total Passed:   {df_res['passed'].sum()}")
    print(f"Total Failed:   {len(df_res) - df_res['passed'].sum()}")
    
    if len(df_res) > 0:
        df_res.to_csv("d:/aero/final/experiments/dataset_audit_results.csv", index=False)
        print("Detailed results saved to experiments/dataset_audit_results.csv")

if __name__ == "__main__":
    analyze_datasets()
