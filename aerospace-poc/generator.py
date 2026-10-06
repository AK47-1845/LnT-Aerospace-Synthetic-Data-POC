import os
import pandas as pd
import numpy as np
import optuna
import torch

from config import *
from utils import logger, get_device
from evaluator import get_composite_score

from genuity.core_generator import (
    CTGANAPI, TVAEAPI, TabuDiffBasicAPI, CopulaAPI, MaskedPredictorAPI, DifferentialPrivacyProcessor
)
from genuity.data_processor.data_postprocess import TabularPostprocessor
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KernelDensity

device = get_device()

class BaselineGMM:
    def __init__(self, n_components=3):
        self.model = GaussianMixture(n_components=n_components, covariance_type='full', random_state=42)
        
    def fit(self, data):
        self.model.fit(data)
        
    def generate(self, n_samples):
        # returns tuple (samples, labels)
        X_gen, _ = self.model.sample(n_samples)
        return type('', (), {"values": X_gen})()

class BaselineKDE:
    def __init__(self, bandwidth='scott'):
        # Fallback to float if scott is not perfectly supported
        self.bw = bandwidth if bandwidth in ['scott', 'silverman'] else 1.0
        self.model = KernelDensity(bandwidth=self.bw)
        
    def fit(self, data):
        self.model.fit(data)
        
    def generate(self, n_samples):
        X_gen = self.model.sample(n_samples, random_state=42)
        return type('', (), {"values": X_gen})()

def fetch_model(model_name, params):
    if model_name == "TVAE":
        return TVAEAPI() # TVAE accepts epochs in fit
    elif model_name == "CTGAN":
        return CTGANAPI()
    elif model_name == "TabuDiff":
        return TabuDiffBasicAPI()
    elif model_name == "Copula":
        return CopulaAPI()
    elif model_name == "MaskedPredictor":
        return MaskedPredictorAPI()
    elif model_name == "DP_TVAE":
        return TVAEAPI()
    elif model_name == "GMM":
        return BaselineGMM(n_components=params.get("n_components", 3))
    elif model_name == "KDE":
        return BaselineKDE(bandwidth=params.get("bandwidth", "scott"))
    else:
        raise ValueError(f"Unknown model: {model_name}")

def train_and_generate(model_name, params, dataset_info, seed, n_samples):
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    model = fetch_model(model_name, params)
    
    df_raw = dataset_info["df_raw"]
    numpy_filtered = dataset_info["numpy_filtered"]
    continuous_indices = dataset_info["continuous_indices"]
    categorical_indices = dataset_info["categorical_indices"]
    output_info = dataset_info["output_info"]
    preprocessor = dataset_info["preprocessor"]
    cols_filtered = dataset_info["cols_filtered"]
    
    # 1. Fit
    if model_name in ["TVAE", "DP_TVAE"]:
        epochs = params.get("epochs", 100)
        df_train = df_raw
        if model_name == "DP_TVAE":
            dp = DifferentialPrivacyProcessor(epsilon=params.get("epsilon", 1.0))
            df_train = dp.apply_dp(df_raw, method="minimal")
            
        # Optional latent_dim passing, depending on genuity API. Assume it uses kwargs
        model.fit(df_train, epochs=epochs)
        
    elif model_name == "CTGAN":
        epochs = params.get("epochs", 200)
        batch_size = params.get("batch_size", 256)
        # Assuming genuity handles batch_size via kwargs
        model.fit(
            data=numpy_filtered,
            continuous_cols=continuous_indices,
            categorical_cols=categorical_indices,
            epochs=epochs,
            output_info=output_info
        )
        
    elif model_name == "Copula":
        model.fit(
            data=numpy_filtered,
            continuous_cols=continuous_indices,
            categorical_cols=categorical_indices,
            pretransformed=True,
            output_info=output_info
        )
        
    elif model_name == "TabuDiff":
        # Fits on numpy numeric
        model.fit(numpy_filtered)
        
    elif model_name == "MaskedPredictor":
        # Fits on preprocessed dataframe numeric
        df_numeric = pd.DataFrame(numpy_filtered, columns=cols_filtered)
        model.fit(df_numeric)
        
    elif model_name in ["GMM", "KDE"]:
        model.fit(numpy_filtered)
        
    # 2. Generate
    if model_name in ["TVAE", "DP_TVAE"]:
        syn_df = model.generate(n_samples)
        return syn_df
        
    elif model_name == "CTGAN":
        syn_raw = model.generate(n_samples=n_samples)
        fake_df_raw = pd.DataFrame(syn_raw, columns=cols_filtered)
        post = TabularPostprocessor(preprocessor_object=preprocessor)
        return post.inverse_transform_modified_data(fake_df_raw)
        
    elif model_name == "Copula":
        syn_raw = model.generate(n_samples=n_samples)
        fake_df_raw = pd.DataFrame(syn_raw, columns=cols_filtered)
        post = TabularPostprocessor(preprocessor_object=preprocessor)
        return post.inverse_transform_modified_data(fake_df_raw)
        
    elif model_name == "TabuDiff":
        syn_raw = model.generate_dataframe(num_samples=n_samples)
        fake_df_raw = pd.DataFrame(syn_raw.values, columns=cols_filtered)
        post = TabularPostprocessor(preprocessor_object=preprocessor)
        return post.inverse_transform_modified_data(fake_df_raw)
        
    elif model_name == "MaskedPredictor":
        syn_numeric_df = model.generate()
        # Assumes generate returns df of same shape or n_samples if supported. 
        # Genuity's doc shows generate() w/o n_samples. We will trim/sample it.
        if len(syn_numeric_df) > n_samples:
            syn_numeric_df = syn_numeric_df.sample(n_samples)
        post = TabularPostprocessor(preprocessor_object=preprocessor)
        return post.inverse_transform_modified_data(syn_numeric_df)
        
    elif model_name in ["GMM", "KDE"]:
        syn_raw = model.generate(n_samples)
        fake_df_raw = pd.DataFrame(syn_raw.values, columns=cols_filtered)
        post = TabularPostprocessor(preprocessor_object=preprocessor)
        return post.inverse_transform_modified_data(fake_df_raw)

