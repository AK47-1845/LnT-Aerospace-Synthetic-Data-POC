import os
import json
import socket
import datetime
import subprocess
import shutil
import pandas as pd
import numpy as np

import config
from config import DIRS, TARGET_EDGE_CASE_EXAMPLES, ALL_MODELS, GENUITY_MODELS, BASELINE_MODELS, SAMPLE_SIZES
from utils import logger, get_device
from physics import derive_physics_features, apply_physics_repair, score_dataset_physics
from edge_cases import enumerate_edge_cases, fallback_generate_edge_cases
from models_engine import run_optuna_study, UnifiedModelWrapper
from eval_extended import evaluate_extended, bootstrap_significance
import reporting

# For prep
from genuity.compliance import check_compliance_and_pii
from genuity.data_processor import TabularPreprocessor

def get_env_metadata():
    try:
        pip_freeze = subprocess.check_output(["pip", "freeze"]).decode("utf-8").split("\n")
    except:
        pip_freeze = []
        
    return {
        "timestamp": config.TIMESTAMP,
        "hostname": socket.gethostname(),
        "device": str(get_device()),
        "packages": pip_freeze
    }

def save_manifest(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def prepare_data():
    logger.info("Loading dataset...")
    df_raw = pd.read_csv("d:/aero/aerospace_structural_design_dataset.csv")
    
    # Validation & Physics Derivation
    df_raw = df_raw.dropna()
    df_raw = derive_physics_features(df_raw)
    
    # PII
    result = check_compliance_and_pii(df_raw)
    df_clean = result["dataframe"]
    
    # Preprocessor
    preprocessor = TabularPreprocessor(random_state=42, verbose=False)
    pre_result = preprocessor.fit_transform(df_clean)
    
    cont_df = pre_result['continuous']
    cat_df = pre_result['categorical']
    training_data_filtered = pd.concat([cont_df, cat_df], axis=1)
    
    n_continuous = cont_df.shape[1]
    n_total = training_data_filtered.shape[1]
    
    # Safely handle column names for numeric vs categorical
    num_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df_raw.select_dtypes(exclude=[np.number]).columns.tolist()

    dataset_info = {
        "df_raw": df_clean,
        "numpy_filtered": training_data_filtered.values.astype(np.float32),
        "cols_filtered": training_data_filtered.columns.tolist(),
        "continuous_indices": list(range(n_continuous)),
        "categorical_indices": list(range(n_continuous, n_total)),
        "output_info": preprocessor.get_output_info(),
        "preprocessor": preprocessor,
        "cat_cols": cat_cols,
        "num_cols": num_cols
    }
    return dataset_info

def main():
    logger.info("=========================================")
    logger.info("Starting Complex synthetic orchestration")
    
    # 0. Metadata & Env
    meta = get_env_metadata()
    save_manifest(os.path.join(DIRS['signoff'], "run_metadata.json"), meta)
    
    # 1. Prepare Data
    dataset_info = prepare_data()
    real_df = dataset_info["df_raw"]
    
    # 2. Edge Case Enumeration
    edge_catalog_df = enumerate_edge_cases(real_df)
    
    # 3. Two-Phase Benchmarking
    results_registry = []
    best_params_map = {}
    
    # PHASE 1: Smoke (8 trials)
    logger.info("--- PHASE 1: SMOKE TESTS ---")
    smoke_scores = {}
    for m in ALL_MODELS:
        try:
            params = run_optuna_study(m, dataset_info, n_trials=3) # Accelerated smoke
            best_params_map[m] = params
            wrapper = UnifiedModelWrapper(m, params, dataset_info)
            wrapper.fit()
            syn_test = wrapper.generate(600)
            metrics = evaluate_extended(real_df, syn_test, dataset_info["cat_cols"], dataset_info["num_cols"])
            smoke_scores[m] = metrics["composite_score"]
        except Exception as e:
            logger.error(f"Phase 1 Smoke failed for {m}: {e}")
            smoke_scores[m] = -np.inf
        
    # Pick Top 6 families
    sorted_models = sorted(smoke_scores, key=smoke_scores.get, reverse=True)
    top_models = [m for m in sorted_models if smoke_scores[m] > -np.inf][:6]
    logger.info(f"Top models advancing to Phase 2: {top_models}")
    
    # PHASE 2: Full
    for m in top_models:
        try:
            params = run_optuna_study(m, dataset_info, n_trials=6) # Accelerated Full for this session
            best_params_map[m] = params
            wrapper = UnifiedModelWrapper(m, params, dataset_info)
            wrapper.fit()
            
            # Default seeds and sizes
            for seed in config.DEFAULT_SEEDS:
                for size in SAMPLE_SIZES:
                    logger.info(f"Generating {m} (Seed {seed}, Size {size})")
                    np.random.seed(seed)
                    
                    try:
                        syn_df = wrapper.generate(size)
                        syn_df, rep_count = apply_physics_repair(syn_df)
                        
                        # Ensure physics bounds exactly
                        syn_df = derive_physics_features(syn_df)
                        
                        metrics = evaluate_extended(real_df, syn_df, dataset_info["cat_cols"], dataset_info["num_cols"])
                        metrics["repair_count"] = rep_count
                        metrics["Model"] = m
                        metrics["Seed"] = seed
                        metrics["Size"] = size
                        
                        # Save exactly
                        file_name = f"synthetic_{m}_{seed}_{size}_best.csv"
                        path = os.path.join(DIRS['synth_datasets'], file_name)
                        syn_df.to_csv(path, index=False)
                        
                        # Metadata provenance
                        save_manifest(path.replace(".csv", "_provenance.json"), {
                            "model": m, "seed": seed, "size": size, "params": params, "metrics": metrics
                        })
                        
                        results_registry.append(metrics)
                        
                        # Output visualization snapshot for the 600 default (Phase 5 request)
                        if size == 600:
                            reporting.generate_visuals(real_df, syn_df, m, str(seed))
                            
                    except Exception as e:
                        logger.error(f"Generation failed for {m} {seed} {size}: {e}")
        except Exception as e:
            logger.error(f"Phase 2 Failed for {m}: {e}")

    # Edge-Cases Fallback Validation (just for top model)
    df_results = pd.DataFrame(results_registry)
    if df_results.empty:
        logger.error("No valid results were generated. Exiting.")
        return

    df_results.to_csv(os.path.join(DIRS['metrics'], "metrics_raw.csv"), index=False)
    
    best_overall = df_results.sort_values(by="composite_score", ascending=False).iloc[0]
    best_m = best_overall["Model"]
    best_seed = int(best_overall["Seed"])
    best_size = int(best_overall["Size"])
    
    logger.info(f"Running edge-case coverage fallback array for {best_m}")
    fallback_generate_edge_cases(real_df, edge_catalog_df, best_m, 42)
    
    # Extended Significance
    baseline_options = [m for m in BASELINE_MODELS if m in top_models]
    best_base = baseline_options[0] if baseline_options else "Empirical"
    
    try:
        best_gen_series = df_results[(df_results["Model"]==best_m) & (df_results["Size"]==600)].iloc[0]
        best_base_series = df_results[(df_results["Model"]==best_base) & (df_results["Size"]==600)].iloc[0]
        
        df_a = pd.read_csv(os.path.join(DIRS['synth_datasets'], f"synthetic_{best_m}_{int(best_gen_series['Seed'])}_600_best.csv"))
        df_b = pd.read_csv(os.path.join(DIRS['synth_datasets'], f"synthetic_{best_base}_{int(best_base_series['Seed'])}_600_best.csv"))
        
        sig_data = bootstrap_significance(real_df, df_a, df_b, dataset_info["cat_cols"], dataset_info["num_cols"])
        save_manifest(os.path.join(DIRS['metrics'], "significance_tests.json"), sig_data)
    except Exception as e:
        logger.error(f"Significance tests failed (maybe shapes mismatch or missing 600 size file): {e}")
        sig_data = {"is_significant": False}
    
    # 4. Final Reporting
    reporting.build_html_report(best_m, df_results, meta, edge_catalog_df)
    try:
        reporting.create_client_slides(
            os.path.join(DIRS['signoff'], "client_slides.pptx"),
            meta, best_m, float(best_overall["composite_score"]), sig_data["is_significant"]
        )
    except Exception as e:
        logger.error(f"Failed to create PPTX natively: {e}")
    
    logger.info("Pipeline Complete. Check final_deliverable for the full SIGN OFF PACKAGE")

if __name__ == "__main__":
    main()
