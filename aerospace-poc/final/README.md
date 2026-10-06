# Aerospace Structural Design — Synthetic Data Generation Project

## Overview

A comprehensive synthetic data generation and validation pipeline for an aerospace structural design dataset. Uses the **Genuity** library to generate, evaluate, and compare synthetic datasets across 9 generative model variants.

**Dataset:** 300 real rows × 22 features → generates 300/600/1000-row synthetic datasets
**Models:** CTGAN, CTGANPremium, TVAE, TVAEPremium, TabuDiff, TabuDiffPremium, Copula, MaskedPredictor, DP-TVAE, DP-TVAEPremium, Empirical
**GPU:** RTX 4050 Laptop (CUDA 12.4) via `torch==2.6.0+cu124`

---

## Project Structure

```
d:\aero\final\
├── README.md                          ← This file
├── requirements.txt                   ← Python dependencies
├── run_all.py                         ← Master runner (runs full pipeline)
│
├── generate_all_models.py             ← Generate all 27 base synthetic datasets
├── run_premium_genuity_models.py      ← GPU-accelerated premium model experiments
├── full_validation_pipeline.py        ← Tier 1 + Tier 2 validation on all datasets
├── build_data_analysis_report.py      ← Generates data_analysis_report.md + 14 plots
│
├── per_model_datasets/                ← 27+ synthetic CSVs (model_size.csv)
│   ├── empirical_300.csv / _600.csv / _1000.csv
│   ├── ctgan_300.csv / _600.csv / _1000.csv
│   ├── ctgan_premium_300/600/1000.csv
│   ├── tvae_300/600/1000.csv
│   ├── tvae_premium_300/600/1000.csv
│   ├── tabudiff_300/600/1000.csv
│   ├── tabudiff_premium_300/600/1000.csv
│   ├── copula_300/600/1000.csv
│   ├── maskedpredictor_300/600/1000.csv
│   ├── dp_tvae_300/600/1000.csv
│   └── dp_tvae_premium_eps*.csv
│
├── synthetic_data/                    ← Final deliverable datasets
│   ├── synthetic_aerospace_data.csv   ← Best overall (winner)
│   ├── balanced_1000.csv              ← Class-balanced version
│   └── feature_engineered_1000.csv   ← +12 engineered features (34 cols)
│
├── edge_cases/                        ← 27 stress scenario datasets (50 rows each)
│   ├── edge_case_*.csv               ← Individual scenarios
│   ├── all_edge_cases_combined.csv   ← All 1350 rows combined
│   ├── edge_case_catalog.md          ← Scenario descriptions + metrics
│   └── edge_case_analysis.py         ← Analysis script
│
├── experiments/                       ← Experimental run metadata
│   ├── all_experiments.csv            ← All ~108 run metrics
│   ├── premium_experiments.csv        ← Premium model run results
│   ├── real_train_split.csv           ← 80% real data (for TRTS)
│   └── real_test_split.csv            ← 20% real data (held-out)
│
├── reports/                           ← All Markdown reports
│   ├── data_analysis_report.md        ← Flagship: 12-chapter EDA (40+ pages)
│   ├── business_narrative_report.md   ← Business intelligence report
│   ├── model_comparison_report.md     ← Model benchmarking leaderboard
│   ├── genuity_library_showcase.md    ← Genuity library documentation
│   ├── genuity_technical_paper.md     ← Academic-style technical paper
│   ├── winner_declaration.md          ← Best model declaration + justification
│   ├── edge_case_report.md            ← Edge case stress test framing
│   └── plots/                         ← All generated PNG plots (60+ files)
│
├── validation_reports/                ← Per-model Tier 1+2 validation reports
│   └── {model}_{size}_validation.md  ← 27 reports
│
├── models/                            ← Predictive model training
│   ├── predictive_models.py           ← 7 classifiers × 4 targets
│   └── predictive_model_report.md     ← Results + multi-output analysis
│
├── balancing/                         ← Class balancing experiments
│   ├── class_balancing.py             ← 4 strategies compared
│   └── class_balancing_report.md      ← Results + winner
│
└── feature_engineering/               ← Feature engineering
    ├── feature_engineering_report.md  ← VIF, PCA scree, accuracy delta
    └── feature_engineering.py         ← 12 engineered features
```

