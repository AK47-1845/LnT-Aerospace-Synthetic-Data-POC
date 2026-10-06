"""
run_sdv_models.py
=================
Replace failed Genuity CTGAN/TVAE with SDV versions.
SDV uses BGM (Bayesian Gaussian Mixture) normalization per column —
correctly handles the tri-modal E (GPa) distribution caused by 3 material types.
Also runs DP-TVAE (DP + SDV TVAE) and improved TabuDiff/MaskedPredictor.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, 'd:/aero')

import os, warnings, time
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score

# SDV
from sdv.single_table import CTGANSynthesizer, TVAESynthesizer, GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

# Genuity for TabuDiff and DP-TVAE
from genuity.compliance import check_compliance_and_pii
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
from genuity.core_generator import (
    TabuDiffBasicAPI, TabuDiffPremiumAPI,
    MaskedPredictorAPI,
    DifferentialPrivacyProcessor, TVAEAPI
)

DATA_PATH = "d:/aero/aerospace_structural_design_dataset.csv"
OUT_DIR   = "d:/aero/final/per_model_datasets"
EXP_DIR   = "d:/aero/final/experiments"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.replace('\u2019', "'").replace('\u2018', "'") for c in df.columns]
    # Standardize target column names
    rename = {}
    for c in df.columns:
        if 'Vibration' in c:     rename[c] = 'Vibration Damping'
        elif 'Computational' in c: rename[c] = 'Computational Time'
        elif 'Weight' in c and ('Eff' in c or 'eff' in c): rename[c] = 'Weight Efficiency'
        elif 'Durability' in c:  rename[c] = 'Durability'
    df = df.rename(columns=rename)
    df = df.dropna()
    print(f"[DATA] {df.shape[0]} rows × {df.shape[1]} cols")
    print(f"[COLS] {list(df.columns)}")
    return df

# ── Evaluation ────────────────────────────────────────────────────────────────
def evaluate(real, syn, name):
    if syn is None or len(syn) == 0:
        print(f"  [{name}] FAILED — empty")
        return {"name": name, "ks": 0, "tstr": 0, "composite": 0}

    num = [c for c in real.select_dtypes(include=[np.number]).columns if c in syn.columns]
    ks_pass = []
    for col in num:
        rc = real[col].dropna().values
        sc = syn[col].dropna().values
        if len(sc) > 5:
            _, p = stats.ks_2samp(rc, sc)
            ks_pass.append(p > 0.05)
    ks_rate = float(np.mean(ks_pass)) if ks_pass else 0

    # TSTR
    target = next((c for c in syn.columns if 'Weight' in c and 'Eff' in c), None)
    if target is None:
        target = next((c for c in ['Vibration Damping', 'Durability', 'Computational Time'] if c in syn.columns), None)
    tstr = 0
    if target and target in real.columns:
        feat = [c for c in num if c in real.columns]
        try:
            le = LabelEncoder()
            all_y = list(real[target].astype(str)) + list(syn[target].astype(str))
            le.fit(all_y)
            y_syn = le.transform(syn[target].astype(str))
            y_real = le.transform(real[target].astype(str))
            X_syn = syn[feat].fillna(0).values
            X_real = real[feat].fillna(0).values
            clf = RandomForestClassifier(100, random_state=42, n_jobs=-1)
            clf.fit(X_syn, y_syn)
            tstr = float(f1_score(y_real, clf.predict(X_real), average='macro', zero_division=0))
        except Exception as e:
            print(f"    TSTR error: {e}")

    # Correlation score
    try:
        rc_df = real[[c for c in num if c in real.columns]].fillna(0)
        sc_df = syn[[c for c in num if c in syn.columns]].fillna(0)
        shared = [c for c in rc_df.columns if c in sc_df.columns]
        if len(shared) >= 2:
            frob = float(np.linalg.norm(rc_df[shared].corr().values - sc_df[shared].corr().values, 'fro'))
            corr = max(0, 1 - frob / 10)
        else:
            corr = 0.5
    except:
        corr = 0.5

    stat_sim = max(0, ks_rate * 0.8 + corr * 0.2)
    composite = round(0.30 * stat_sim + 0.25 * tstr + 0.20 * corr + 0.15 * ks_rate + 0.10 * stat_sim, 4)

    print(f"  [{name}] rows={len(syn)} ks={ks_rate:.3f} tstr={tstr:.3f} composite={composite:.4f}")
    return {"name": name, "ks": round(ks_rate,3), "tstr": round(tstr,3), "composite": composite,
            "corr": round(corr,3)}

# ── SDV helpers ───────────────────────────────────────────────────────────────
def sdv_meta(df):
    m = SingleTableMetadata()
    m.detect_from_dataframe(df)
    return m

def sdv_ctgan(df, n, epochs=300):
    meta = sdv_meta(df)
    s = CTGANSynthesizer(metadata=meta, epochs=epochs, verbose=False)
    s.fit(df)
    syn = s.sample(n)
    # Ensure column order matches
    shared = [c for c in df.columns if c in syn.columns]
    return syn[shared] if len(shared) == len(df.columns) else syn

def sdv_tvae(df, n, epochs=300):
    meta = sdv_meta(df)
    s = TVAESynthesizer(metadata=meta, epochs=epochs)
    s.fit(df)
    syn = s.sample(n)
    shared = [c for c in df.columns if c in syn.columns]
    return syn[shared] if len(shared) == len(df.columns) else syn

def sdv_copula(df, n):
    meta = sdv_meta(df)
    s = GaussianCopulaSynthesizer(metadata=meta)
    s.fit(df)
    syn = s.sample(n)
    shared = [c for c in df.columns if c in syn.columns]
    return syn[shared] if len(shared) == len(df.columns) else syn

# ── Genuity helpers ───────────────────────────────────────────────────────────
def get_genuity_inputs(df):
    preprocessor = TabularPreprocessor(verbose=False, n_pca_components=0)
    pre = preprocessor.fit_transform(df)
    cont_df = pre['continuous']
    cat_df  = pre['categorical']
    full_df = pre['preprocessed']
    train = pd.concat([cont_df, cat_df], axis=1)
    n_cont = cont_df.shape[1]
    n_cat  = cat_df.shape[1]
    output_info = preprocessor.get_output_info()
    # Copula indices from output_info
    copula_cat = []
    for info in output_info:
        copula_cat.extend(range(info['start_idx'], info['end_idx']))
    copula_cont = [i for i in range(full_df.shape[1]) if i not in copula_cat]
    return {
        "preprocessor": preprocessor,
        "train_np": train.values.astype(np.float32),
        "train_cols": list(train.columns),
        "cont_idx": list(range(n_cont)),
        "cat_idx": list(range(n_cont, n_cont + n_cat)),
        "output_info": output_info,
        "full_np": full_df.values.astype(np.float32),
        "full_df": full_df,
        "full_cols": list(full_df.columns),
        "copula_cont": copula_cont,
        "copula_cat": copula_cat,
    }

def postprocess(syn_raw, gp, cols):
    post = TabularPostprocessor(preprocessor_object=gp["preprocessor"], verbose=False)
    if isinstance(syn_raw, np.ndarray):
        df_raw = pd.DataFrame(syn_raw, columns=cols)
    else:
        df_raw = pd.DataFrame(syn_raw.values, columns=cols)
    return post.inverse_transform_modified_data(df_raw)

def genuity_tabudiff(df, gp, n, premium=False):
    api = TabuDiffPremiumAPI() if premium else TabuDiffBasicAPI()
    api.fit(gp["full_np"])
    syn_mat = api.generate_dataframe(num_samples=n)
    return postprocess(syn_mat, gp, gp["full_cols"])

def genuity_masked(df, gp, n):
    api = MaskedPredictorAPI()
    api.fit(gp["full_df"])
    syn = api.generate()
    if syn is None or len(syn) == 0:
        return None
    # Scale to desired n
    if len(syn) < n:
        reps = (n // len(syn)) + 2
        syn = pd.concat([syn] * reps, ignore_index=True).iloc[:n]
    else:
        syn = syn.iloc[:n]
    return postprocess(syn, gp, gp["full_cols"])

def dp_tvae_sdv(df, n, epsilon=1.0, epochs=300):
    """DP noise + SDV TVAE."""
    dp = DifferentialPrivacyProcessor(epsilon=epsilon)
    df_priv = dp.apply_dp(df, method="laplace")
    return sdv_tvae(df_priv, n, epochs=epochs)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "="*65)
    print("SDV-BACKED SYNTHETIC DATA GENERATION — EXCELLENCE RUN")
    print("="*65)

    df = load_data()
    gp = get_genuity_inputs(df)

    SIZES = [300, 600, 1000]
    results = []

    tasks = [
        # (output_key,            display,              fn,                  kwargs)
        ("ctgan",           "SDV-CTGAN",          sdv_ctgan,           {"epochs": 300}),
        ("ctgan_premium",   "SDV-CTGAN-Premium",  sdv_ctgan,           {"epochs": 500}),
        ("tvae",            "SDV-TVAE",           sdv_tvae,            {"epochs": 300}),
        ("tvae_premium",    "SDV-TVAE-Premium",   sdv_tvae,            {"epochs": 500}),
        ("tabudiff",        "Genuity-TabuDiff",   None,                {"premium": False}),
        ("tabudiff_premium","Genuity-TabuDiffP",  None,                {"premium": True}),
        ("masked_predictor","Genuity-MaskedPred", None,                {}),
        ("dp_tvae",         "SDV-DP-TVAE",        dp_tvae_sdv,         {"epsilon": 1.0, "epochs": 300}),
    ]

    for size in SIZES:
        print(f"\n{'─'*55}\nSIZE = {size}\n{'─'*55}")
        for key, name, fn, kwargs in tasks:
            out = os.path.join(OUT_DIR, f"{key}_{size}.csv")
            print(f"\n[{name}] size={size}")
            t0 = time.time()
            try:
                if fn is not None:
                    # SDV-based
                    syn = fn(df, size, **kwargs)
                elif key.startswith("tabudiff"):
                    syn = genuity_tabudiff(df, gp, size, premium=kwargs.get("premium", False))
                elif key == "masked_predictor":
                    syn = genuity_masked(df, gp, size)
                else:
                    syn = None

                if syn is not None and len(syn) > 0:
                    syn.to_csv(out, index=False)
                    elapsed = time.time() - t0
                    print(f"  Saved {out} ({elapsed:.1f}s)")
                    m = evaluate(df, syn, f"{name}_{size}")
                    results.append({**m, "model_key": key, "size": size})
                else:
                    print(f"  FAILED — empty output")
                    results.append({"name": f"{name}_{size}", "model_key": key, "size": size,
                                    "ks": 0, "tstr": 0, "composite": 0})
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback; traceback.print_exc()
                results.append({"name": f"{name}_{size}", "model_key": key, "size": size,
                                "ks": 0, "tstr": 0, "composite": 0})

    # Also keep/evaluate Copula (already good)
    print("\n\n=== ALSO EVALUATING EXISTING COPULA ===")
    for size in SIZES:
        path = os.path.join(OUT_DIR, f"copula_{size}.csv")
        if os.path.exists(path):
            syn = pd.read_csv(path)
            m = evaluate(df, syn, f"Copula_{size}")
            results.append({**m, "model_key": "copula", "size": size})

    print("\n\n" + "="*65)
    print("FINAL LEADERBOARD")
    print("="*65)
    df_res = pd.DataFrame(results)
    df_res = df_res.sort_values("composite", ascending=False)
    print(df_res[["name", "size", "ks", "tstr", "composite"]].to_string(index=False))

    # Save
    df_res.to_csv(os.path.join(EXP_DIR, "excellence_results.csv"), index=False)
    print(f"\nSaved to {EXP_DIR}/excellence_results.csv")

if __name__ == "__main__":
    main()
