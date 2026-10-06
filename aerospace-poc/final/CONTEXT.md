# CONTEXT.md — Aerospace Synthetic Data Project
**Purpose:** Capture every important finding so no future session rediscovers anything.
**Last Updated:** 2026-03-18 | Session 0

---

## 1. ORIGINAL DATASET

**File:** `d:/aero/aerospace_structural_design_dataset.csv`
**Shape:** 300 rows × 22 columns | **Zero nulls** | **No PII**

### 1.1 Numeric Columns (14)
| Column | Range | Notes |
|---|---|---|
| E (GPa) | 50.1 – 199.8 | Tri-modal: Al 50–100, Ti 100–150, CF 150–200 |
| Poisson's Ratio (ν) | 0.30 – 0.35 | Very tight range |
| Density (ρ) (kg/m³) | 1521 – 4496 | Tri-modal by material |
| Tensile Strength (MPa) | 261 – 1496 | Tri-modal by material |
| Young's Modulus | 50 – 99.6 | Redundant with E (GPa) but different scale |
| Altitude (m) | 5086 – 19963 | |
| Temperature (°C) | -60 to -40 | Very tight range |
| Pressure (Pa) | 100172 – 199839 | |
| Operational Life (years) | 20 – 39 | |
| Wing Span (m) | 20 – 59.7 | |
| Fuselage Length (m) | 30 – 70 | |
| Structural Thickness (mm) | 5 – 14.9 | |
| Number of Iterations | 523 – 1983 | |
| Optimization Time (sec) | 51.5 – 149.8 | |

### 1.2 Categorical Columns (8)
| Column | Levels |
|---|---|
| Material Type | Aluminum, Carbon Fiber, Titanium |
| Structural Shape | Cylindrical, Rectangular, Tapered |
| Load Distribution | distributed, point load, uniform |
| Vibration Damping | High, Low, Moderate |
| Computational Time | Long, Medium, Short |
| Weight Efficiency | Excellent, Good, Poor |
| Durability | High, Low, Medium |
| Quantum Algorithm Type | Chaotic Quantum Genetic, Shark Optimizer |

### 1.3 Physics Constraints (Material → Property Correlations)
- **Material Type → E (GPa), ρ, Tensile Strength** are tightly coupled
- Aluminum: E ≈ 50–100, ρ ≈ 2500–2900, Tensile ≈ 261–600
- Titanium: E ≈ 100–150, ρ ≈ 4400–4700, Tensile ≈ 800–1100
- Carbon Fiber: E ≈ 150–200, ρ ≈ 1500–1800, Tensile ≈ 1000–1500
- These tight correlations cause mode collapse in neural generative models

### 1.4 Column Name Quirks
- **Curly apostrophe:** `Young's Modulus` uses U+2019 (`'`) in the CSV header — must normalize:
  ```python
  df.columns = [c.replace('\u2019', "'").replace('\u2018', "'") for c in df.columns]
  ```
- **Target column prefixes vary by model:**
  - Original CSV: no prefix (e.g., `Vibration Damping`)
  - Genuity TVAE/TabuDiff/MaskedPredictor output: adds `Target - ` prefix
  - 5000-row gold dataset: uses em-dash `Target — ` and adds `(Poisson)` to ν
  - DP-TVAE: reorders columns entirely
- **Standardization rename map** (used in run_sdv_models.py):
  ```python
  if 'Vibration' in c:     rename[c] = 'Vibration Damping'
  elif 'Computational' in c: rename[c] = 'Computational Time'
  elif 'Weight' in c and ('Eff' in c or 'eff' in c): rename[c] = 'Weight Efficiency'
  elif 'Durability' in c:  rename[c] = 'Durability'
  ```

---

## 2. GENUITY LIBRARY (v1.0.0)

### 2.1 API Patterns (from `d:\aero\DOCUMENTATION.md`)

| Model | Input | Key Detail |
|---|---|---|
| CTGANAPI | numpy float32 array + integer col indices + output_info | Filter to continuous+categorical ONLY (exclude outlier_flags, PCA) |
| TVAEAPI | Raw DataFrame directly | Internal MinMaxScaler + OneHotEncoder — causes mode collapse on multi-modal |
| TabuDiffBasicAPI | `pre_output["preprocessed"].values` (numpy) | Pass full preprocessed numpy |
| TabuDiffPremiumAPI | Same as Basic | GPU required — RTX 4050 (6.4GB VRAM) |
| CopulaAPI | Full preprocessed numpy + copula indices | `pretransformed=True` |
| MaskedPredictorAPI | `pre_output["preprocessed"]` DataFrame (NOT numpy) | `generate()` returns same-size output |
| DifferentialPrivacyProcessor | Apply to RAW data BEFORE preprocessing | Methods: minimal, laplace, gaussian |

