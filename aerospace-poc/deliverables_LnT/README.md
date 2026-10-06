# Aerospace Synthetic Data Generation Pipeline



## What This Project Does

Takes a **300-row Kaggle aerospace structural design dataset** and builds a complete, validated synthetic data generation pipeline that:

- **Benchmarks 9 generative models** (KDE, GMM, Copula, TVAE, CTGAN, TabuDiff, MaskedPredictor, and Premium variants) across 92 experimental configurations
- **Enforces physics constraints** — fatigue ratios, tensile strength bounds, material density ranges, ISA atmosphere validation
- **Generates production-ready synthetic datasets** up to 5,000 rows with near-perfect fidelity (composite score 0.9965)
- **Validates rigorously** using a 6-axis evaluation framework: physics consistency, statistical similarity, ML utility, correlation preservation, KS/KL divergence, and privacy/detection risk
- **Produces 7 comprehensive PDF reports** with LaTeX sources covering every angle — from executive summary to deep statistical analysis

---

## Key Results at a Glance

| Metric | Best Result | Model |
|--------|------------|-------|
| Composite Score | **0.9965** | KDE (n=5000) |
| TSTR F1 (ML Utility) | **1.000** | KDE |
| MMD (Indistinguishability) | **0.0003** | KDE |
| Discriminator AUC | **0.478** (near-chance = ideal) | KDE |
| Physics Repair Triggers | **0** | KDE |
| Edge Case Realism | **91% mean** (30 scenarios) | All models |

**Verdict:** Statistical models (KDE, GMM, Copula) decisively outperform deep learning approaches (TVAE, CTGAN, TabuDiff) on this 300-row dataset — achieving >96% indistinguishability with zero memorization.

---

## Project Structure

```
final_LnT/
│
├── README.md                    ← You are here
├── LnT_POC_structure.md         ← Full project highlights (technical + business)
├── PROJECT_SUMMARY.md           ← Detailed technical summary
├── DIRECTORY_GUIDE.md           ← Complete directory map with file descriptions
│
├── reports/                     ← 7 PDF reports + LaTeX sources
│   ├── executive_summary.pdf    ← 1-page overview (start here)
│   ├── deep_data_analysis/      ← Full EDA, distributions, correlations
│   ├── business_narrative/      ← Material selection, risk flags, engineering insights
│   ├── model_comparison/        ← 9-model benchmarking, radar charts, scale analysis
│   ├── feature_interdependency/ ← Correlation preservation (Frobenius norm, spectral)
│   ├── io_coherence/            ← Input-Output causal fidelity, SHAP alignment
│   ├── class_balance_edge/      ← Class balancing strategies + edge case validation
│   └── similarity_innovation/   ← TSTR/TRTS, MMD, discriminator AUC, bootstrap CIs
│
├── synthetic_data/              ← 112 generated datasets
│   ├── best_per_model/          ← 9 files — single best per model
│   ├── top_10/                  ← Top 10 overall (ranked) + index CSV
│   └── experimentations/        ← 92 raw experimental run CSVs
│
├── explainable_graphs/          ← 294 visualizations across 11 categories
│   ├── graph_catalog.csv        ← Master index with descriptions
│   ├── 01_univariate/           ← Histograms, KDE plots, boxplots
│   ├── 02_bivariate/            ← Scatter grids, correlation heatmaps
│   ├── 03_synthetic_vs_real/    ← Distribution overlays per model
│   ├── 04_target_analysis/      ← Class distributions, grouped statistics
│   ├── 05_validation_metrics/   ← KS/KL/Wasserstein heatmaps, ROC curves
│   ├── 06_feature_importance/   ← SHAP + Random Forest rankings
│   ├── 07_model_performance/    ← Leaderboard, radar, composite charts
│   ├── 08_edge_cases/           ← LOF distributions, realism scores
│   ├── 09_feature_engineering/  ← VIF, PCA scree, accuracy delta
│   ├── 10_dimensionality_reduction/ ← PCA/t-SNE overlays (all 9 models)
│   └── 11_report_figures/       ← Figures embedded in PDF reports
│
├── anomaly_outlier/             ← Isolation Forest + LOF analysis
├── class_balanced/              ← SMOTE-NC, undersampling results
├── discriminator_similarity/    ← RF discriminator, MMD, PCA/t-SNE
├── edge_cases/                  ← 30 edge case scenarios + realism scores
└── feature_engineering/         ← Derived features, VIF, importance rankings
```

---

## How to Navigate This Deliverable

| If you want to... | Go to... |
|-------------------|----------|
| Get a 1-page overview | `reports/executive_summary.pdf` |
| Understand every highlight | `LnT_POC_structure.md` |
| See the full technical depth | `PROJECT_SUMMARY.md` |
| Find a specific file | `DIRECTORY_GUIDE.md` |
| Compare all 9 models | `reports/model_comparison/` |
| Use the best synthetic data | `synthetic_data/best_per_model/KDE_s123_n5000_r035.csv` |
| Browse all visualizations | `explainable_graphs/graph_catalog.csv` |
| Check physics validity | `anomaly_outlier/` + `edge_cases/` |

---

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Core Language | Python 3.x |
| Generative Models | Genuity 1.0.0 (TVAE, CTGAN, TabuDiff, Copula, MaskedPredictor), scikit-learn (KDE, GMM) |
| Hyperparameter Optimization | Optuna (multi-trial, multi-seed) |
| Evaluation Metrics | KS-test, KL divergence, MMD, TSTR/TRTS, SHAP, Isolation Forest, LOF |
| Visualization | Matplotlib, Seaborn, Plotly (294 graphs) |
| Reporting | LaTeX (tectonic compiler), 7 PDFs |
| Physics Validation | Custom domain constraints (ISA atmosphere, material property bounds) |

---

## Evaluation Framework (6-Axis Composite Scoring)

Each synthetic dataset is scored on a weighted composite of:

| Axis | Weight | What It Measures |
|------|--------|-----------------|
| Physics Consistency | 20% | Per-row constraint validity, range checks, correlation consistency |
| Statistical Similarity | 30% | KL divergence across all numeric feature distributions |
| ML Utility | 25% | TSTR — train on synthetic, test on real (Random Forest F1) |
| Correlation Preservation | 15% | Frobenius norm of correlation matrix difference |
| Privacy / Detection Risk | 10% | Discriminator AUC (0.5 = undetectable = ideal) |

---

## Model Tier Rankings

### Tier 1 — Production Ready
| Model | Composite | Discriminator AUC | Strength |
|-------|-----------|-------------------|----------|
| **KDE** | **0.9965** | 0.478 | Highest fidelity, zero repair triggers |
| **GMM** | 0.9658 | 0.451 | 90.2% indistinguishable |
| **Copula** | 0.9625 | 0.518 | 96.5% indistinguishable, best dependency preservation |

### Tier 2 — Research Interest
| Model | Composite | Note |
|-------|-----------|------|
| TabuDiff | 0.9425 | Moderate MMD, promising for larger datasets |

### Tier 3 — Not Recommended
| Model | Issue |
|-------|-------|
| TVAE / TVAEPremium | Class collapse, AUC ~1.0 (memorization) |
| CTGANPremium | 0% anomaly rate (pure memorization) |
| MaskedPredictor | High variance, architecture-limited |

---

> **Best synthetic dataset:** `synthetic_data/best_per_model/KDE_s123_n5000_r035.csv`
> 5,000 rows | Composite 0.9965 | TSTR F1 1.000 | MMD 0.0003 | 0 physics violations

---

*736 files | 157 MB | 9 models | 92 experiments | 294 visualizations | 7 PDF reports*
