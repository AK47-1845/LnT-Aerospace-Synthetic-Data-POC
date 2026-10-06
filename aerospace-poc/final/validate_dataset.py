import pandas as pd
import numpy as np
import os
import json
from scipy.stats import ks_2samp, entropy, chisquare
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
from sklearn.metrics import accuracy_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_dataset(real_path, syn_path, report_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Loading real: {real_path}")
    real_df = pd.read_csv(real_path)
    print(f"Loading synthetic: {syn_path}")
    syn_df = pd.read_csv(syn_path)
    
    targets = ["Vibration Damping", "Computational Time", "Weight Efficiency", "Durability"]
    num_cols = real_df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = real_df.select_dtypes(exclude=[np.number]).columns.tolist()
    features = [c for c in real_df.columns if c not in targets]
    
    report = [f"# Validation Report: {os.path.basename(syn_path)}", ""]
    
    # ---------------------------------------------------------
    # TIER 1: MINIMUM BAR
    # ---------------------------------------------------------
    report.append("## Tier 1: Minimum Bar")
    
    # 1. Schema
    schema_pass = (list(real_df.columns) == list(syn_df.columns))
    report.append(f"- **Schema Match:** {'✅ Pass' if schema_pass else '❌ Fail'}")
    
    # 2. Nulls
    nulls = syn_df.isnull().sum().sum()
    report.append(f"- **Null Check:** {'✅ Pass' if nulls == 0 else f'❌ Fail ({nulls} nulls found)'}")
    
    # 3. Ranges
    range_failures = []
    for c in num_cols:
        r_min, r_max = real_df[c].min(), real_df[c].max()
        s_min, s_max = syn_df[c].min(), syn_df[c].max()
        if s_min < r_min - 1e-4 or s_max > r_max + 1e-4: # slight float tolerance
            range_failures.append(f"{c} (Expected {r_min:.2f} to {r_max:.2f}, got {s_min:.2f} to {s_max:.2f})")
    
    if not range_failures:
        report.append("- **Numeric Range Check:** ✅ Pass")
    else:
        report.append("- **Numeric Range Check:** ❌ Fail")
        for f in range_failures:
            report.append(f"  - {f}")
            
    # 4. Categoricals
    cat_failures = []
    for c in cat_cols:
        r_levels = set(real_df[c].unique())
        s_levels = set(syn_df[c].unique())
        if not s_levels.issubset(r_levels):
            cat_failures.append(f"{c} (Expected {r_levels}, got {s_levels})")
            
    if not cat_failures:
        report.append("- **Categorical Level Check:** ✅ Pass")
    else:
        report.append("- **Categorical Level Check:** ❌ Fail")
        for f in cat_failures:
            report.append(f"  - {f}")
            
    # 5. Row Count
    rows = len(syn_df)
    report.append(f"- **Row Count:** {'✅ Pass' if rows >= 300 else '❌ Fail'} ({rows} rows)")
    
    report.append("")
    
    # ---------------------------------------------------------
    # TIER 2: DEEPER VALIDATIONS
    # ---------------------------------------------------------
    report.append("## Tier 2: Academic Validations")
    
    # TSTR
    report.append("### 1. ML Utility (Train-on-Synthetic, Test-on-Real)")
    
    def encode_df(df):
        enc = df.copy()
        for c in cat_cols:
            enc[c] = LabelEncoder().fit_transform(enc[c].astype(str))
        return enc
        
    r_enc = encode_df(real_df)
    s_enc = encode_df(syn_df)
    
    tstr_scores = {}
    for t in targets:
        rf = RandomForestClassifier(n_estimators=50, random_state=42)
        rf.fit(s_enc[features], s_enc[t])
        preds = rf.predict(r_enc[features])
        acc = accuracy_score(r_enc[t], preds)
        tstr_scores[t] = acc
        report.append(f"- **{t}:** {acc:.4f} accuracy")
        
    # Feature Importance Alignment
    report.append("\n### 2. Feature Importance Alignment")
    report.append("Measures if the generative model learned the same physical rules governing the targets.")
    
    imp_diffs = []
    for t in targets:
        rf_real = RandomForestClassifier(n_estimators=50, random_state=42).fit(r_enc[features], r_enc[t])
        rf_syn = RandomForestClassifier(n_estimators=50, random_state=42).fit(s_enc[features], s_enc[t])
        
        real_imp = rf_real.feature_importances_
        syn_imp = rf_syn.feature_importances_
        
        mae = np.mean(np.abs(real_imp - syn_imp))
        imp_diffs.append(mae)
        report.append(f"- **{t} MAE:** {mae:.4f}")
        
    # Statistical Fidelity (KS/KL)
    report.append("\n### 3. Statistical Fidelity (KS & KL)")
    ks_p_vals = []
    
    for c in num_cols:
        r_val = real_df[c].dropna()
        s_val = syn_df[c].dropna()
        stat, pval = ks_2samp(r_val, s_val)
        ks_p_vals.append(pval)
        
    mean_pval = np.mean(ks_p_vals)
    report.append(f"- **Mean KS p-value:** {mean_pval:.4f} (Higher is better, >0.05 fails to reject null hypothesis)")
    
    # Rare Case Realism
    report.append("\n### 4. Rare Case Realism (Isolation Forest)")
    iso = IsolationForest(contamination=0.05, random_state=42)
    # Train IF on real numeric data
    r_num = real_df[num_cols].fillna(0)
    iso.fit(r_num)
    
    # Predict on synthetic
    s_num = syn_df[num_cols].fillna(0)
    s_preds = iso.predict(s_num)
    syn_anomalies = np.sum(s_preds == -1)
    syn_anomaly_rate = syn_anomalies / len(syn_df)
    report.append(f"- **Synthetic Anomaly Rate:** {syn_anomaly_rate:.2%} (Expected ~5%)")
    
    if syn_anomaly_rate > 0:
        syn_anom_pts = s_num.iloc[s_preds == -1]
        real_anom_pts = r_num.iloc[iso.predict(r_num) == -1]
        if len(real_anom_pts) > 0:
            nn = NearestNeighbors(n_neighbors=1).fit(real_anom_pts)
            distances, _ = nn.kneighbors(syn_anom_pts)
            mean_dist = np.mean(distances)
            report.append(f"- **Mean distance to real anomalies:** {mean_dist:.4f}")
            
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Validation complete. Report saved to {report_path}")
    
    # Generate some comparative graphs
    model_name = os.path.basename(syn_path).split('_')[0]
    out_prefix = f"{out_dir}/{model_name}"
    
    # Target Class Distribution
    fig, axes = plt.subplots(1, 4, figsize=(20, 4))
    for i, t in enumerate(targets):
        r_counts = real_df[t].value_counts(normalize=True).sort_index()
        s_counts = syn_df[t].value_counts(normalize=True).sort_index()
        
        idx = r_counts.index
        x = np.arange(len(idx))
        width = 0.35
        
        axes[i].bar(x - width/2, [r_counts.get(k, 0) for k in idx], width, label='Real')
        axes[i].bar(x + width/2, [s_counts.get(k, 0) for k in idx], width, label='Synthetic')
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(idx, rotation=45)
        axes[i].set_title(t)
        if i == 0: axes[i].legend()
        
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_class_balance.png")
    plt.close()
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        evaluate_dataset(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
