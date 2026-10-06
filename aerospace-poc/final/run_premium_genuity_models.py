"""
Premium Genuity Model Experiments — GPU-enabled
RTX 4050 Laptop GPU | CUDA 12.4 | torch 2.6.0+cu124
Models: CTGANPremium, TVAEPremium, CopulaAPI, TabuDiffPremium, DP-TVAEPremium
Max epochs: 1000 (as specified)
"""
import os, sys, logging, warnings, traceback
import numpy as np
import pandas as pd
from datetime import datetime

warnings.filterwarnings('ignore')

# ── Live logging to both stdout AND file ──────────────────────────────────────
LOG_FILE = r"d:\aero\final\premium_models.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
handlers = [
    logging.StreamHandler(sys.stdout),
    logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
]
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=handlers)
logger = logging.getLogger(__name__)

# Force stdout to flush immediately (live log)
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

REAL_PATH = r"d:\aero\aerospace_structural_design_dataset.csv"
OUT_DIR   = r"d:\aero\final\per_model_datasets"
EXP_DIR   = r"d:\aero\final\experiments"
SEED      = 11
TARGETS   = ["Vibration Damping", "Computational Time", "Weight Efficiency", "Durability"]

# ── GPU verify ────────────────────────────────────────────────────────────────
import torch
logger.info(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
    logger.info(f"VRAM: {round(torch.cuda.get_device_properties(0).total_memory/1e9,1)} GB")
else:
    logger.warning("No CUDA — running on CPU")

# ── Genuity imports ────────────────────────────────────────────────────────────
sys.path.insert(0, r"d:\aero")
from genuity.compliance import check_compliance_and_pii
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
from genuity.core_generator import (
    CTGANPremiumAPI, TVAEPremiumAPI,
    TabuDiffPremiumAPI, CopulaAPI,
    DifferentialPrivacyProcessor
)

# ── Quick evaluation (custom TSTR + KS) ───────────────────────────────────────
def quick_eval(real_df, syn_df):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score
    from scipy.stats import ks_2samp

    cat_cols = [c for c in syn_df.select_dtypes(include='object').columns if c not in TARGETS]
    features = [c for c in real_df.columns if c not in TARGETS]

    def enc(df):
        e = df.copy()
        for c in cat_cols + TARGETS:
            if c in e.columns:
                e[c] = LabelEncoder().fit_transform(e[c].astype(str))
        return e

    r_e, s_e = enc(real_df), enc(syn_df)
    tstr_scores = []
    for t in TARGETS:
        if t not in syn_df.columns: continue
        try:
            feat_c = [c for c in features if c in r_e.columns and c in s_e.columns]
            rf = RandomForestClassifier(n_estimators=100, random_state=42)
            rf.fit(s_e[feat_c], s_e[t])
            tstr_scores.append(accuracy_score(r_e[t], rf.predict(r_e[feat_c])))
        except:
            tstr_scores.append(0.0)

    num_cols = real_df.select_dtypes(include=np.number).columns.tolist()
    ks_passes = []
    for c in num_cols:
        if c not in syn_df.columns: continue
        try:
            _, p = ks_2samp(real_df[c].dropna(), syn_df[c].dropna())
            ks_passes.append(p > 0.05)
        except: pass

    return {
        "tstr_mean":    round(float(np.mean(tstr_scores)), 4) if tstr_scores else 0.0,
        "ks_pass_rate": round(float(np.mean(ks_passes)),   4) if ks_passes   else 0.0,
    }

# ── Data preparation (per DOCUMENTATION.md) ──────────────────────────────────
def prepare_data(real_df):
    result   = check_compliance_and_pii(real_df)
    df_clean = result["dataframe"]
    preprocessor = TabularPreprocessor(random_state=SEED, verbose=False)
    pre      = preprocessor.fit_transform(df_clean)
    # CRITICAL: exclude outlier_flags + pca — only continuous + categorical
    cont_df  = pre['continuous']
    cat_df   = pre['categorical']
    train    = pd.concat([cont_df, cat_df], axis=1)
    n_cont   = cont_df.shape[1]
    return {
        "df_clean":    df_clean,
        "preprocessor":preprocessor,
        "train_df":    train,
        "numpy_data":  train.values.astype(np.float32),
        "cont_idx":    list(range(n_cont)),
        "cat_idx":     list(range(n_cont, train.shape[1])),
        "output_info": preprocessor.get_output_info(),
        "feat_names":  train.columns.tolist(),
    }

def postprocess(syn_raw, info):
    post = TabularPostprocessor(preprocessor_object=info["preprocessor"], verbose=False)
    if isinstance(syn_raw, np.ndarray):
        df_raw = pd.DataFrame(syn_raw, columns=info["feat_names"])
    else:
        vals   = syn_raw.values if hasattr(syn_raw, 'values') else np.array(syn_raw)
        n      = min(vals.shape[1], len(info["feat_names"]))
        df_raw = pd.DataFrame(vals[:, :n], columns=info["feat_names"][:n])
    return post.inverse_transform_modified_data(df_raw)

def align_clip(syn_df, real_df):
    if len(syn_df.columns) == len(real_df.columns):
        try: syn_df = syn_df[real_df.columns]
        except: pass
    for col in real_df.select_dtypes(include=np.number).columns:
        if col in syn_df.columns:
            syn_df[col] = syn_df[col].clip(real_df[col].min(), real_df[col].max())
    return syn_df

def save_eval(syn_df, real_df, tag, size, extra=None):
    syn_df = align_clip(syn_df, real_df)
    fname  = f"{tag}_{size}.csv"
    fpath  = os.path.join(OUT_DIR, fname)
    syn_df.to_csv(fpath, index=False)
    ev = quick_eval(real_df, syn_df)
    schema_ok = list(syn_df.columns) == list(real_df.columns)
    logger.info(f"  SAVED [{tag}_{size}] | TSTR={ev['tstr_mean']:.4f} | "
                f"KS={ev['ks_pass_rate']:.4f} | rows={len(syn_df)} | "
                f"schema={'OK' if schema_ok else 'MISMATCH'}")
    row = {"model": tag, "size": size, "timestamp": datetime.now().isoformat(),
           **ev, "schema_ok": schema_ok, "path": fpath}
    if extra: row.update(extra)
    return row

# ── Model runners ──────────────────────────────────────────────────────────────

def run_ctgan_premium(real_df, info, size, epochs=500):
    logger.info(f"  CTGANPremium | epochs={epochs} | n={size} | GPU={'YES' if torch.cuda.is_available() else 'NO'}")
    np.random.seed(SEED)
    model = CTGANPremiumAPI(model_type="premium")
    model.fit(
        data=info["numpy_data"],
        continuous_cols=info["cont_idx"],
        categorical_cols=info["cat_idx"],
        epochs=epochs,
        output_info=info["output_info"],
        premium_features={
            "use_spectral_norm":    True,   # prevents mode collapse
            "use_gradient_penalty": True,   # stabilises training
        }
    )
    return postprocess(model.generate(n_samples=size), info)


def run_tvae_premium(real_df, info, size, epochs=300):
    logger.info(f"  TVAEPremium | epochs={epochs} | n={size} | GPU={'YES' if torch.cuda.is_available() else 'NO'}")
    np.random.seed(SEED)
    model = TVAEPremiumAPI(model_type="premium")
    model.fit(info["df_clean"], epochs=epochs,
              premium_features={"use_vamp_prior": True, "use_cyclical_annealing": True})
    syn = model.generate(size)
    if not isinstance(syn, pd.DataFrame): syn = pd.DataFrame(syn)
    return syn


def run_copula(real_df, info, size):
    logger.info(f"  CopulaAPI | n={size}")
    np.random.seed(SEED)
    model = CopulaAPI()
    model.fit(data=info["numpy_data"], continuous_cols=info["cont_idx"],
              categorical_cols=info["cat_idx"], pretransformed=True,
              output_info=info["output_info"])
    return postprocess(model.generate(n_samples=size), info)


def run_tabudiff_premium(real_df, info, size):
    logger.info(f"  TabuDiffPremium | n={size} | GPU={'YES' if torch.cuda.is_available() else 'NO'}")
    np.random.seed(SEED)
    model = TabuDiffPremiumAPI()
    try:
        model.fit_dataframe(info["df_clean"], verbose=False)
    except Exception:
        model.fit(info["numpy_data"])
    syn_raw = model.generate_dataframe(num_samples=size)
    try:
        if isinstance(syn_raw, pd.DataFrame):
            df_raw = pd.DataFrame(syn_raw.values, columns=info["feat_names"][:syn_raw.shape[1]])
        else:
            df_raw = pd.DataFrame(syn_raw, columns=info["feat_names"][:np.array(syn_raw).shape[1]])
        post = TabularPostprocessor(preprocessor_object=info["preprocessor"], verbose=False)
        return post.inverse_transform_modified_data(df_raw)
    except Exception:
        return syn_raw if isinstance(syn_raw, pd.DataFrame) else pd.DataFrame(syn_raw)


def run_dp_tvae_premium(real_df, info, size, epsilon=1.0):
    logger.info(f"  DP-TVAEPremium | epsilon={epsilon} | n={size}")
    np.random.seed(SEED)
    dp = DifferentialPrivacyProcessor(epsilon=epsilon, noise_scale=0.05,
                                       categorical_noise_prob=0.03)
    df_private = dp.apply_dp(real_df, method="laplace")
    model = TVAEPremiumAPI(model_type="premium")
    model.fit(df_private, epochs=300,
              premium_features={"use_vamp_prior": True, "use_cyclical_annealing": True})
    syn = model.generate(size)
    if not isinstance(syn, pd.DataFrame): syn = pd.DataFrame(syn)
    return syn

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(EXP_DIR, exist_ok=True)

    real_df = pd.read_csv(REAL_PATH)
    logger.info(f"Real data: {real_df.shape}")
    info = prepare_data(real_df)
    logger.info(f"Data prep done | tensor={info['numpy_data'].shape} | "
                f"cont={len(info['cont_idx'])} cat={len(info['cat_idx'])}")

    all_results = []
    SIZES = [300, 600, 1000]

    # ── 1. CTGANPremium — spectral_norm + gradient_penalty ────────────────────
    logger.info("\n" + "="*65)
    logger.info("MODEL 1 / 5  |  CTGANPremium  |  epochs=500 (max 1000 cap)")
    logger.info("="*65)
    for size in SIZES:
        try:
            syn = run_ctgan_premium(real_df, info, size, epochs=500)
            all_results.append(save_eval(syn, real_df, "ctgan_premium", size))
        except Exception as e:
            logger.error(f"  CTGANPremium size={size} FAILED: {e}\n{traceback.format_exc()}")

    # Also run 1000-row at 1000 epochs for best quality (user cap respected)
    logger.info("\n  -- CTGANPremium 1000-row at MAX 1000 epochs --")
    try:
        syn = run_ctgan_premium(real_df, info, 1000, epochs=1000)
        all_results.append(save_eval(syn, real_df, "ctgan_premium_e1000", 1000))
    except Exception as e:
        logger.error(f"  CTGANPremium e1000 FAILED: {e}")

    # ── 2. TVAEPremium — VampPrior + Cyclical Annealing ───────────────────────
    logger.info("\n" + "="*65)
    logger.info("MODEL 2 / 5  |  TVAEPremium  |  epochs=300")
    logger.info("="*65)
    for size in SIZES:
        try:
            syn = run_tvae_premium(real_df, info, size, epochs=300)
            all_results.append(save_eval(syn, real_df, "tvae_premium", size))
        except Exception as e:
            logger.error(f"  TVAEPremium size={size} FAILED: {e}\n{traceback.format_exc()}")

    # ── 3. CopulaAPI ──────────────────────────────────────────────────────────
    logger.info("\n" + "="*65)
    logger.info("MODEL 3 / 5  |  CopulaAPI  |  (no epochs — Gaussian Copula)")
    logger.info("="*65)
    for size in SIZES:
        try:
            syn = run_copula(real_df, info, size)
            all_results.append(save_eval(syn, real_df, "copula", size))
        except Exception as e:
            logger.error(f"  CopulaAPI size={size} FAILED: {e}\n{traceback.format_exc()}")

    # ── 4. TabuDiffPremium ────────────────────────────────────────────────────
    logger.info("\n" + "="*65)
    logger.info("MODEL 4 / 5  |  TabuDiffPremium")
    logger.info("="*65)
    for size in SIZES:
        try:
            syn = run_tabudiff_premium(real_df, info, size)
            all_results.append(save_eval(syn, real_df, "tabudiff_premium", size))
        except Exception as e:
            logger.error(f"  TabuDiffPremium size={size} FAILED: {e}\n{traceback.format_exc()}")

    # ── 5. DP-TVAEPremium — privacy budget sweep ──────────────────────────────
    logger.info("\n" + "="*65)
    logger.info("MODEL 5 / 5  |  DP-TVAEPremium  |  epsilon=0.5 / 1.0 / 2.0")
    logger.info("="*65)
    for eps in [0.5, 1.0, 2.0]:
        try:
            syn = run_dp_tvae_premium(real_df, info, 1000, epsilon=eps)
            tag = f"dp_tvae_premium_eps{str(eps).replace('.','p')}"
            all_results.append(save_eval(syn, real_df, tag, 1000, {"epsilon": eps}))
        except Exception as e:
            logger.error(f"  DP-TVAEPremium eps={eps} FAILED: {e}")

    # ── Final leaderboard ─────────────────────────────────────────────────────
    logger.info("\n" + "="*65)
    logger.info("ALL PREMIUM RUNS COMPLETE — LEADERBOARD")
    logger.info("="*65)
    results_df = pd.DataFrame(all_results)
    if len(results_df):
        lb = results_df[results_df["size"]==1000].sort_values("tstr_mean", ascending=False)
        for _, r in lb.iterrows():
            logger.info(f"  {r['model']:40s} | TSTR={r['tstr_mean']:.4f} | KS={r['ks_pass_rate']:.4f}")

    out_path = os.path.join(EXP_DIR, "premium_experiments.csv")
    results_df.to_csv(out_path, index=False)
    logger.info(f"\nResults saved: {out_path}")
    logger.info("DONE. Run full_validation_pipeline.py for complete Tier 2 metrics.")


if __name__ == "__main__":
    main()
