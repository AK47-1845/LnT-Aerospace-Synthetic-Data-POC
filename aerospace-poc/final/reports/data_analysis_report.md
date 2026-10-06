# Data Analysis Report — Aerospace Structural Design Dataset

---

## Table of Contents

1. [Executive Summary](#chapter-1--executive-summary)
2. [Dataset Overview](#chapter-2--dataset-overview)
3. [Univariate Analysis](#chapter-3--univariate-analysis)
4. [Bivariate & Multivariate Analysis](#chapter-4--bivariate--multivariate-analysis)
5. [Material Type Deep Dive](#chapter-5--material-type-deep-dive)
6. [Flight Environment Analysis](#chapter-6--flight-environment-analysis)
7. [Structural Geometry Analysis](#chapter-7--structural-geometry-analysis)
8. [Optimization & Algorithm Analysis](#chapter-8--optimization--algorithm-analysis)
9. [Target Variable Analysis](#chapter-9--target-variable-analysis)
10. [Feature Importance & Drivers](#chapter-10--feature-importance--drivers)
11. [Real vs Synthetic Comparison](#chapter-11--real-vs-synthetic-comparison)
12. [Conclusions & Recommendations](#chapter-12--conclusions--recommendations)

---

## Chapter 1 — Executive Summary

### What the Dataset Is

The **Aerospace Structural Design Dataset** is a multi-domain simulation dataset representing aerospace component design scenarios. It captures material properties (Young's modulus, Poisson's ratio, density, tensile strength), flight-environment parameters (altitude, temperature, pressure), structural geometry (wing span, fuselage length, thickness), and quantum-algorithm optimisation metadata (iterations, time). The real dataset contains **300 rows** and **22 columns**, with **14 numeric** and **4 categorical** features, and four ordinal classification targets.

### Top 3 Findings (computed from real data)

**Finding 1 — Dominant Correlation:** The strongest Pearson correlation in the dataset is between **Number of Iterations** and **E (GPa)** (r = 0.1501), indicating a strong linear relationship between these two engineered features.

**Finding 2 — Skewed Features:** 0 numeric features exhibit |skew| > 1, namely: none detected. These features may benefit from log- or Box-Cox transformation before modelling.

**Finding 3 — Material Type as Significant Predictor:** Chi-square tests confirm that Material Type has a statistically significant association (p < 0.05) with the following target variables: none. This makes Material Type a critical categorical feature for all downstream classifiers.

---

## Chapter 2 — Dataset Overview

- **Rows (real):** 300
- **Rows (synthetic — empirical_1000):** 1000
- **Columns:** 22
- **Memory footprint (real, deep):** 0.1635 MB
- **Missing values (real):** 0 total

### Schema Table

| Column | Dtype | Type | Range / Values |
| --- | --- | --- | --- |
| Material Type | object | Categorical | Aluminum, Carbon Fiber, Titanium |
| E (GPa) | float64 | Numeric | 50.10 – 199.83 |
| ν | float64 | Numeric | 0.30 – 0.35 |
| ρ (kg/m³) | float64 | Numeric | 1520.93 – 4495.76 |
| Tensile Strength (MPa) | float64 | Numeric | 261.25 – 1496.09 |
| Young’s Modulus | float64 | Numeric | 50.11 – 99.60 |
| Altitude (m) | float64 | Numeric | 5085.76 – 19962.63 |
| Temperature (°C) | float64 | Numeric | -59.97 – -40.03 |
| Pressure (Pa) | float64 | Numeric | 100171.59 – 199838.64 |
| Operational Life (years) | int64 | Numeric | 20.00 – 39.00 |
| Wing Span (m) | float64 | Numeric | 20.02 – 59.70 |
| Fuselage Length (m) | float64 | Numeric | 30.01 – 69.96 |
| Structural Thickness (mm) | float64 | Numeric | 5.00 – 14.94 |
| Structural Shape | object | Categorical | Cylindrical, Rectangular, Tapered |
| Load Distribution | object | Categorical | distributed, point load, uniform |
| Vibration Damping | object | Target (ordinal) | High, Low, Moderate |
| Computational Time | object | Target (ordinal) | Long, Medium, Short |
| Weight Efficiency | object | Target (ordinal) | Excellent, Good, Poor |
| Durability | object | Target (ordinal) | High, Low, Medium |
| Quantum Algorithm Type | object | Categorical | Chaotic Quantum Genetic, Shark Optimizer |
| Number of Iterations | int64 | Numeric | 523.00 – 1983.00 |
| Optimization Time (sec) | float64 | Numeric | 51.45 – 149.83 |

### Missing Values Audit

No missing values found in the real dataset. Data is complete.

### Class Counts for All 4 Targets

**Vibration Damping:**
| Class | Count |
| --- | --- |
| Moderate | 109 |
| Low | 104 |
| High | 87 |

**Computational Time:**
| Class | Count |
| --- | --- |
| Medium | 119 |
| Long | 92 |
| Short | 89 |

**Weight Efficiency:**
| Class | Count |
| --- | --- |
| Good | 109 |
| Poor | 97 |
| Excellent | 94 |

**Durability:**
| Class | Count |
| --- | --- |
| Medium | 108 |
| Low | 99 |
| High | 93 |

---

## Chapter 3 — Univariate Analysis

### Descriptive Statistics — All Numeric Features

| Feature | Mean | Std | Min | Max | Median | Skewness | Kurtosis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E (GPa) | 124.2119 | 43.3863 | 50.1032 | 199.8347 | 125.0864 | 0.0327 | -1.1681 |
| ν | 0.3254 | 0.0136 | 0.3002 | 0.3499 | 0.3257 | -0.0421 | -1.0494 |
| ρ (kg/m³) | 3018.0182 | 843.2637 | 1520.9327 | 4495.7591 | 3071.5450 | -0.0633 | -1.2130 |
| Tensile Strength (MPa) | 880.6487 | 363.2993 | 261.2469 | 1496.0901 | 883.2903 | -0.0016 | -1.1804 |
| Young’s Modulus | 75.4579 | 14.2789 | 50.1084 | 99.6047 | 75.9967 | -0.0877 | -1.2450 |
| Altitude (m) | 12452.7735 | 4545.2843 | 5085.7629 | 19962.6289 | 12586.8547 | -0.0094 | -1.3571 |
| Temperature (°C) | -49.6773 | 6.0357 | -59.9743 | -40.0275 | -49.0479 | -0.0933 | -1.2834 |
| Pressure (Pa) | 149463.6062 | 27865.5448 | 100171.5893 | 199838.6373 | 147942.9279 | 0.0411 | -1.1266 |
| Operational Life (years) | 29.8800 | 5.7940 | 20.0000 | 39.0000 | 31.0000 | -0.0847 | -1.2175 |
| Wing Span (m) | 39.5212 | 11.2237 | 20.0191 | 59.7005 | 39.3671 | 0.0197 | -1.2208 |
| Fuselage Length (m) | 50.9883 | 12.0302 | 30.0128 | 69.9633 | 51.6472 | -0.1595 | -1.2145 |
| Structural Thickness (mm) | 10.1656 | 2.8390 | 5.0027 | 14.9384 | 10.4369 | -0.1422 | -1.1324 |
| Number of Iterations | 1238.0133 | 410.8865 | 523.0000 | 1983.0000 | 1217.5000 | 0.1205 | -1.0988 |
| Optimization Time (sec) | 102.2619 | 29.5945 | 51.4522 | 149.8336 | 105.8235 | -0.1006 | -1.2917 |

### High-Skew Features (|skew| > 1)

No features with |skew| > 1 detected.

![Univariate Histogram Grid](plots/eda_univariate_histograms.png)

### Categorical Value Counts

**Material Type:**
| Value | Count |
| --- | --- |
| Carbon Fiber | 109 |
| Titanium | 99 |
| Aluminum | 92 |

**Structural Shape:**
| Value | Count |
| --- | --- |
| Rectangular | 109 |
| Cylindrical | 99 |
| Tapered | 92 |

**Load Distribution:**
| Value | Count |
| --- | --- |
| point load | 114 |
| distributed | 94 |
| uniform | 92 |

**Quantum Algorithm Type:**
| Value | Count |
| --- | --- |
| Shark Optimizer | 172 |
| Chaotic Quantum Genetic | 128 |

---

## Chapter 4 — Bivariate & Multivariate Analysis

![Pearson Correlation Heatmap](plots/eda_correlation_heatmap_pearson.png)

![Spearman Rank Correlation Heatmap](plots/eda_correlation_heatmap_spearman.png)

### Top 10 Most Correlated Pairs (Pearson)

| Feature 1 | Feature 2 | Correlation |
| --- | --- | --- |
| Number of Iterations | E (GPa) | 0.1501 |
| Fuselage Length (m) | ρ (kg/m³) | 0.1388 |
| ρ (kg/m³) | E (GPa) | 0.1350 |
| Fuselage Length (m) | Operational Life (years) | -0.1210 |
| Number of Iterations | Fuselage Length (m) | 0.1206 |
| Altitude (m) | Tensile Strength (MPa) | 0.1147 |
| Operational Life (years) | ν | 0.1047 |
| Operational Life (years) | E (GPa) | 0.0994 |
| Altitude (m) | ρ (kg/m³) | -0.0988 |
| Optimization Time (sec) | Pressure (Pa) | 0.0978 |

![Pairplot by Material Type](plots/eda_pairplot_material.png)

### Mean of Each Numeric Feature Grouped by Material Type

| Material Type | E (GPa) | ν | ρ (kg/m³) | Tensile Strength (MPa) | Young’s Modulus | Altitude (m) | Temperature (°C) | Pressure (Pa) | Operational Life (years) | Wing Span (m) | Fuselage Length (m) | Structural Thickness (mm) | Number of Iterations | Optimization Time (sec) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Aluminum | 127.1599 | 0.3265 | 3123.7935 | 840.2027 | 74.7652 | 12604.9294 | -50.1587 | 150393.8698 | 29.9891 | 40.2915 | 51.0418 | 10.3876 | 1263.4348 | 99.7647 |
| Carbon Fiber | 123.3788 | 0.3231 | 3068.3709 | 906.0985 | 77.4022 | 12711.5074 | -49.5426 | 144241.8029 | 29.3486 | 39.6468 | 52.2518 | 9.8351 | 1239.0826 | 106.1484 |
| Titanium | 122.3894 | 0.3271 | 2864.283 | 890.2145 | 73.9609 | 12026.5074 | -49.3781 | 154348.3771 | 30.3636 | 38.6671 | 49.5474 | 10.3233 | 1213.2121 | 100.3036 |

---

## Chapter 5 — Material Type Deep Dive

### Statistical Profile per Material (mean ± std)

| Material | E (GPa) | ρ (kg/m³) | Tensile Strength (MPa) |
| --- | --- | --- | --- |
| Aluminum | 127.1599 ± 45.0936 | 3123.7935 ± 830.9396 | 840.2027 ± 371.5325 |
| Carbon Fiber | 123.3788 ± 43.4673 | 3068.3709 ± 831.4265 | 906.0985 ± 362.6860 |
| Titanium | 122.3894 ± 41.9580 | 2864.2830 ± 854.0565 | 890.2145 ± 356.6571 |

![Violin Plot: E (GPa) by Material Type](plots/eda_violin_E_by_material.png)

![Boxplots by Material Type](plots/eda_boxplots_by_material.png)

### Chi-Square Tests: Material Type vs Each Target

| Target | chi2 | p-value | Significant |
| --- | --- | --- | --- |
| Vibration Damping | 3.7291 | 0.4439 | No |
| Computational Time | 2.0339 | 0.7295 | No |
| Weight Efficiency | 2.5045 | 0.6438 | No |
| Durability | 4.0277 | 0.4023 | No |

---

## Chapter 6 — Flight Environment Analysis

![Altitude vs Temperature & Pressure](plots/eda_altitude_temp_pressure.png)

- **R² of Temperature ~ Altitude (linear regression):** 0.0063
- **R² of Pressure ~ Altitude (linear regression):** 0.0031

### ISA Standard Atmosphere Comparison Note

In the International Standard Atmosphere (ISA), temperature decreases at ~6.5 °C/km in the troposphere (up to ~11 km) and remains roughly constant in the lower stratosphere (11–20 km). Pressure follows an exponential decay with altitude. The dataset linear R² for Temperature ~ Altitude of 0.0063 suggests a moderate-to-weak linear fit, consistent with stratospheric altitudes where the lapse rate is near-zero. The R² for Pressure ~ Altitude of 0.0031 reflects limited linear approximation of the exponential pressure profile over the altitude range sampled.

---

## Chapter 7 — Structural Geometry Analysis

![Wing Span vs Fuselage Length](plots/eda_wingspan_fuselage.png)

### Structural Thickness (mm) by Structural Shape

| Shape | Mean (mm) | Std (mm) | Min (mm) | Max (mm) |
| --- | --- | --- | --- | --- |
| Cylindrical | 10.0872 | 2.9072 | 5.1238 | 14.8915 |
| Rectangular | 10.4083 | 2.7497 | 5.1388 | 14.9384 |
| Tapered | 9.9624 | 2.8790 | 5.0027 | 14.6625 |

### Operational Life (years) by Material Type

| Material | Mean Life (yrs) | Std Life (yrs) |
| --- | --- | --- |
| Aluminum | 29.9891 | 5.9365 |
| Carbon Fiber | 29.3486 | 5.6312 |
| Titanium | 30.3636 | 5.8475 |

---

## Chapter 8 — Optimization & Algorithm Analysis

![Number of Iterations vs Optimization Time](plots/eda_optimization_scatter.png)

### Optimization Time by Algorithm Type

| Algorithm | Mean Time (sec) | Std Time (sec) |
| --- | --- | --- |
| Chaotic Quantum Genetic | 103.0827 | 28.4875 |
| Shark Optimizer | 101.6511 | 30.4603 |

### Correlation: Number of Iterations vs Computational Time (label-encoded)

Pearson correlation (iterations vs encoded Computational Time): **0.0205**
This weak-to-moderate correlation suggests that more iterations tend to map to longer computational time classes.

---

## Chapter 9 — Target Variable Analysis

![Target Distributions](plots/eda_target_distributions.png)

![Target Crosstab Heatmap: Durability x Weight Efficiency](plots/eda_target_crosstab_heatmap.png)

### Cross-Tabulations — All Target Pairs

**Vibration Damping x Computational Time:**

| Vibration Damping | Long | Medium | Short |
| --- | --- | --- | --- |
| High | 27 | 35 | 25 |
| Low | 30 | 46 | 28 |
| Moderate | 35 | 38 | 36 |

**Vibration Damping x Weight Efficiency:**

| Vibration Damping | Excellent | Good | Poor |
| --- | --- | --- | --- |
| High | 25 | 34 | 28 |
| Low | 33 | 36 | 35 |
| Moderate | 36 | 39 | 34 |

**Vibration Damping x Durability:**

| Vibration Damping | High | Low | Medium |
| --- | --- | --- | --- |
| High | 31 | 25 | 31 |
| Low | 30 | 39 | 35 |
| Moderate | 32 | 35 | 42 |

**Computational Time x Weight Efficiency:**

| Computational Time | Excellent | Good | Poor |
| --- | --- | --- | --- |
| Long | 25 | 37 | 30 |
| Medium | 44 | 39 | 36 |
| Short | 25 | 33 | 31 |

**Computational Time x Durability:**

| Computational Time | High | Low | Medium |
| --- | --- | --- | --- |
| Long | 31 | 24 | 37 |
| Medium | 30 | 42 | 47 |
| Short | 32 | 33 | 24 |

**Weight Efficiency x Durability:**

| Weight Efficiency | High | Low | Medium |
| --- | --- | --- | --- |
| Excellent | 25 | 29 | 40 |
| Good | 34 | 35 | 40 |
| Poor | 34 | 35 | 28 |

---

## Chapter 10 — Feature Importance & Drivers

![Random Forest Feature Importance](plots/eda_feature_importance_rf.png)

### Top 3 Features per Target (Random Forest Importance)

| Target | Rank | Feature | Importance |
| --- | --- | --- | --- |
| Vibration Damping | 1 | Tensile Strength (MPa) | 0.0812 |
| Vibration Damping | 2 | Altitude (m) | 0.0767 |
| Vibration Damping | 3 | ρ (kg/m³) | 0.0765 |
| Computational Time | 1 | Altitude (m) | 0.0829 |
| Computational Time | 2 | Fuselage Length (m) | 0.0808 |
| Computational Time | 3 | Wing Span (m) | 0.0786 |
| Weight Efficiency | 1 | Optimization Time (sec) | 0.0796 |
| Weight Efficiency | 2 | Wing Span (m) | 0.0791 |
| Weight Efficiency | 3 | Fuselage Length (m) | 0.0780 |
| Durability | 1 | Altitude (m) | 0.0848 |
| Durability | 2 | E (GPa) | 0.0813 |
| Durability | 3 | Tensile Strength (MPa) | 0.0813 |

### SHAP Note

SHAP (SHapley Additive exPlanations) values were not computed in this report due to runtime constraints. For production analysis, SHAP TreeExplainer applied to the Random Forest models above is recommended to obtain directional (signed) feature attribution and detect non-monotonic effects and interaction terms.

---

## Chapter 11 — Real vs Synthetic Comparison

![Real vs Synthetic Histograms](plots/eda_real_vs_syn_histograms.png)

![PCA Real vs Synthetic](plots/eda_pca_real_vs_syn.png)

### Kolmogorov-Smirnov Test Results (Real vs Empirical-1000)

| Feature | KS Statistic | p-value | Pass (p>0.05) |
| --- | --- | --- | --- |
| E (GPa) | 0.0523 | 0.5355 | Yes |
| ν | 0.0207 | 0.9999 | Yes |
| ρ (kg/m³) | 0.0327 | 0.9597 | Yes |
| Tensile Strength (MPa) | 0.0470 | 0.6706 | Yes |
| Young’s Modulus | 0.0303 | 0.9796 | Yes |
| Altitude (m) | 0.0177 | 1.0000 | Yes |
| Temperature (°C) | 0.0283 | 0.9901 | Yes |
| Pressure (Pa) | 0.0123 | 1.0000 | Yes |
| Operational Life (years) | 0.0400 | 0.8398 | Yes |
| Wing Span (m) | 0.0197 | 1.0000 | Yes |
| Fuselage Length (m) | 0.0263 | 0.9960 | Yes |
| Structural Thickness (mm) | 0.0337 | 0.9484 | Yes |
| Number of Iterations | 0.0273 | 0.9936 | Yes |
| Optimization Time (sec) | 0.0347 | 0.9355 | Yes |

**KS Test Pass Rate:** 100.0000% (14 / 14 features)

**Mean KL Divergence (real || synthetic):** 0.0177

A lower KL divergence indicates the synthetic marginal distributions are closer to the real ones. Values below 0.05 are generally considered excellent for synthetic data generation.

---

## Chapter 12 — Conclusions & Recommendations

### Key Statistical Properties the Synthetic Generator Must Preserve

1. **Marginal distributions** — Each numeric feature mean, standard deviation, skewness, and kurtosis must match the real dataset within acceptable tolerance (recommended: <=5% relative error for mean and std).
2. **Correlation structure** — The inter-feature Pearson and Spearman correlation matrices should be preserved. Material Type drives significant variation in E, rho, and Tensile Strength; any generator must condition on categorical features.
3. **Class balance of targets** — The ordinal target distributions (particularly Vibration Damping and Durability) must be reproduced to avoid classifier bias.
4. **Conditional relationships** — Material Type x target associations confirmed by chi-square tests must be reflected in synthetic samples.
5. **Flight-environment physics** — The negative correlation of Temperature with Altitude and the exponential-like decay of Pressure with Altitude must be preserved.

### Red Lines: Physical Constraints

| Constraint | Requirement |
|---|---|
| E (GPa) > 0 | Young's modulus is always strictly positive |
| nu in (0, 0.5) | Poisson's ratio physically bounded |
| rho (kg/m3) > 0 | Density is strictly positive |
| Tensile Strength (MPa) > 0 | Strength is strictly positive |
| Altitude (m) > 0 | Operational altitude above ground |
| Temperature < 0 C | High-altitude temperatures are sub-zero |
| Pressure (Pa) > 0 | Pressure is always positive |
| Operational Life > 0 | Service life is positive |
| Number of Iterations >= 1 | At least one optimisation step |
| Optimization Time > 0 | Wall-clock time is positive |

### Recommended Approach

1. **Use a copula-based or CTGAN model** conditioned on Material Type and Quantum Algorithm Type to capture inter-feature correlations and categorical dependencies simultaneously.
2. **Apply post-generation clipping** to enforce all physical constraints listed above.
3. **Evaluate with KS test + KL divergence** per feature after each generation run; target KS pass rate >= 80% and mean KL divergence < 0.05.
4. **Stratify synthetic samples** to match real class distributions for all 4 targets.
5. **Validate downstream classifier performance** by training on synthetic data and testing on real data (TSTR protocol) — accuracy degradation < 5% versus real-data-trained baseline is the acceptance criterion.

---

*Report generated automatically by `build_data_analysis_report.py` — Aerospace Structural Design Synthetic Data Project.*
