import optuna
import pandas as pd
import numpy as np
from config import HYPERPARAM_GRIDS, GENUITY_MODELS, BASELINE_MODELS, SAMPLE_SIZES, DIRS
from eval_extended import evaluate_extended
from utils import logger
import traceback

# Genuity Models
from genuity.core_generator import (
    CTGANAPI, TVAEAPI, TabuDiffBasicAPI, CopulaAPI, MaskedPredictorAPI, DifferentialPrivacyProcessor
)
from genuity.data_processor.data_postprocess import TabularPostprocessor

# Baselines
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KernelDensity

class UnifiedModelWrapper:
    def __init__(self, model_name, params, dataset_info):
        self.model_name = model_name
        self.params = params
        self.dataset_info = dataset_info
        
        self.df_raw = dataset_info["df_raw"]
        self.numpy_filtered = dataset_info["numpy_filtered"]
        self.continuous_indices = dataset_info["continuous_indices"]
        self.categorical_indices = dataset_info["categorical_indices"]
        self.output_info = dataset_info["output_info"]
        self.preprocessor = dataset_info["preprocessor"]
        self.cols_filtered = dataset_info["cols_filtered"]
        
        self._init_model()

    def _init_model(self):
        m = self.model_name
        if m == "TVAE": self.model = TVAEAPI()
        elif m == "CTGAN": self.model = CTGANAPI()
        elif m == "TabuDiff": self.model = TabuDiffBasicAPI()
        elif m == "Copula": self.model = CopulaAPI()
        elif m == "MaskedPredictor": self.model = MaskedPredictorAPI()
        elif m == "DP_TVAE": self.model = TVAEAPI()
        elif m == "GMM": self.model = GaussianMixture(
            n_components=self.params.get("n_components", 5), 
            covariance_type=self.params.get("covariance_type", "full")
        )
        elif m == "KDE":
            bw = self.params.get("bandwidth", "scott")
            if bw == "scott": bw = 1.0 # fallback for sklearn < 1.0 
            self.model = KernelDensity(bandwidth=bw)
        elif m == "Empirical":
            pass # No model needed, relies on raw_df
        else:
            raise ValueError(f"Unknown: {m}")

    def fit(self):
        m = self.model_name
        p = self.params
        
        if m in ["TVAE", "DP_TVAE"]:
            df_train = self.df_raw
            if m == "DP_TVAE":
                dp = DifferentialPrivacyProcessor(epsilon=p.get("epsilon", 1.0))
                df_train = dp.apply_dp(self.df_raw, method="minimal")
            self.model.fit(df_train, epochs=p.get("epochs", 100))
            
        elif m == "CTGAN":
            self.model.fit(
                data=self.numpy_filtered,
                continuous_cols=self.continuous_indices,
                categorical_cols=self.categorical_indices,
                epochs=p.get("epochs", 200),
                output_info=self.output_info
            )
            
        elif m == "TabuDiff":
            self.model.fit(self.numpy_filtered)
            
        elif m == "Copula":
            self.model.fit(
                data=self.numpy_filtered,
                continuous_cols=self.continuous_indices,
                categorical_cols=self.categorical_indices,
                pretransformed=True,
                output_info=self.output_info
            )
            
        elif m == "MaskedPredictor":
            df_numeric = pd.DataFrame(self.numpy_filtered, columns=self.cols_filtered)
            self.model.fit(df_numeric)
            
        elif m in ["GMM", "KDE"]:
            self.model.fit(self.numpy_filtered)
            
        elif m == "Empirical":
            pass 

    def generate(self, n_samples):
        m = self.model_name
        
        if m == "Empirical":
            return self.df_raw.sample(n_samples, replace=True).copy()
            
        elif m in ["TVAE", "DP_TVAE"]:
            return self.model.generate(n_samples)
            
        elif m == "CTGAN":
            syn_raw = self.model.generate(n_samples=n_samples)
            fake_df = pd.DataFrame(syn_raw, columns=self.cols_filtered)
        
        elif m == "Copula":
            syn_raw = self.model.generate(n_samples=n_samples)
            fake_df = pd.DataFrame(syn_raw, columns=self.cols_filtered)
            
        elif m == "TabuDiff":
            syn_raw = self.model.generate_dataframe(num_samples=n_samples)
            fake_df = pd.DataFrame(syn_raw.values, columns=self.cols_filtered)
            
        elif m == "MaskedPredictor":
            fake_df = self.model.generate()
            if len(fake_df) > n_samples:
                fake_df = fake_df.sample(n_samples)
            elif len(fake_df) < n_samples:
                fake_df = fake_df.sample(n_samples, replace=True)
                
        elif m == "GMM":
            syn_raw, _ = self.model.sample(n_samples)
            fake_df = pd.DataFrame(syn_raw, columns=self.cols_filtered)
            
        elif m == "KDE":
            syn_raw = self.model.sample(n_samples)
            fake_df = pd.DataFrame(syn_raw, columns=self.cols_filtered)

        post = TabularPostprocessor(preprocessor_object=self.preprocessor)
        return post.inverse_transform_modified_data(fake_df)

def run_optuna_study(model_name, dataset_info, n_trials=8):
    logger.info(f"Phase {'1 (Smoke)' if n_trials <= 12 else '2 (Full)'} Optuna for {model_name}...")
    grid = HYPERPARAM_GRIDS.get(model_name, {})
    
    # Empirical needs no tuning
    if model_name == "Empirical" or not grid:
        return {}

    def objective(trial):
        params = {}
        for k, choices in grid.items():
            params[k] = trial.suggest_categorical(k, choices)
            
        try:
            wrapper = UnifiedModelWrapper(model_name, params, dataset_info)
            wrapper.fit()
            syn_df = wrapper.generate(n_samples=600)
            
            # SAVE EVERY SINGLE CSV
            import os
            trial_csv_path = os.path.join(DIRS['optuna'], f"{model_name}_trial_{trial.number}.csv")
            syn_df.to_csv(trial_csv_path, index=False)
            
            metrics = evaluate_extended(dataset_info["df_raw"], syn_df, dataset_info["cat_cols"], dataset_info["num_cols"])
            
            # SAVE EVERY METRIC JSON
            import json
            trial_json_path = os.path.join(DIRS['optuna'], f"{model_name}_trial_{trial.number}_metrics.json")
            with open(trial_json_path, 'w') as f:
                json.dump(metrics, f, indent=4)
                
            return metrics["composite_score"]
        except Exception as e:
            logger.error(f"Trial failed:\n{traceback.format_exc()}")
            return 0.0

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    
    logger.info(f"Best Optuna params for {model_name}: {study.best_params} (Val: {study.best_value:.4f})")
    
    # Save study summary
    df_study = study.trials_dataframe()
    df_study.to_csv(f"{DIRS['optuna']}/{model_name}_study_n{n_trials}.csv", index=False)
    
    return study.best_params