---

## Quick Start

### 1. Install dependencies

```bash
# GPU environment (recommended)
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

# Install genuity from local source
pip install -e d:\aero\
```

### 2. Run everything

```bash
cd d:\aero\final
python run_all.py
```

This runs the full pipeline in order:
1. Tier 1 validation on all existing datasets
2. Full Tier 2 validation on best dataset
3. All report generation
4. Feature engineering + predictive models

### 3. Run only specific components

```bash
# Generate premium models (GPU required)
"/d/head counting software/.venv/Scripts/python.exe" run_premium_genuity_models.py

# Generate data analysis report + plots
python build_data_analysis_report.py

# Run full validation pipeline
python full_validation_pipeline.py

# Run predictive models
python models/predictive_models.py

# Run class balancing comparison
python balancing/class_balancing.py

# Run edge case analysis + catalog
python edge_cases/edge_case_analysis.py
```

---

## Dataset Schema

| Feature | Type | Range / Values |
|---|---|---|
| Material Type | Categorical | Aluminum, Titanium, Carbon Fiber |
| E (GPa) | Numeric | 50.1 – 199.8 |
| ν (Poisson) | Numeric | 0.30 – 0.35 |
| ρ (kg/m³) | Numeric | 1,521 – 4,496 |
| Tensile Strength (MPa) | Numeric | 261 – 1,496 |
| Young's Modulus | Numeric | 50 – 99.6 |
| Altitude (m) | Numeric | 5,086 – 19,963 |
| Temperature (°C) | Numeric | −60 to −40 |
| Pressure (Pa) | Numeric | 100,172 – 199,839 |
| Operational Life (years) | Integer | 20 – 39 |
| Wing Span (m) | Numeric | 20 – 59.7 |
| Fuselage Length (m) | Numeric | 30 – 70 |
| Structural Thickness (mm) | Numeric | 5 – 14.9 |
| Structural Shape | Categorical | Rectangular, Cylindrical, Tapered |
| Load Distribution | Categorical | uniform, point load, distributed |
| Quantum Algorithm Type | Categorical | Chaotic Quantum Genetic, Shark Optimizer |
| Number of Iterations | Integer | 523 – 1,983 |
| Optimization Time (sec) | Numeric | 51.5 – 149.8 |
| **Vibration Damping** | **Target** | Low, Moderate, High |
| **Computational Time** | **Target** | Short, Medium, Long |
| **Weight Efficiency** | **Target** | Poor, Good, Excellent |
| **Durability** | **Target** | Low, Medium, High |

---

## Model Results Summary

| Model | TSTR (1000-row) | KS Pass Rate | Notes |
|---|---|---|---|
| Empirical | ~0.95 | ~0.95 | Direct resampling — upper bound baseline |
| TabuDiff Premium | 0.3892 | — | Best TSTR among generative models |
| Copula | 0.3442 | **0.9286** | Best KS — preserves marginal distributions |
| CTGANPremium | 0.3508 | — | spectral_norm + gradient_penalty |
| DP-TVAE Premium | 0.3533 | — | ε=1.0; privacy-preserving |

---

## GPU Requirements

| Component | Spec |
|---|---|
| GPU | NVIDIA GeForce RTX 4050 Laptop |
| VRAM | 6.4 GB |
| CUDA | 12.4 |
| PyTorch | 2.6.0+cu124 |
| Python env | `/d/head counting software/.venv/` |

---

## Expected Outputs

After a full run:
- **27+ synthetic CSVs** in `per_model_datasets/`
- **3 final datasets** in `synthetic_data/`
- **27 edge case CSVs** + catalog in `edge_cases/`
- **7 major reports** in `reports/`
- **27 validation reports** in `validation_reports/`
- **60+ plots** in `reports/plots/`
- **108+ experiment rows** in `experiments/all_experiments.csv`

---

*Aerospace Synthetic Data Project — Genuity v1.0.0*