### 2.2 Preprocessing Workflow
```python
preprocessor = TabularPreprocessor(verbose=False, n_pca_components=0)
pre = preprocessor.fit_transform(df)
# pre['continuous']  — continuous features only
# pre['categorical'] — categorical features only
# pre['preprocessed'] — full preprocessed (continuous + categorical + metadata)
output_info = preprocessor.get_output_info()
```

### 2.3 Postprocessing
```python
post = TabularPostprocessor(preprocessor_object=preprocessor, verbose=False)  # keyword required!
result = post.inverse_transform_modified_data(df_raw)
```

### 2.4 Premium Features
- CTGANPremium: spectral_norm, gradient_penalty
- TVAEPremium: vamp_prior, cyclical_annealing
- TVAEPremium **BROKEN**: numpy ufunc error (Int64 vs string in align_clip) — consistently fails

---

## 3. SDV LIBRARY (v1.34.3)

### 3.1 Why SDV
SDV uses **BGM (Bayesian Gaussian Mixture)** per-column normalization — detects material modes, normalizes each separately → prevents the mode collapse that Genuity's MinMaxScaler causes.

### 3.2 SDV API Pattern
```python
from sdv.single_table import CTGANSynthesizer, TVAESynthesizer, GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

meta = SingleTableMetadata()
meta.detect_from_dataframe(df)
synth = CTGANSynthesizer(metadata=meta, epochs=300, verbose=False)
synth.fit(df)
syn = synth.sample(n)
```

### 3.3 SDV Results (excellence_results.csv)
| Model | Best Composite | KS | TSTR | Verdict |
|---|---|---|---|---|
| SDV Copula | 0.74–0.78 | 0.857–0.929 | 0.32 | Best generative for KS |
| SDV CTGAN | 0.38–0.42 | 0.071–0.143 | 0.35 | Still poor KS |
| SDV TVAE | 0.35–0.40 | 0.071–0.143 | 0.30 | Still poor KS |
| TabuDiff | 0.43–0.50 | 0.46 | 0.35 | Moderate |

---

## 4. KNOWN FAILURES & ROOT CAUSES

### 4.1 Mode Collapse (CTGAN, TVAE, CTGANPremium, TVAEPremium)
- **Root cause:** 300-row physics-constrained data with tri-modal distributions (3 materials)
- CTGAN generates constant values (GAN mode collapse)
- TVAE generates E (GPa) in [118, 130] vs real [50, 199] (posterior collapse to mean)
- Even SDV's BGM only partially helps — KS still 0.07–0.14 for CTGAN/TVAE
- **Fundamental limitation:** 300 rows is insufficient for deep generative models on physics-constrained joint distributions

### 4.2 TVAEPremium numpy ufunc Error
- Consistently fails with type mismatch (Int64 vs string) during `align_clip`
- Logged in `premium_models.log`

### 4.3 DP-TVAE Double Penalty
- DP noise + TVAE collapse = worst performance (composite 0.22)
- Fix: Apply DP to raw data FIRST, then use SDV TVAE (not Genuity TVAE)

### 4.4 Windows Encoding
- Unicode characters (→, −, ≈, ν, ρ) cause `UnicodeEncodeError` on Windows cp1252
- **Fix:** Add at top of every script:
  ```python
  import sys, io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
  ```

---

## 5. EXPERIMENT HISTORY

### 5.1 72-Run Baseline (from `d:\aero\` parent)
- **Config:** 6 models × 3 seeds (11, 42, 123) × 4 sizes (300, 600, 1000, 5000)
- **Models:** Empirical, KDE, GMM, Copula, TabuDiff, MaskedPredictor
- **Best:** Empirical seed=11 size=5000 composite=0.9969
- **File:** `experiments/all_metrics_72runs.csv` (72 rows)

### 5.2 Top 10 Runs
| Rank | Model | Seed | Size | Composite |
|---|---|---|---|---|
| 1 | Empirical | 11 | 5000 | 0.9969 |
| 2 | KDE | 123 | 5000 | 0.9965 |
| 3 | KDE | 42 | 5000 | 0.9963 |
| 4 | Empirical | 42 | 5000 | 0.9952 |
| 5 | Empirical | 123 | 5000 | 0.9941 |

