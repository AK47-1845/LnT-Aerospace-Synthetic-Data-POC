import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, entropy
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score, r2_score
from utils import logger
from config import DEFAULT_SCORING
from physics import score_dataset_physics
import traceback

def calc_kl_divergence(real_col, syn_col, bins=20):
    hist_real, bin_edges = np.histogram(real_col.dropna(), bins=bins, density=True)
    hist_syn, _ = np.histogram(syn_col.dropna(), bins=bin_edges, density=True)
    eps = 1e-9
    hist_real = hist_real * np.diff(bin_edges) + eps
    hist_syn = hist_syn * np.diff(bin_edges) + eps
    hist_real /= hist_real.sum()
    hist_syn /= hist_syn.sum()
    return entropy(hist_real, hist_syn)

def get_ml_utility(real_df, syn_df, cat_cols, target_col="Weight Efficiency"):
    try:
        if target_col not in real_df.columns or target_col not in syn_df.columns:
            return 0.5
        r_df = real_df.copy().dropna(subset=[target_col])
        s_df = syn_df.copy().dropna(subset=[target_col])
        if len(r_df) == 0 or len(s_df) == 0: return 0.5
        
        is_class = str(r_df[target_col].dtype) in ['object', 'category', 'bool']
        
        common_cols = [c for c in r_df.columns if c in s_df.columns]
        r_df = r_df[common_cols]
        s_df = s_df[common_cols]
        
        r_merged = pd.concat([r_df.assign(source='real'), s_df.assign(source='synth')])
        cat_present = [c for c in cat_cols if c in r_merged.columns and c != target_col]
        for col in cat_present:
            r_merged[col] = r_merged[col].astype(str)
                
        r_merged = pd.get_dummies(r_merged, columns=cat_present)
        
        real_pr = r_merged[r_merged['source'] == 'real'].drop('source', axis=1)
        syn_pr = r_merged[r_merged['source'] == 'synth'].drop('source', axis=1)
        
        real_pr = real_pr.fillna(method='ffill').fillna(0)
        syn_pr = syn_pr.fillna(method='ffill').fillna(0)
        
        X_real = real_pr.drop(target_col, axis=1)
        y_real = real_pr[target_col]
        X_syn = syn_pr.drop(target_col, axis=1)
        y_syn = syn_pr[target_col]
        
        if is_class:
            model = RandomForestClassifier(n_estimators=50, random_state=42)
            model.fit(X_syn, y_syn)
            y_pred = model.predict(X_real)
            return float(accuracy_score(y_real, y_pred))
        else:
            y_real = pd.to_numeric(y_real, errors='coerce').fillna(0)
            y_syn = pd.to_numeric(y_syn, errors='coerce').fillna(0)
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X_syn, y_syn)
            y_pred = model.predict(X_real)
            return float(np.clip(r2_score(y_real, y_pred), 0, 1))
    except Exception as e:
        logger.warning(f"ML Utility evaluation failed: {e}")
        return 0.5

def evaluate_extended(real_df, syn_df, cat_cols, num_cols):
    metrics = {}
    
    # 1. Physics Score
    phys_score, _, _, _ = score_dataset_physics(real_df, syn_df)
    metrics["physics_consistency"] = phys_score
    
    # 2. Statistical (KS / KL) on numeric
    ks_pvals = []
    kl_divs = []
    
    for col in num_cols:
        try:
            r_drop = pd.to_numeric(real_df[col].dropna(), errors='coerce').dropna().astype(float)
            s_drop = pd.to_numeric(syn_df[col].dropna(), errors='coerce').dropna().astype(float)
            
            if len(r_drop) > 0 and len(s_drop) > 0:
                stat, pval = ks_2samp(r_drop, s_drop)
                ks_pvals.append(pval)
                kl = calc_kl_divergence(r_drop, s_drop)
                kl_divs.append(kl)
        except Exception as e:
            pass
            
    metrics["mean_ks_pval"] = np.mean(ks_pvals) if ks_pvals else 0.0
    metrics["mean_kl_div"] = np.mean(kl_divs) if kl_divs else 0.0
    
    stat_sim = float(np.clip(1.0 - metrics["mean_kl_div"], 0, 1))
    metrics["statistical_similarity"] = stat_sim
    metrics["ml_utility"] = get_ml_utility(real_df, syn_df, cat_cols)
    metrics["privacy_detectability"] = stat_sim # Proxy

    # 4. Correlation preservation
    if len(num_cols) > 1:
        num_real = real_df[num_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
        num_syn = syn_df[num_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
        corr_r = num_real.corr().fillna(0).values
        corr_s = num_syn.corr().fillna(0).values
        diff = np.abs(corr_r - corr_s)
        mean_diff = np.nanmean(diff)
        metrics["correlation_preservation"] = float(np.clip(1.0 - mean_diff, 0, 1))
    else:
        metrics["correlation_preservation"] = 1.0
        
    # Compute composite
    comp_score = 0
    for k, w in DEFAULT_SCORING.items():
        comp_score += float(metrics.get(k, 0.5) * w)
        
    metrics["composite_score"] = float(comp_score)
    
    for k in metrics:
        metrics[k] = float(metrics[k])
        
    return metrics

def bootstrap_significance(real_df, model_a_df, model_b_df, cat_cols, num_cols, n_samples=1000):
    np.random.seed(42)
    diffs = []
    
    row_count = min(len(model_a_df), len(model_b_df))
    model_a_df = model_a_df.sample(row_count)
    model_b_df = model_b_df.sample(row_count)
    
    for _ in range(n_samples):
        idx = np.random.randint(0, row_count, row_count)
        boot_a = model_a_df.iloc[idx]
        boot_b = model_b_df.iloc[idx]
        
        m_a = evaluate_extended(real_df, boot_a, cat_cols, num_cols)
        m_b = evaluate_extended(real_df, boot_b, cat_cols, num_cols)
        
        diffs.append(m_a["composite_score"] - m_b["composite_score"])
        
    diffs = np.array(diffs)
    mean_diff = np.mean(diffs)
    ci_lower = np.percentile(diffs, 2.5)
    ci_upper = np.percentile(diffs, 97.5)
    
    p_val = np.mean(diffs <= 0)
    
    logger.info(f"Significance: diff={mean_diff:.4f}, p={p_val:.4f}, 95% CI=[{ci_lower:.4f}, {ci_upper:.4f}]")
    is_significant = bool(p_val < 0.05)
    
    return {
        "mean_diff": float(mean_diff),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "p_value": float(p_val),
        "is_significant": is_significant
    }
