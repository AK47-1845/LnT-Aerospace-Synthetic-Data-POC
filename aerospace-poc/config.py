import os
import datetime

# --- TIMESTAMP & PATHS ---
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ROOT_ARTIFACTS = f"d:/aero/artifacts/experiments/{TIMESTAMP}/"

DIRS = {
    "raw_runs": os.path.join(ROOT_ARTIFACTS, "raw_runs"),
    "synth_datasets": os.path.join(ROOT_ARTIFACTS, "synth_datasets"),
    "metrics": os.path.join(ROOT_ARTIFACTS, "metrics"),
    "visuals": os.path.join(ROOT_ARTIFACTS, "visuals"),
    "optuna": os.path.join(ROOT_ARTIFACTS, "optuna"),
    "reports": os.path.join(ROOT_ARTIFACTS, "reports"),
    "edge_cases": os.path.join(ROOT_ARTIFACTS, "edge_cases"),
    "edge_cases_examples": os.path.join(ROOT_ARTIFACTS, "edge_cases", "examples"),
    "edge_cases_visuals": os.path.join(ROOT_ARTIFACTS, "edge_cases", "visuals"),
    "ab_comparisons": os.path.join(ROOT_ARTIFACTS, "ab_comparisons"),
    "final_deliverable": f"d:/aero/artifacts/final_deliverable_{TIMESTAMP}/",
    "signoff": f"d:/aero/artifacts/final_deliverable_{TIMESTAMP}/SIGNOFF_PACKAGE/"
}

# --- NATURAL & PHYSICAL CONSTANTS ---
CONSTANTS = {
    "gravitational_acceleration": 9.80665,
    "speed_of_sound_sea_level": 340.29,
    "standard_atm_pressure": 101325,
    "gas_constant_air": 287.058
}

PHYSICS_RANGES = {
    "Aluminum": [2500, 2900],
    "Titanium": [4400, 4700],
    "Carbon Fiber": [1500, 1800],
    "Steel": [7700, 8000]
}

# --- PIPELINE CONFIG ---
DEFAULT_SEEDS = [11, 42, 123]
SAMPLE_SIZES = [300, 600, 1000, 5000] # Ensure 600 is present
TARGET_EDGE_CASE_EXAMPLES = 50

# --- MODELS & GRIDS ---
GENUITY_MODELS = ["TVAE", "CTGAN", "TabuDiff", "Copula", "MaskedPredictor", "DP_TVAE"]
BASELINE_MODELS = ["GMM", "KDE", "Empirical"]
ALL_MODELS = GENUITY_MODELS + BASELINE_MODELS

HYPERPARAM_GRIDS = {
    "CTGAN": {
        "epochs": [500, 1000, 2000,5000],
        "batch_size": [64, 128, 256, 512],
        "embedding_dim": [64, 128, 256]
    },
    "TVAE": {
        "latent_dim": [16, 32, 64, 128],
        "epochs": [500, 1000, 2000,5000]
    },
    "TabuDiff": {
        "timesteps": [25, 50, 100, 200],
        "model_dim": [64, 128]
    },
    "Copula": {
        "regularization": [0.0, 0.001, 0.01, 0.1]
    },
    "MaskedPredictor": {
        "mask_rate": [0.10, 0.15, 0.25, 0.35]
    },
    "DP_TVAE": {
        "epsilon": [0.1, 0.5, 1.0, 2.0]
    },
    "GMM": {
        "n_components": [3, 5, 8, 12],
        "covariance_type": ["full", "tied", "diag"]
    },
    "KDE": {
        "bandwidth": [0.1, 0.5, 1.0, "scott"]
    }
}

DEFAULT_SCORING = {
    "statistical_similarity": 0.30,
    "ml_utility": 0.25,
    "correlation_preservation": 0.15,
    "physics_consistency": 0.20,
    "privacy_detectability": 0.10
}

# Create dirs
for k, path in DIRS.items():
    os.makedirs(path, exist_ok=True)