### 5.3 Optuna HPO Results (51 files in `experiments/optuna/`)
| Model | Trials | Best Composite | Best Config |
|---|---|---|---|
| CTGAN | 3 | 0.4201 | batch=64, embed=64, epochs=500 |
| TabuDiff | 3 | 0.7952 | plateau |
| Copula | 6 | 0.8261 | reg=0.1 |

### 5.4 Significance Testing
- Empirical vs KDE paired bootstrap n=10000:
  - mean_diff=0.1110, CI=[0.0945, 0.1262], p=0.0000, Cohen's d=8.34

### 5.5 Premium Model Results (`experiments/premium_experiments.csv`, 13 rows)
| Model | KS | TSTR | Notes |
|---|---|---|---|
| copula | 0.9286 | — | Best KS of any model |
| tabudiff_premium | — | 0.3892 | GPU-trained |
| ctgan_premium | 0.0 | 0.35 | Mode collapse |
| TVAEPremium | FAILED | — | numpy ufunc error |

### 5.6 SDV Excellence Run (`experiments/excellence_results.csv`, 28 rows)
- 8 model variants × 3 sizes (300, 600, 1000) + existing copula evaluations
- Best non-empirical generative: Copula (composite 0.74–0.78)

---

## 6. COMPOSITE SCORE FORMULA

### 6.1 Config-Level Weights (from `config.py`)
```python
DEFAULT_SCORING = {
    "statistical_similarity": 0.30,
    "ml_utility": 0.25,
    "correlation_preservation": 0.15,
    "physics_consistency": 0.20,
    "privacy_detectability": 0.10
}
```

### 6.2 run_sdv_models.py Composite
```python
stat_sim = max(0, ks_rate * 0.8 + corr * 0.2)
composite = 0.30 * stat_sim + 0.25 * tstr + 0.20 * corr + 0.15 * ks_rate + 0.10 * stat_sim
```

### 6.3 Physics Ranges (from `config.py`)
```python
PHYSICS_RANGES = {
    "Aluminum": [2500, 2900],   # density kg/m³
    "Titanium": [4400, 4700],
    "Carbon Fiber": [1500, 1800],
    "Steel": [7700, 8000]       # not in dataset
}
```

---

## 7. KEY FILE INVENTORY

### 7.1 Scripts (16 total)
| File | Lines | Purpose | Status |
|---|---|---|---|
| `run_sdv_models.py` | 288 | SDV + Genuity generation, 8 models × 3 sizes | CREATED, RAN |
| `run_all_models_excellence.py` | 564 | Genuity-first + SDV fallback | CREATED, READY |
| `full_validation_pipeline.py` | 836 | Tier 1+2 validation, reports, plots | EXISTS |
| `build_data_analysis_report.py` | 250+ | EDA plots + data analysis report | EXISTS |
| `create_balanced_dataset.py` | 140 | Sequential conditional oversampling | EXISTS |
| `create_feature_engineered_dataset.py` | 331 | 12 engineered features + VIF + PCA | EXISTS |
| `models/predictive_models.py` | 150+ | 7 classifiers × 4 targets | EXISTS |
| `balancing/class_balancing.py` | 150+ | 4 strategies: baseline/conditional/undersample/SMOTE-NC | EXISTS |
| `edge_cases/edge_case_analysis.py` | 150+ | 27 stress scenarios, IF/LOF/NN scoring | EXISTS |
| `run_premium_genuity_models.py` | 323 | GPU premium models | EXISTS |
| `config.py` (root) | 91 | Global config, paths, grids | EXISTS |
| `evaluator.py` (root) | 74 | Composite scorer via genuity.evaluation | EXISTS |

### 7.2 Reports (12 total in `reports/`)
| File | Lines | Quality | Notes |
|---|---|---|---|
| `explainability_report.md` | 1,611 | HIGH | 50-section comprehensive |
| `business_narrative_report.md` | 869 | HIGH | Engineering intelligence |
| `model_comparison_report.md` | 853 | HIGH | 31 experiments leaderboard |
| `hyperparameter_optimization_report.md` | 456 | GOOD | Optuna CTGAN/TabuDiff/Copula |
| `genuity_library_showcase.md` | 443 | GOOD | API reference + benchmarks |
| `data_analysis_report.md` | 431 | GOOD | 12-chapter EDA |
| `genuity_technical_paper.md` | 429 | GOOD | Academic-style |
| `winner_declaration.md` | 147 | OK | empirical_1000 winner |
| `executive_report.html` | 179KB | HIGH | Client-facing |
| `benchmarking_report.html` | 13KB | GOOD | Technical |
| `full_report.pdf` | 602KB | HIGH | Print deliverable |
| `edge_case_report.md` | 68 | STUB | Needs major expansion |

