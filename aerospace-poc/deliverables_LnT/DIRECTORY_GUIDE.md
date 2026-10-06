# Directory Guide — Aerospace Synthetic Data Deliverable

## Quick Start

This directory (`final_LnT/`) contains the complete deliverable for the Aerospace Structural Design Dataset synthetic data generation project. Everything the client asked for — and more — is organized here.

**At a glance:**
- 736 files, ~157 MB total
- 7 PDF reports with LaTeX sources
- 112 synthetic datasets from 9 generative models
- 294 catalogued visualizations in 11 categories
- Full validation pipeline results (anomaly detection, class balancing, edge cases, discriminator tests, MMD, dimensionality reduction)

---

## Directory Map

```
final_LnT/
│
├── PROJECT_SUMMARY.md          ← Technical summary of ALL work done
├── DIRECTORY_GUIDE.md           ← You are here
│
├── reports/                     ← 7 comprehensive PDF reports
│   ├── deep_data_analysis/      ← Full EDA + statistical profiling
│   ├── business_narrative/      ← Executive-level insights & decision matrices
│   ├── model_comparison/        ← 9-model benchmarking + scale analysis
│   ├── feature_interdependency/ ← Correlation preservation across models
│   ├── io_coherence/            ← Input→Output causal fidelity checks
│   ├── class_balance_edge/      ← Class balance + edge case validation
│   └── similarity_innovation/   ← TSTR/MMD/discriminator + bootstrap CIs
│
├── synthetic_data/              ← All generated synthetic datasets
│   ├── best_per_model/          ← 9 files — single best dataset per model
│   ├── top_10/                  ← Top 10 overall (all KDE) + index CSV
│   └── experimentations/        ← 92 full experimental runs
│
├── explainable_graphs/          ← 294 organized visualizations + catalog
│   ├── graph_catalog.csv        ← Master index: filename, category, description
│   ├── 01_univariate/           ← Histograms, KDE plots, boxplots (42 files)
│   ├── 02_bivariate/            ← Scatter grids, correlations, radar (22 files)
│   ├── 03_synthetic_vs_real/    ← Distribution comparisons per model (79 files)
│   ├── 04_target_analysis/      ← Target variable distributions (31 files)
│   ├── 05_validation_metrics/   ← KS/KL/Wasserstein/ROC/MMD/anomaly (21 files)
│   ├── 06_feature_importance/   ← SHAP, RF importance rankings (10 files)
│   ├── 07_model_performance/    ← Leaderboard, radar, scale charts (31 files)
│   ├── 08_edge_cases/           ← Edge case realism visualizations (4 files)
│   ├── 09_feature_engineering/  ← VIF, PCA scree, accuracy delta (4 files)
│   ├── 10_dimensionality_reduction/ ← PCA/t-SNE overlays (36 files)
│   └── 11_report_figures/       ← All figures from 7 PDF reports (36 files)
│
├── feature_engineering/         ← 12 engineered features + analysis (Bonus — beyond client scope)
│   ├── real/                    ← Applied to original 300-row dataset
│   │   ├── datasets/            ← full_feature_engineered.csv, pca_augmented.csv, etc.
│   │   ├── visuals/             ← VIF, importance, PCA plots
│   │   ├── feature_engineering_report.md
│   │   └── engineering_log.txt
│   └── kde_synthetic/           ← Applied to KDE synthetic data
│       ├── datasets/
│       ├── visuals/
│       └── feature_engineering_report.md
│
├── class_balanced/              ← Balancing strategy evaluation
│   ├── real/                    ← SMOTE-NC, ADASYN, undersampling on real data
│   │   ├── best_balanced.csv
│   │   ├── balancing_evaluation.csv
│   │   └── per_target_*.csv     ← Per-target balanced datasets (4 files)
│   └── kde_synthetic/           ← Same strategies on KDE synthetic data
│
├── edge_cases/                  ← 30 edge case scenarios
│   ├── edge_case_metrics.csv    ← Realism scores for all 30 scenarios
│   ├── all_edge_cases_combined.csv
│   ├── augmented_with_edge_cases.csv
│   ├── tier1_valid_edge_cases.csv
│   ├── top5_showcase_edge_cases.csv
│   └── [27 individual scenario CSVs]
│
├── anomaly_outlier/             ← Isolation Forest + LOF analysis
│   ├── real/visuals/            ← IF/LOF score distributions for real data
│   └── synthetic/
│       ├── anomaly_summary.csv  ← Per-model anomaly rates (93 rows)
│       ├── anomalous_rows_per_model/
│       └── visuals/             ← NN distance heatmaps, violin plots
│
└── discriminator_similarity/    ← Discriminator + MMD + dim-reduction
    ├── discriminator/
    │   ├── discriminator_metrics.csv  ← AUC per model (9 rows)
    │   ├── per_model/           ← Per-model discriminator scores
    │   └── visuals/             ← ROC curves, AUC bar charts
    ├── mmd/
    │   ├── mmd_scores_all.csv   ← MMD for every experiment
    │   ├── mmd_pivot.csv        ← MMD by model × size
    │   └── visuals/             ← MMD heatmap
    └── dimensionality_reduction/
        ├── pca_coordinates_combined.csv
        ├── tsne_coordinates_combined.csv
        ├── per_model/           ← Individual PCA/t-SNE coordinates
        └── visuals/             ← PCA grid, overlay, real-vs-synthetic
```

