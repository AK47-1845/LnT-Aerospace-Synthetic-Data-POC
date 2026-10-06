# Aerospace Synthetic Data Generation — Project Summary

## 1. Project Overview

This project addresses the synthetic data generation challenge for the **Aerospace Structural Design Dataset** — a Kaggle dataset of 300 simulated aircraft structural configurations. Each row represents one design attempt combining material properties, flight environment parameters, geometry specifications, and quantum optimization settings to predict four categorical performance targets.

**Objective:** Generate high-fidelity synthetic datasets that preserve:
- Statistical distributions and feature correlations of the original data
- Physics-consistent relationships between inputs and outputs
- Balanced class representation across all four target variables
- Realistic edge cases covering rare but plausible design configurations

**Scale of Work:**
- 9 generative models evaluated
- 90+ experimental runs across 3 random seeds and 4 dataset sizes
- 7 comprehensive PDF reports (LaTeX-compiled)
- 294 catalogued visualizations across 11 analytical categories
- 736 total deliverable files

---

## 2. Dataset Description

### Input Features (18 columns)

| # | Feature | Type | Range/Levels | Domain Role |
|---|---------|------|-------------|-------------|
| 1 | Material Type | Categorical | Aluminum, Carbon Fiber, Titanium | Base material selection |
| 2 | E (GPa) | Numeric | ~70–400 | Elastic modulus (stiffness) |
| 3 | ν (Poisson's Ratio) | Numeric | ~0.26–0.33 | Lateral strain ratio |
| 4 | ρ (kg/m³) | Numeric | ~1600–4500 | Material density |
| 5 | Tensile Strength (MPa) | Numeric | ~200–1800 | Maximum stress before fracture |
| 6 | Young's Modulus | Numeric | ~70–400 | Duplicate of E (kept for schema compliance) |
| 7 | Altitude (m) | Numeric | 5,000–20,000 | Flight operating altitude |
| 8 | Temperature (°C) | Numeric | –60 to –40 | Ambient temperature at altitude |
| 9 | Pressure (Pa) | Numeric | 100,000–200,000 | Atmospheric pressure |
| 10 | Operational Life (years) | Numeric | ~5–30 | Expected service life |
| 11 | Wing Span (m) | Numeric | ~10–80 | Wing tip-to-tip distance |
| 12 | Fuselage Length (m) | Numeric | ~20–70 | Aircraft body length |
| 13 | Structural Thickness (mm) | Numeric | ~1–10 | Wall thickness |
| 14 | Structural Shape | Categorical | I-Beam, Cylindrical, Rectangular | Cross-section geometry |
| 15 | Load Distribution | Categorical | Uniform, Point, Distributed | Loading pattern type |
| 16 | Quantum Algorithm Type | Categorical | QAOA, VQE, Grover, Quantum Annealing, SHARK | Optimization method |
| 17 | Number of Iterations | Numeric | ~50–500 | Optimizer convergence steps |
| 18 | Optimization Time (sec) | Numeric | ~10–300 | Total optimization runtime |

### Target Variables (4 columns)

| Target | Classes | Description |
|--------|---------|-------------|
| Vibration Damping | Low, Moderate, High | Structural vibration absorption capability |
| Computational Time | Short, Medium, Long | Optimization computational expense |
| Weight Efficiency | Poor, Good, Excellent | Mass-to-performance ratio |
| Durability | Low, Medium, High | Structural longevity under stress |

---

## 3. Synthetic Data Generation

### Models Evaluated (9 Models, 3 Tiers)

A rigorous model selection process evaluated 9 generative models across 92 configurations to ensure the recommended model is truly optimal — not just the first that worked.

**Tier 1 — Production Ready** (recommended for use)

| # | Model | Type | Description |
|---|-------|------|-------------|
| 1 | **KDE** | Non-parametric | Kernel Density Estimation with bandwidth tuning |
| 2 | **GMM** | Parametric | Gaussian Mixture Model with EM optimization |
| 3 | **Copula** | Statistical | Gaussian copula preserving marginal + dependency structure |

**Tier 2 — Research Interest** (shows potential but not production-grade for this dataset)

| # | Model | Type | Description |
|---|-------|------|-------------|
| 4 | **TabuDiff** | Deep Learning | Tabular diffusion model (denoising-based generation) |
| 5 | **TabuDiffPremium** | Deep Learning | Enhanced TabuDiff with extended training |

**Tier 3 — Evaluated, Not Recommended** (included for completeness of benchmarking)

| # | Model | Type | Description |
|---|-------|------|-------------|
| 6 | **TVAE** | Deep Learning | Tabular Variational Autoencoder — class collapse at this data scale |
| 7 | **TVAEPremium** | Deep Learning | Enhanced TVAE — same class collapse issue |
| 8 | **CTGANPremium** | Deep Learning | Conditional Tabular GAN — memorizes training data |
| 9 | **MaskedPredictor** | ML-based | Iterative masked prediction — high variance, architecture-limited |

> **Why 9 models?** Statistical models (KDE, GMM, Copula) excel at n=300 because they don't need large training sets. Deep learning models (TVAE, CTGAN, TabuDiff) typically require thousands of rows to generalize. By testing both families, we confirm that statistical methods are the right choice for this dataset size — not an assumption, but a data-driven conclusion.

### Experimental Design

- **Random Seeds:** 11, 42, 123 (reproducibility across 3 seeds)
- **Dataset Sizes:** 300, 600, 1,000, 5,000 rows
- **Total Experiments:** 92 runs in `synthetic_data/experimentations/`
- **Best Per Model:** 9 curated datasets in `synthetic_data/best_per_model/`
- **Top 10 Overall:** All KDE variants, stored in `synthetic_data/top_10/`

---

## 4. Evaluation Framework

Every synthetic dataset was scored on a **6-axis composite metric**:

| Axis | Metric | What It Measures |
|------|--------|-----------------|
| Physics Consistency | Domain rule checks | Do generated rows obey physical laws (ISA model, material bounds)? |
| Statistical Similarity | Distribution overlap | Do per-feature distributions match the real data? |
| KS p-value | Kolmogorov-Smirnov test | Are synthetic and real samples drawn from the same distribution? |
| KL Divergence | Kullback-Leibler | Information-theoretic distance between distributions |
| ML Utility (TSTR) | Train-Synthetic, Test-Real | Can a model trained on synthetic data predict real labels? |
| Privacy / Detection AUC | Discriminator classifier | Can a binary classifier distinguish real from synthetic? |

**Composite Score** = weighted combination of all 6 axes (higher = better, max 1.0)

---

## 5. Top Results

### Overall Leaderboard (Top 10)

| Rank | Model | Seed | Size | Composite Score | TSTR | KS p-value | KL Div | Repair Triggers |
|------|-------|------|------|----------------|------|-----------|--------|-----------------|
| 1 | KDE | 123 | 5000 | **0.9965** | 1.000 | 0.9975 | 0.0040 | 0 |
| 2 | KDE | 11 | 5000 | 0.9963 | 1.000 | 0.9990 | 0.0043 | 0 |
| 3 | KDE | 42 | 5000 | 0.9960 | 1.000 | 0.9988 | 0.0045 | 0 |
| 4 | KDE | 123 | 1000 | 0.9865 | 0.983 | 0.9417 | 0.0111 | 0 |
| 5 | KDE | 42 | 1000 | 0.9819 | 0.963 | 0.9485 | 0.0109 | 0 |
| 6 | KDE | 11 | 1000 | 0.9806 | 0.963 | 0.8971 | 0.0125 | 0 |
| 7 | KDE | 123 | 600 | 0.9712 | 0.933 | 0.9588 | 0.0146 | 0 |
| 8 | KDE | 42 | 600 | 0.9629 | 0.907 | 0.8912 | 0.0191 | 0 |
| 9 | KDE | 11 | 600 | 0.9624 | 0.903 | 0.8603 | 0.0178 | 0 |
| 10 | KDE | 42 | 300 | 0.9195 | 0.760 | 0.8790 | 0.0328 | 0 |

**Key Insight:** KDE sweeps all top-10 positions. Larger sizes (n=5000) achieve near-perfect scores. Zero repair triggers across all top runs.

### Best Per Model — Discriminator & MMD

| Model | Discriminator AUC | Indistinguishability | MMD (5000) | Verdict |
|-------|-------------------|---------------------|------------|---------|
| **GMM** | 0.451 | 90.2% | 0.0007 | Excellent |
| **KDE** | 0.478 | 95.5% | 0.0003 | Excellent |
| **Copula** | 0.518 | 96.5% | 0.0013 | Excellent |
| TabuDiff | 0.722 | 55.7% | 0.0207 | Moderate |
| TabuDiffPremium | 0.895 | 21.1% | — | Poor |
| MaskedPredictor | 0.976 | 4.8% | 0.0276 | Poor |
| CTGANPremium | 0.995 | 1.0% | — | Overfitting |
| TVAE | 0.999 | 0.1% | 0.402 | Overfitting |
| TVAEPremium | 1.000 | 0.0% | — | Overfitting |

**Interpretation:** AUC near 0.5 = synthetic is indistinguishable from real (ideal). AUC near 1.0 = trivially separable (poor).

---

## 6. Feature Engineering (Bonus — Beyond Client Scope)

> *This section goes beyond the client brief to demonstrate additional analytical depth. The client did not request feature engineering, but it provides useful context for understanding the dataset's structure.*

### 12 Domain-Specific Engineered Features

| Feature | Formula | Aerospace Significance |
|---------|---------|----------------------|
| stiffness_to_weight | E / ρ | Specific stiffness — primary material selection criterion |
| strength_to_weight | Tensile Strength / ρ | Specific strength — weight-critical design metric |
| aspect_ratio | Wing Span / Fuselage Length | Aerodynamic efficiency indicator |
| thickness_ratio | Structural Thickness / Wing Span | Structural slenderness — buckling susceptibility |
| thermal_stress_proxy | \|Temperature\| × Pressure / 1e6 | Combined thermal-pressure loading estimate |
| optimization_efficiency | Iterations / Optimization Time | Quantum optimizer convergence rate |
| altitude_pressure_deviation | Pressure − ISA(Altitude) | Deviation from International Standard Atmosphere |
| material_density_normalized | ρ / max(ρ) per material | Material utilization ratio within class |
| log_E | log1p(E) | Normalizes right-skewed modulus distribution |
| log_tensile | log1p(Tensile Strength) | Normalizes right-skewed tensile distribution |
| E_times_thickness | E × Structural Thickness | Structural stiffness interaction term |
| rho_times_wingspan | ρ × Wing Span | Total structural mass proxy |

### Multicollinearity Analysis (VIF)

| Feature | VIF | Severity |
|---------|-----|----------|
| ν (Poisson's Ratio) | 182.6 | CRITICAL |
| Temperature (°C) | 66.8 | HIGH |
| Pressure (Pa) | 31.0 | HIGH |
| Operational Life (years) | 28.9 | HIGH |
| Young's Modulus | 27.9 | HIGH |

### Feature Importance (Random Forest, Top 10)

| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | aspect_ratio | 0.0446 |
| 2 | Altitude (m) | 0.0435 |
| 3 | optimization_efficiency | 0.0409 |
| 4 | Optimization Time (sec) | 0.0408 |
| 5 | Fuselage Length (m) | 0.0401 |
| 6 | Temperature (°C) | 0.0394 |
| 7 | Young's Modulus | 0.0394 |
| 8 | thickness_ratio | 0.0387 |
| 9 | Number of Iterations | 0.0385 |
| 10 | Wing Span (m) | 0.0378 |

### PCA Summary
- **5 components** explain **58.0%** of total variance
- Used for dimensionality reduction visualizations and augmented datasets

---

## 7. Class Balancing

Four strategies were evaluated on both real and KDE synthetic data:

### Real Dataset Results

| Strategy | Balance Score | TSTR F1 | Composite | Output Rows |
|----------|--------------|---------|-----------|-------------|
| **SMOTE-NC** | 0.9663 | 0.9903 | **0.9783** | 999 |
| ADASYN | 0.9663 | 0.9903 | 0.9783 | 999 |
| Undersampling | 0.9646 | 0.7858 | 0.8752 | 207 |
| Genuity Conditional | 0.9311 | 0.6984 | 0.8147 | 1,000 |

### KDE Synthetic Results

| Strategy | Balance Score | TSTR F1 | Composite | Output Rows |
|----------|--------------|---------|-----------|-------------|
| **Undersampling** | 0.9769 | 1.0000 | **0.9884** | 3,369 |
| SMOTE-NC | 0.9661 | 0.9533 | 0.9597 | 999 |
| ADASYN | 0.9661 | 0.9533 | 0.9597 | 999 |
| Genuity Conditional | 0.8667 | 0.9719 | 0.9193 | 1,000 |

**Recommendation:** SMOTE-NC for real data (best F1 preservation), undersampling for KDE synthetic (already large enough to afford trimming).

---

## 8. Edge Case Analysis

### 30 Scenarios Across 6 Categories

| Category | Scenarios | Examples |
|----------|-----------|---------|
| Material | 5 | Aluminum-only, Carbon Fiber-only, Titanium-only, extreme density |
| Flight Envelope | 4 | Extreme altitude, moderate temperature, pressure extremes |
| Target/Performance | 4 | Low/high durability clusters, poor weight efficiency |
| Geometry | 4 | Extreme wingspan (small/large), extreme thickness |
| Optimization | 4 | SHARK-only, long optimization time |
| Lifecycle | 2 | Long/short operational life |

### Realism Scores

- **Highest:** low_durability_cluster (98.1%), material_carbonfiber_only (98.1%)
- **Lowest:** wingspan_extreme_small (69.3%), long_optimization (81.3%)
- **Mean across all 30 scenarios:** ~91%

### Anomaly Detection
- **Isolation Forest** + **Local Outlier Factor** applied to every edge case
- Realism score = 1 − (anomaly percentage)
- Nearest-neighbor distance to reference rows computed for spatial validation

---

## 9. Anomaly & Outlier Detection

Per-model anomaly rates (Isolation Forest novelty detection against real data):

| Model | IF Anomaly % | LOF Anomaly % | Self-IF % | NN Distance (mean) |
|-------|-------------|---------------|-----------|-------------------|
| **KDE** | 7–13% | 8–11% | — | Low |
| **GMM** | 30–35% | 11–13% | — | Moderate |
| **Copula** | 37–39% | 15–18% | — | Moderate |
| **TabuDiff** | 17–26% | 4–6% | — | Low-Moderate |
| **TabuDiffPremium** | 42–60% | ~21% | — | High |
| **MaskedPredictor** | 0% | 0% | ~10% | Low |
| **CTGANPremium** | 0% | 0% | 0% | Very Low |
| **TVAE / TVAEPremium** | 0% | 0% | 0% | Very Low |

**Interpretation:**
- KDE produces the most realistic novel samples (low anomaly %, non-zero = not memorizing)
- TVAE/CTGANPremium show 0% anomalies — a sign of overfitting/memorization, confirmed by discriminator AUC ≈ 1.0
- TabuDiffPremium generates too many outliers — data is novel but unrealistic

---

## 10. Discriminator Similarity

A binary Random Forest classifier was trained to distinguish real from synthetic rows.

- **AUC ≈ 0.5** = classifier cannot tell them apart (ideal)
- **AUC ≈ 1.0** = trivially separable (poor)

**Best performers:** GMM (0.451), KDE (0.478), Copula (0.518) — all near random chance.

### Maximum Mean Discrepancy (MMD)

MMD measures distributional distance in kernel space (lower = better):

| Model | n=300 | n=600 | n=1000 | n=5000 |
|-------|-------|-------|--------|--------|
| KDE | 0.0017 | 0.0009 | 0.0005 | **0.0003** |
| GMM | 0.0026 | 0.0012 | 0.0008 | 0.0007 |
| Copula | 0.0032 | 0.0019 | 0.0015 | 0.0013 |
| TabuDiff | 0.0241 | 0.0220 | 0.0210 | 0.0207 |
| MaskedPredictor | 0.0235 | 0.0254 | 0.0263 | 0.0276 |

**KDE and GMM show excellent scaling** — MMD drops dramatically with more data.

---

## 11. Dimensionality Reduction

- **PCA 2D projections** for all 9 models overlaid on real data
- **t-SNE visualizations** showing cluster overlap
- Per-model comparison grids available in `discriminator_similarity/dimensionality_reduction/visuals/`
- Organized copies in `explainable_graphs/10_dimensionality_reduction/` (36 plots)

**Key Visual Finding:** KDE, GMM, and Copula synthetic points overlap almost perfectly with real data clusters in both PCA and t-SNE space. Deep learning models (TVAE, CTGAN) form separate clusters.

---

## 12. Reports Generated

| # | Report | Pages | Key Content |
|---|--------|-------|-------------|
| 1 | Deep Data Analysis | ~30 | Full EDA: univariate, bivariate, correlation matrices, ISA validation, feature importance |
| 2 | Business Narrative | ~10 | Material selection decision matrix, risk flags, operational insights |
| 3 | Model Comparison | ~15 | 9-model benchmarking: composite scores, radar charts, scale analysis |
| 4 | Feature Interdependency | ~12 | Frobenius norm comparison, spectral similarity, correlation preservation |
| 5 | Input-Output Coherence | ~12 | Causal fidelity, SHAP alignment, counterfactual analysis, domain rule checks |
| 6 | Class Balance & Edge Cases | ~12 | Chi-square tests, 4-way joint distribution, balancing strategy evaluation, edge case realism |
| 7 | Similarity & Innovation | ~15 | TSTR/TRTS/TRTR, MMD, discriminator AUC, bootstrap CI, sensitivity analysis |

All reports compiled as PDF via tectonic (LaTeX engine) with embedded figures and supporting data tables.

---

## 13. Visualization Catalog

**294 unique graphs** organized into 11 categories in `explainable_graphs/`:

| Category | Count | Contents |
|----------|-------|---------|
| 01_univariate | 42 | Histograms, KDE density plots, boxplots per feature |
| 02_bivariate | 22 | Scatter grids, correlation heatmaps, radar charts, ISA validation |
| 03_synthetic_vs_real | 79 | Per-model correlation diffs, overlaid histograms, distribution comparisons |
| 04_target_analysis | 31 | Target distributions, class frequencies, grouped statistics |
| 05_validation_metrics | 21 | KS/KL/Wasserstein heatmaps, discriminator ROC, MMD, anomaly scores |
| 06_feature_importance | 10 | SHAP bar charts, RF importance rankings, importance heatmaps |
| 07_model_performance | 31 | Leaderboard, radar charts, scale analysis, TSTR by size |
| 08_edge_cases | 4 | LOF distribution, realism scores, edge case overlays |
| 09_feature_engineering | 4 | VIF analysis, PCA scree, accuracy with/without FE, skewness |
| 10_dimensionality_reduction | 36 | PCA/t-SNE overlays for all models |
| 11_report_figures | 36 | All figures embedded in the 7 PDF reports |

A master index is available at `explainable_graphs/graph_catalog.csv` with filename, category, description, and audience metadata.

---

## 14. Key Findings & Recommendations

### What Works Best
1. **KDE is the clear winner** — highest composite score (0.9965), lowest MMD, near-perfect TSTR, zero repair triggers
2. **n=5000 is the optimal scale** — all metrics improve monotonically with size for KDE/GMM/Copula
3. **Statistical models outperform deep learning** for this dataset size (300 rows) — KDE, GMM, and Copula all produce indistinguishable synthetic data

### What Doesn't Work
1. **TVAE/CTGANPremium memorize the training data** — 0% anomaly rate + AUC ≈ 1.0 confirms they simply reproduce rather than generalize
2. **TabuDiffPremium generates too many outliers** — 42-60% anomaly rate means most samples are unrealistic
3. **Feature engineering provides minimal accuracy gain** (mean Δ = –0.0025) — the original 22 features already capture the signal well

### Recommendations for Production Use
- Use **KDE with seed=123, n=5000** as the primary synthetic dataset
- Apply **SMOTE-NC** for class balancing if balanced targets are required
- Include **edge cases** from the top-realism scenarios (>95%) to cover rare design configurations
- Monitor **altitude_pressure_deviation** as a physics sanity check on any new synthetic generation