### 7.3 Datasets in `per_model_datasets/` (37 CSVs)
- Genuity originals: copula_{300,600,1000}, ctgan_{300,600,1000}, ctgan_premium_{300,600,1000}, dp_tvae_{300,600,1000}, masked_predictor_{300,600,1000}, tabudiff_{300,600,1000}, tabudiff_premium_{300,600,1000}, tvae_{300,600,1000}
- SDV additions: sdv_ctgan_{300,600,1000}, sdv_tvae_{300,600,1000}, sdv_copula_{300,600,1000}, sdv_dp_tvae_{300,600,1000}
- Some Genuity files have "Target - " prefixed columns; SDV files have clean columns

### 7.4 Plots (202 PNGs across `reports/plots/`)
- `model_comparison/` — 44 PNGs (side-by-side distributions, scatter, etc.)
- `explainability/` — 72+ PNGs (SHAP, feature importance, per-model)
- `statistical/` — 31 PNGs (distribution overlays, QQ plots)
- `summary/` — summary dashboards
- `scale_analysis/` — size scaling analysis

### 7.5 Other Key Files
- `experiments/all_experiments.csv` — 18 rows, current experiment tracker
- `experiments/all_metrics_72runs.csv` — 72 rows from parent 72-run
- `experiments/excellence_results.csv` — 28 rows from SDV run
- `experiments/premium_experiments.csv` — 13 rows premium models
- `experiments/top10_runs.csv` — top 10 from 72-run
- `experiments/significance_tests.json` — bootstrap significance results
- `edge_cases/edge_case_catalog.csv` — 27 scenarios
- `edge_cases/` — 27 individual edge case CSVs
- `validation_reports/` — 24 per-dataset validation reports
- `synthetic_data/best_synthetic_empirical_seed11_n5000.csv` — 5000-row gold
- `synthetic_data/balanced_1000.csv` — class-balanced dataset
- `notebooks/aerospace_synthesis_analysis.ipynb` — Jupyter notebook
- `IMPLEMENTATION_PLAN.md` — prior implementation plan (192 lines)

---

## 8. GPU ENVIRONMENT

- **GPU:** NVIDIA RTX 4050 Laptop, 6.4GB VRAM
- **CUDA:** 12.4
- **PyTorch:** 2.6.0+cu124
- **Python with GPU:** `/d/head counting software/.venv/Scripts/python.exe`
- **SDV:** v1.34.3 (installed)
- **Genuity:** v1.0.0 (custom library at `d:/aero/genuity/`)

---

## 9. DELIVERABLES SPECIFICATION (User-Provided)

### Section 1: Datasets (8 categories)
1. **Core Synthetic** — 9 models × 3 sizes = 27 CSVs in `per_model_datasets/`
2. **Class-Balanced** — balanced versions for each model+size
3. **Edge Case** — stress-tested variants (27 scenarios)
4. **Feature-Engineered** — 12 engineered features per dataset
5. **Evaluation Splits** — train/test/validation splits
6. **Experimental Tracking** — all_experiments.csv, per-run metrics
7. **Anomaly/Outlier** — anomaly scores, outlier flags per dataset
8. **Discriminator/Similarity** — real-vs-synthetic discriminator scores

### Section 2: Reports (22 types)
1. Deep Data Analysis Report
2. Model Comparison Report
3. Explainability Report
4. Hyperparameter Optimization Report
5. Winner Declaration Report
6. Genuity Technical Paper
7. Genuity Library Showcase
8. Business Narrative Report
9. Edge Case Report
10. Validation Report (per-model)
11. Privacy & Compliance Report
12. Feature Engineering Report
13. Predictive Modeling Report
14. Class Balancing Report
15. Scale Analysis Report
16. Conditional Probability Report
17. Domain Constraint Validation Report
18. Reproducibility Report
19. Executive Summary (HTML)
20. Benchmarking Report (HTML)
21. Full Technical Report (PDF)
22. Model Card (per model)

### Section 3: Visualizations
- Distribution overlays, correlation heatmaps, QQ plots, PCA/t-SNE/UMAP
- Per-model comparison dashboards
- Scale analysis (300 vs 600 vs 1000)
- Edge case visualization
- SHAP/feature importance plots

---

*This file must be updated whenever significant new findings emerge.*