---

## Where to Find What

| If you want to... | Go to... |
|-------------------|----------|
| **Get the 1-page overview** | `reports/executive_summary.pdf` |
| **Read the full project story** | `PROJECT_SUMMARY.md` |
| **See the best synthetic dataset** | `synthetic_data/best_per_model/KDE_s123_n5000_r035.csv` |
| **Compare all 9 models** | `reports/model_comparison/model_comparison_report.pdf` |
| **Understand the original data** | `reports/deep_data_analysis/deep_data_analysis_report.pdf` |
| **Check if synthetic data is realistic** | `discriminator_similarity/discriminator/discriminator_metrics.csv` |
| **See distribution overlap** | `discriminator_similarity/mmd/mmd_pivot.csv` |
| **View PCA/t-SNE visualizations** | `explainable_graphs/10_dimensionality_reduction/` |
| **Check class balance** | `class_balanced/real/balancing_evaluation.csv` |
| **Review edge cases** | `edge_cases/edge_case_metrics.csv` |
| **Find anomaly rates per model** | `anomaly_outlier/synthetic/anomaly_summary.csv` |
| **See feature importance** | `explainable_graphs/06_feature_importance/` |
| **Browse all graphs** | `explainable_graphs/graph_catalog.csv` (open in Excel) |
| **See engineered features** | `feature_engineering/real/feature_engineering_report.md` |
| **Get executive business insights** | `reports/business_narrative/business_narrative_report.pdf` |
| **Check input→output coherence** | `reports/io_coherence/io_coherence_report.pdf` |
| **Review feature interdependency** | `reports/feature_interdependency/feature_interdependency_report.pdf` |
| **See bootstrap confidence intervals** | `reports/similarity_innovation/similarity_innovation_report.pdf` |

---

## Reports Overview

| # | Report | File | Key Question Answered |
|---|--------|------|----------------------|
| 0 | **Executive Summary** | `reports/executive_summary.pdf` | 1-page overview: best model, key metrics, client criteria checklist |
| 1 | **Deep Data Analysis** | `reports/deep_data_analysis/deep_data_analysis_report.pdf` | What does the original data look like? (Full EDA with 27 plots) |
| 2 | **Business Narrative** | `reports/business_narrative/business_narrative_report.pdf` | What do these numbers mean for engineering decisions? |
| 3 | **Model Comparison** | `reports/model_comparison/model_comparison_report.pdf` | Which generative model is best and why? |
| 4 | **Feature Interdependency** | `reports/feature_interdependency/feature_interdependency_report.pdf` | Do synthetic models preserve feature correlations? |
| 5 | **Input-Output Coherence** | `reports/io_coherence/io_coherence_report.pdf` | Do generated targets make sense given the inputs? |
| 6 | **Class Balance & Edge Cases** | `reports/class_balance_edge/class_balance_edge_report.pdf` | Are target classes balanced? Are edge cases realistic? |
| 7 | **Similarity & Innovation** | `reports/similarity_innovation/similarity_innovation_report.pdf` | How similar is synthetic to real? (TSTR, MMD, bootstrap CIs) |