def run_optuna(model_name, dataset_info, n_trials=2):
    """ Runs a tiny grid/random search to find best hyperparams """
    logger.info(f"Running Optuna Optimization for {model_name}...")
    
    grid = HYPERPARAM_GRIDS.get(model_name, {})
    if not grid:
        return {} # No search needed
        
    def objective(trial):
        params = {}
        for k, choices in grid.items():
            params[k] = trial.suggest_categorical(k, choices)
            
        try:
            # Generate a small sample to evaluate
            syn_df = train_and_generate(model_name, params, dataset_info, seed=42, n_samples=300)
            score, _ = get_composite_score(dataset_info["df_raw"], syn_df)
            return score
        except Exception as e:
            logger.error(f"Trial failed for {model_name} with {params}: {e}")
            return 0.0

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    
    logger.info(f"Best params for {model_name}: {study.best_params} (Score: {study.best_value:.4f})")
    return study.best_params

def generate_all_candidates(dataset_info):
    best_params_per_model = {}
    
    # 1. Tuning Phase
    for model_name in MODELS_TO_RUN:
        best_params_per_model[model_name] = run_optuna(model_name, dataset_info, n_trials=2)
        
    # 2. Generation Phase
    logger.info("Starting Mass Generation Phase...")
    results_registry = []
    
    for model_name in MODELS_TO_RUN:
        params = best_params_per_model[model_name]
        for seed in range(N_SEEDS):
            for size in SAMPLE_SIZES:
                logger.info(f"Generating -> {model_name} | Seed: {seed} | Size: {size}")
                try:
                    syn_df = train_and_generate(model_name, params, dataset_info, seed=seed, n_samples=size)
                    
                    # Force exact matching for categorical levels to avoid downstream issues
                    for col in CATEGORICAL_COLS:
                        if col in syn_df.columns and col in dataset_info['df_raw'].columns:
                            # Clip / Map unsupported categories to most frequent real category
                            real_cats = dataset_info['df_raw'][col].dropna().unique()
                            mode_cat = dataset_info['df_raw'][col].mode()[0]
                            syn_df[col] = syn_df[col].apply(lambda x: x if x in real_cats else mode_cat)
                    
                    # Ensure range clipping for numerics based on real ranges
                    for col in syn_df.select_dtypes(include=[np.number]).columns:
                        if col in dataset_info['df_raw'].columns:
                            cmin, cmax = dataset_info['df_raw'][col].min(), dataset_info['df_raw'][col].max()
                            syn_df[col] = syn_df[col].clip(cmin, cmax)
                            
                    out_path = os.path.join(SYNTHETIC_DIR, f"synthetic_{model_name}_{seed}_{size}.csv")
                    syn_df.to_csv(out_path, index=False)
                    
                    # Evaluate on the spot
                    score, details = get_composite_score(dataset_info["df_raw"], syn_df)
                    
                    results_registry.append({
                        "Model": model_name,
                        "Seed": seed,
                        "SampleSize": size,
                        "Params": str(params),
                        "CompositeScore": score,
                        "EvalDetails": details,
                        "Path": out_path
                    })
                except Exception as e:
                    logger.error(f"Generation failed for {model_name} s={seed} n={size} -> {e}")
                    
    return pd.DataFrame(results_registry)