Each report directory also contains:
- `.tex` source file (LaTeX)
- `plots/` subfolder with all embedded figures
- `data/` subfolder with supporting CSV tables

---

## Key Datasets

| File | Location | Rows | Cols | Purpose |
|------|----------|------|------|---------|
| KDE_s123_n5000_r035.csv | `synthetic_data/best_per_model/` | 5,000 | 22 | **Best overall synthetic dataset** (composite 0.9965) |
| GMM_s42_n5000_r019.csv | `synthetic_data/best_per_model/` | 5,000 | 22 | Best GMM variant |
| Copula_s11_n5000_r003.csv | `synthetic_data/best_per_model/` | 5,000 | 22 | Best Copula variant |
| top_10.csv | `synthetic_data/top_10/` | 10 | 11 | Leaderboard index with all scores |
| full_feature_engineered.csv | `feature_engineering/real/datasets/` | 300 | 34 | Real data + 12 engineered features |
| best_balanced.csv | `class_balanced/real/` | 999 | 22 | SMOTE-NC balanced real data |
| edge_case_metrics.csv | `edge_cases/` | 30 | 10 | Realism scores for all 30 scenarios |
| augmented_with_edge_cases.csv | `edge_cases/` | varies | 22 | Real data + validated edge cases |
| anomaly_summary.csv | `anomaly_outlier/synthetic/` | 93 | 15 | Anomaly rates per model per experiment |
| discriminator_metrics.csv | `discriminator_similarity/discriminator/` | 9 | 5 | AUC per model |
| mmd_pivot.csv | `discriminator_similarity/mmd/` | 9 | 5 | MMD by model x scale |
| graph_catalog.csv | `explainable_graphs/` | 294 | 6 | Master index of all visualizations |

---

## Graphs & Visualizations

All 294 graphs are organized in `explainable_graphs/` by analysis type. Open `graph_catalog.csv` in Excel/Sheets for a searchable index with:
- **filename** — the PNG file name
- **source_path** — where the original was generated
- **category** — which of the 11 folders it lives in
- **subcategory** — finer grouping within the category
- **description** — what the graph shows
- **target_audience** — technical or executive

### Category Quick Reference

| Folder | What's Inside | Best For |
|--------|--------------|----------|
| `01_univariate/` | Per-feature distributions (histograms, KDE, boxplots) | Understanding individual feature shapes |
| `02_bivariate/` | Scatter grids, correlation heatmaps, material radar charts | Seeing feature relationships |
| `03_synthetic_vs_real/` | Side-by-side distribution comparisons per model | Judging synthetic quality visually |
| `04_target_analysis/` | Target class distributions, grouped statistics | Checking class balance |
| `05_validation_metrics/` | KS/KL/Wasserstein heatmaps, ROC curves, anomaly scores | Quantitative validation |
| `06_feature_importance/` | SHAP values, Random Forest rankings | Understanding what drives predictions |
| `07_model_performance/` | Leaderboard, radar charts, scale analysis | Comparing models |
| `08_edge_cases/` | LOF distributions, realism score charts | Edge case validation |
| `09_feature_engineering/` | VIF analysis, PCA scree, accuracy comparison | Feature engineering impact |
| `10_dimensionality_reduction/` | PCA/t-SNE overlays for all 9 models | Visual cluster overlap |
| `11_report_figures/` | All figures from the 7 PDF reports | Quick access to report visuals |

---

## Synthetic Data Explained

### Best Per Model (9 files)
One champion dataset per model, selected by highest composite score. Models are tiered by production readiness:

| Tier | Model | File | Size | Strengths |
|------|-------|------|------|-----------|
| **Production** | **KDE** | KDE_s123_n5000_r035.csv | 5,000 | Highest fidelity, lowest MMD, perfect TSTR |
| **Production** | **GMM** | GMM_s42_n5000_r019.csv | 5,000 | Excellent discriminator score (AUC 0.45) |
| **Production** | **Copula** | Copula_s11_n5000_r003.csv | 5,000 | Best indistinguishability (96.5%) |
| Research | **TabuDiff** | TabuDiff_s11_n5000_r051.csv | 5,000 | Best deep-learning model |
| Research | **TabuDiffPremium** | TabuDiffPremium_s11_n1000_r075.csv | 1,000 | Extended training variant |
| Evaluated | **TVAE** | TVAE_s123_n1000_r086.csv | 1,000 | Not recommended — class collapse |
| Evaluated | **TVAEPremium** | TVAEPremium_s11_n1000_r087.csv | 1,000 | Not recommended — class collapse |
| Evaluated | **CTGANPremium** | CTGANPremium_s42_n1000_r089.csv | 1,000 | Not recommended — memorization |
| Evaluated | **MaskedPredictor** | MaskedPredictor_s11_n300_r077.csv | 300 | Not recommended — high variance |

### Top 10 Overall
All 10 are KDE variants (different seeds and sizes). See `top_10/top_10.csv` for the full scored leaderboard.

### Experimentation Archive
92 raw experimental outputs archived in `experimentations.zip` (also available as individual CSVs in `experimentations/`). Naming convention: `{Model}_s{seed}_n{size}_r{rank}.csv`

---

## Validation Results Quick Reference

| Validation | Client Criterion | Where to Find It |
|-----------|-----------------|-------------------|
| **Statistical Fidelity** (Criterion 01) | Distributions, spread, skew match | `reports/deep_data_analysis/`, `explainable_graphs/03_synthetic_vs_real/` |
| **Feature Interdependencies** (Criterion 02) | Correlation structure preserved | `reports/feature_interdependency/`, `explainable_graphs/05_validation_metrics/` |
| **Input→Output Coherence** (Criterion 03) | Targets follow logically from inputs | `reports/io_coherence/`, `explainable_graphs/06_feature_importance/` |
| **Class Balance & Edge Cases** (Criterion 04) | Balanced targets, realistic rare cases | `reports/class_balance_edge/`, `class_balanced/`, `edge_cases/` |
| I/P→O/P Correlations | Correlation matrix, grouped stats | `reports/deep_data_analysis/data/correlation_*.csv` |
| Feature Structure | KS test, KL divergence, pair plots | `explainable_graphs/05_validation_metrics/` |
| Rare Case Realism | Isolation Forest, LOF, NN distance | `anomaly_outlier/`, `edge_cases/edge_case_metrics.csv` |
| Overall Similarity | TSTR/TRTS, MMD, discriminator | `reports/similarity_innovation/`, `discriminator_similarity/` |

---

## Recommended Reading Order

For someone new to this deliverable, we suggest:

1. **Quick glance** — Open `reports/executive_summary.pdf` for a 1-page overview of everything
2. **Start here** — Read `PROJECT_SUMMARY.md` for the full technical narrative
3. **Understand the data** — Open `reports/deep_data_analysis/deep_data_analysis_report.pdf`
4. **See the results** — Open `reports/model_comparison/model_comparison_report.pdf`
5. **Check quality** — Open `reports/similarity_innovation/similarity_innovation_report.pdf`
6. **Browse visuals** — Open `explainable_graphs/graph_catalog.csv` in Excel, filter by category
7. **Dive deeper** — Read the remaining 4 reports (feature interdependency, I/O coherence, class balance, business narrative)
8. **Get the data** — Pick your synthetic dataset from `synthetic_data/best_per_model/`

---

*Last updated: 2026-03-20*
