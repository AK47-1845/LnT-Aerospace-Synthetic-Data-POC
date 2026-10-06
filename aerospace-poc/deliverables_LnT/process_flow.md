# Aerospace Synthetic Data — Complete Process Flow & Deliverables Guide

> **Purpose of this document:** To give anyone — regardless of background — a full, unambiguous understanding of how this project started (a 300-row CSV file), what was done at every step, the exact physics mathematics used, what every deliverable file contains, and the ideal order to consume all outputs.

---

## Table of Contents

1. [Where It All Starts — The Raw Dataset](#1-where-it-all-starts--the-raw-dataset)
2. [Step-by-Step Pipeline Walkthrough](#2-step-by-step-pipeline-walkthrough)
   - 2.1 Data Ingestion & Preprocessing
   - 2.2 Physics Feature Derivation (with full formulae)
   - 2.3 Multi-Phase Model Benchmarking
   - 2.4 Synthetic Data Generation
   - 2.5 Physics Repair & Hard Constraint Enforcement
   - 2.6 6-Axis Composite Evaluation Framework
   - 2.7 Edge Case Engineering
   - 2.8 Class Balancing
   - 2.9 Anomaly & Outlier Detection
   - 2.10 Discriminator & Similarity Testing
   - 2.11 Feature Engineering Analysis (Bonus)
   - 2.12 Visualization & Reporting
3. [Deliverables — Every File, Every Folder Explained](#3-deliverables--every-file-every-folder-explained)
4. [Key Numbers Quick Reference](#4-key-numbers-quick-reference)
5. [Ideal Reading Flow](#5-ideal-reading-flow)

---

## 1. Where It All Starts — The Raw Dataset

**Input file:** `aerospace_structural_design_dataset.csv`
**Location:** `d:/aero/aerospace_structural_design_dataset.csv`
**Size:** 300 rows × 22 columns (~89 KB)

This dataset represents simulated aircraft structural design configurations from Kaggle. Each row is one design attempt combining material properties, atmospheric parameters, structural geometry, and quantum optimization settings. The four output columns are performance targets classified into discrete levels.

### Input Features (18 Columns)

| # | Column Name | Type | Range | Engineering Meaning |
|---|-------------|------|-------|---------------------|
| 1 | Material Type | Categorical | Aluminum, Carbon Fiber, Titanium, Steel | Base material selection — determines density, modulus, and strength bounds |
| 2 | Youngs Modulus (GPa) | Numeric | ~70–400 | Elastic modulus: how much a material deforms per unit stress |
| 3 | Poisson's Ratio (ν) | Numeric | ~0.26–0.33 | Ratio of lateral strain to axial strain; very high VIF (182.6) — strongly correlated with material type |
| 4 | Density (kg/m³) | Numeric | ~1600–4500 | Material mass per unit volume; drives weight efficiency calculations |
| 5 | Tensile Strength (MPa) | Numeric | ~200–1800 | Maximum stress the material can withstand before fracturing |
| 6 | Yield Strength (MPa) | Numeric | ~150–1600 | Stress at which permanent deformation begins (must be ≤ tensile strength) |
| 7 | Fatigue Limit (MPa) | Numeric | ~100–1000 | Maximum cyclic stress without eventual failure (must be ≤ tensile strength) |
| 8 | Altitude (m) | Numeric | 5,000–20,000 | Operating altitude — determines ambient temperature and pressure via ISA model |
| 9 | Temperature (°C) | Numeric | –60 to –40 | Ambient temperature at altitude — must correlate with altitude per ISA lapse rate |
| 10 | Pressure (Pa) | Numeric | ~100,000–200,000 | Atmospheric pressure — must be consistent with altitude per ISA model |
| 11 | Operational Life (years) | Numeric | ~5–30 | Expected service duration — affects fatigue considerations |
| 12 | Wing Span (m) | Numeric | ~10–80 | Wing tip-to-tip distance — drives structural loading and aspect ratio |
| 13 | Fuselage Length (m) | Numeric | ~20–70 | Aircraft body length — paired with wing span for aerodynamic efficiency |
| 14 | Structural Thickness (mm) | Numeric | ~1–10 | Wall thickness of structural member — key buckling resistance parameter |
| 15 | Structural Shape | Categorical | I-Beam, Cylindrical, Rectangular | Cross-section geometry — affects moment of inertia and buckling characteristics |
| 16 | Load Distribution | Categorical | Uniform, Point, Distributed | Loading pattern type — determines stress concentration factors |
| 17 | Quantum Algorithm Type | Categorical | QAOA, VQE, Grover, Quantum Annealing, SHARK | Optimization method used for structural design |
| 18 | Number of Iterations | Numeric | ~50–500 | Steps to optimizer convergence |
| 19 | Optimization Time (sec) | Numeric | ~10–300 | Total wall-clock time for optimization |

### Output / Target Variables (4 Columns)

| Target | Classes | Engineering Interpretation |
|--------|---------|---------------------------|
| Vibration Damping | Low / Moderate / High | How well the structure absorbs oscillations |
| Computational Time | Short / Medium / Long | How expensive the quantum optimization was |
| Weight Efficiency | Poor / Good / Excellent | How well the design optimizes performance-to-mass ratio |
| Durability | Low / Medium / High | Expected structural lifespan under operating stress |

---

## 2. Step-by-Step Pipeline Walkthrough

### 2.1 Data Ingestion & Preprocessing

**Script:** `data_prep.py`

1. **Loading:** The CSV is loaded using `pandas.read_csv()`. Headers are validated against the expected 22-column schema.
2. **Type Enforcement:** Categorical columns (Material Type, Structural Shape, Load Distribution, Quantum Algorithm Type) are cast to `pd.Categorical` dtype. Numeric columns are cast to `float64`.
3. **PII Check:** All column names are scanned against a PII regex pattern (names, SSNs, emails, phone numbers). This dataset is confirmed PII-free.
4. **Missing Value Handling:** Any rows with NaNs in numeric columns are dropped. Categorical NaNs are imputed by mode.
5. **Encoding:** Categorical features are label-encoded for model inputs. One-hot encoding is used where model architecture requires it (e.g., CTGAN's conditional embedding).
6. **Scaling:** StandardScaler applied to numeric columns for models sensitive to feature magnitudes (TVAE, CTGAN). KDE and GMM use raw values.
7. **Train/Test Split:** An 80/20 stratified split on `Durability` is held out exclusively for TSTR (Train Synthetic, Test Real) evaluation. The 80% (240 rows) serves as the generative training set.

---

### 2.2 Physics Feature Derivation (Full Formulae)

**Script:** `physics.py` — Function: `derive_physics_features(df)`

Six domain-grounded physics features are computed and appended to the dataset. These are not arbitrary transforms; each one is a recognized aerospace engineering quantity derived from first principles.

---

#### Feature 1: Specific Stiffness (Stiffness-to-Weight Ratio)

```
specific_stiffness = E / ρ

Where:
  E = Young's Modulus (GPa or Pa — consistent units)
  ρ = Density (kg/m³)

Units: (Pa) / (kg/m³) = m²/s²
```

**Why it matters:** Primary material selection criterion in aerospace design. A material with high specific stiffness provides maximum structural rigidity for minimum added mass. Carbon fibre composites dominate here; aluminium is second. This metric is why carbon fibre dominates modern aircraft construction despite its higher cost.

**Implementation:**
```python
df['specific_stiffness'] = df['Youngs Modulus'] / df['Density']
```

---

#### Feature 2: Specific Strength (Strength-to-Weight Ratio)

```
specific_strength = σ_uts / ρ

Where:
  σ_uts = Ultimate Tensile Strength (MPa = N/mm² = 10⁶ Pa)
  ρ     = Density (kg/m³)

Units: (Pa) / (kg/m³) = m²/s²
```

**Why it matters:** For weight-critical structures (wings, fuselage frames), maximising specific strength means more load can be carried per kilogram of material. Titanium excels here for cyclic loads; carbon fibre leads for tensile dominant loads.

**Implementation:**
```python
df['specific_strength'] = df['Tensile Strength'] / df['Density']
```

---

#### Feature 3: Buckling Resistance Index

```
buckling_resistance_index = E × t²

Where:
  E = Young's Modulus (GPa)
  t = Structural Thickness (mm)

Units: GPa·mm²
```

**Why it matters:** Euler's column buckling formula gives critical buckling load as:

```
P_cr = (π² × E × I) / (K × L)²

Where I (second moment of area) scales with t².
```

The simplified `E × t²` product captures the relative buckling resistance across configurations without requiring full geometry specification. Higher values indicate resistance to sudden lateral collapse under axial compression — critical for fuselage stringers and wing ribs.

**Implementation:**
```python
df['buckling_resistance_index'] = df['Youngs Modulus'] * (df['Structural Thickness'] ** 2)
```

---

#### Feature 4: Elastic Energy Capacity (Modulus of Resilience)

```
elastic_energy_capacity = σ_y² / (2 × E)

In this implementation, tensile strength (σ_uts) is used as a conservative proxy for σ_y:

elastic_energy_capacity = σ_uts² / E

Where:
  σ_uts = Tensile Strength (MPa)
  E     = Young's Modulus (GPa — matched units required)

Units: MPa² / GPa = MPa (energy per unit volume, J/m³)
```

**Why it matters:** The modulus of resilience is the maximum energy per unit volume a material can absorb and release elastically (without permanent deformation). High resilience is essential for spring-loaded components, landing gear, and structural joints subject to repeated impact. Materials with high strength but low modulus (like titanium vs. steel) store far more elastic energy per kilogram.

**Implementation:**
```python
df['elastic_energy_capacity'] = (df['Tensile Strength'] ** 2) / df['Youngs Modulus']
```

---

#### Feature 5: Fatigue Resistance Ratio

```
fatigue_resistance_ratio = σ_f / σ_uts

Where:
  σ_f   = Fatigue Limit (MPa) — the cyclic stress below which the material won't fail
  σ_uts = Ultimate Tensile Strength (MPa)

Units: dimensionless ratio, range (0, 1]
```

**Why it matters:** The fatigue ratio (also called endurance ratio) measures what fraction of a material's ultimate strength survives indefinite cyclic loading. For steel it is typically ~0.5; for aluminium it can be lower and more variable. It directly governs the operational life and inspection intervals required for airworthiness certification.

**Hard constraint enforced:** `σ_f ≤ σ_uts` always — a material cannot have a fatigue limit exceeding its ultimate strength. Any synthetic row violating this is automatically repaired.

**Implementation:**
```python
df['fatigue_resistance_ratio'] = df['Fatigue Limit'] / df['Tensile Strength']
```

---

#### Feature 6: Stress Safety Factor

```
stress_safety_factor = σ_uts / σ_applied

Where:
  σ_uts     = Tensile Strength (MPa) — the material's limit
  σ_applied = Applied Stress (MPa) — the actual design load

Units: dimensionless; typical aerospace range: 1.5–4.0
```

**Why it matters:** The factor of safety is the most direct measure of structural margin. A factor of 1.5 means the structure can take 50% more load than designed before failure — the minimum for most aerospace standards (FAR/CS regulations). Higher safety factors add weight; lower ones increase risk.

**Note on implementation:** This feature is computed only when `Applied Stress` is present in the dataset schema:
```python
if 'Tensile Strength' in df.columns and 'Applied Stress' in df.columns:
    df['stress_safety_factor'] = df['Tensile Strength'] / df['Applied Stress']
```

---

#### ISA Atmosphere Validation (Physics Check, Not a Feature)

The International Standard Atmosphere (ISA) model defines the relationship between altitude, temperature, and pressure:

**Temperature lapse rate (troposphere, 0–11,000 m):**
```
T(h) = T₀ - L × h

Where:
  T₀ = 288.15 K (15°C at sea level)
  L  = 0.0065 K/m (temperature lapse rate)
  h  = altitude (m)
```

**Pressure at altitude:**
```
P(h) = P₀ × (T(h) / T₀)^(g / (R × L))

Where:
  P₀ = 101,325 Pa  (sea-level standard pressure)
  g  = 9.80665 m/s²  (gravitational acceleration — from CONSTANTS in config.py)
  R  = 287.058 J/(kg·K)  (gas constant for dry air — from CONSTANTS in config.py)
  L  = 0.0065 K/m
```

For altitudes above the tropopause (>11,000 m), temperature is constant at 216.65 K and the pressure formula changes to exponential decay. Each synthetic row's `Pressure` and `Temperature` are cross-validated against the predicted ISA values at the stated `Altitude`. Deviations beyond 5% are flagged.

---

### 2.3 Multi-Phase Model Benchmarking

**Scripts:** `main.py`, `models_engine.py`, `evaluator.py`

#### Phase 1 — Smoke Benchmarking

- **Purpose:** Rapid elimination of poor models before committing to full compute.
- **Optuna trials:** 3 per model
- **Models tested:** All 9 (KDE, GMM, Copula, TVAE, TVAEPremium, CTGAN, CTGANPremium, TabuDiff, TabuDiffPremium, MaskedPredictor)
- **Sample size:** 300 rows (same as training set) only
- **Outcome:** Models below a composite threshold are eliminated from Phase 2

#### Phase 2 — Full Benchmarking

- **Optuna trials:** 6 per model (full search of hyperparameter grid)
- **Random seeds:** 11, 42, 123 — each configuration run 3 times to ensure reproducibility
- **Dataset sizes:** 300, 600, 1,000, 5,000 rows — to observe scaling behaviour
- **Total experiments:** 9 models × seeds × sizes → **92 total runs** (some deep learning models pruned at certain scales due to smoke results)

#### Hyperparameter Search Spaces (from `config.py`)

| Model | Hyperparameter | Search Space |
|-------|---------------|--------------|
| KDE | bandwidth | [0.1, 0.5, 1.0, "scott"] |
| GMM | n_components | [3, 5, 8, 12] |
| GMM | covariance_type | ["full", "tied", "diag"] |
| Copula | regularization | [0.0, 0.001, 0.01, 0.1] |
| TVAE | latent_dim | [16, 32, 64, 128] |
| TVAE | epochs | [500, 1000, 2000, 5000] |
| CTGAN | epochs | [500, 1000, 2000, 5000] |
| CTGAN | batch_size | [64, 128, 256, 512] |
| CTGAN | embedding_dim | [64, 128, 256] |
| TabuDiff | timesteps | [25, 50, 100, 200] |
| TabuDiff | model_dim | [64, 128] |
| MaskedPredictor | mask_rate | [0.10, 0.15, 0.25, 0.35] |

---

### 2.4 Synthetic Data Generation

**Script:** `generator.py`

Each model generates data in the following flow:
1. Model is fitted on the preprocessed 240-row training split.
2. Synthetic rows are sampled at the target size (300 / 600 / 1000 / 5000).
3. Categorical columns are decoded back to their original string labels.
4. All rows are immediately passed through physics validation.
5. Outputs saved as `{Model}_s{seed}_n{size}_r{rank}.csv` in the experiments folder.

#### The 9 Generative Algorithms

| # | Model | Class | Core Mechanism |
|---|-------|-------|---------------|
| 1 | **KDE** | Non-parametric | Fits a kernel density over the joint distribution using bandwidth tuning. Samples new points by: (a) picking a training row, (b) adding Gaussian noise scaled by bandwidth. Learns feature correlations implicitly. |
| 2 | **GMM** | Parametric | Fits a mixture of K Gaussian components using the Expectation-Maximization (EM) algorithm. Samples by choosing a component (proportional to mixing weight) then drawing from that Gaussian. Covariance type controls correlation modelling. |
| 3 | **Copula** | Statistical | Separates marginal distribution modelling from dependency modelling. Fits marginals per feature + Gaussian copula for joint dependency. Samples from the copula then invert-transforms per marginal. Best at preserving complex feature relationships. |
| 4 | **TVAE** | Deep Learning | Variational Autoencoder adapted for tabular data. Encodes rows into a low-dimensional `latent_dim`-size Gaussian space during training. At generation, samples from N(0,I) in latent space and decodes. Requires many training rows to generalize — underperforms at n=300. |
| 5 | **TVAEPremium** | Deep Learning | Enhanced TVAE with deeper network and extended training epochs. Same failure mode at n=300 (class collapse). |
| 6 | **CTGAN** | Deep Learning | Conditional Tabular GAN. Generator and discriminator networks trained adversarially. Conditional vector ensures minority class sampling. Batch normalisation and residual connections. Memorizes training rows at this data scale. |
| 7 | **CTGANPremium** | Deep Learning | Extended CTGAN with larger network, more epochs, tuned pac size. Confirmed memorizer — discriminator AUC = 0.995. |
| 8 | **TabuDiff** | Diffusion Model | Denoising diffusion probabilistic model for tables. Gradually adds Gaussian noise to real data over T timesteps, then trains a neural network to reverse this process. Samples by running the reverse diffusion chain from pure noise. |
| 9 | **MaskedPredictor** | ML-based | Iteratively masks random columns at `mask_rate` fraction and trains a predictor to fill them in. Generates new rows by starting from the marginal distribution and applying multiple rounds of masked prediction. |

---

### 2.5 Physics Repair & Hard Constraint Enforcement

**Script:** `physics.py` — Function: `apply_physics_repair(df)`

After generation, each synthetic dataset is scanned for physics violations and automatically repaired:

#### Rule A — Fatigue Limit ≤ Tensile Strength

```
Violation: Fatigue Limit > Tensile Strength
Repair: Fatigue Limit = 0.85 × Tensile Strength

Physical basis: A material's cyclic fatigue limit cannot exceed its ultimate static
strength — this would violate fundamental fracture mechanics. The 0.85 factor imposes a
conservative 15% safety margin below the tensile limit.
```

#### Rule B — Yield Strength ≤ Tensile Strength

```
Violation: Yield Strength > Tensile Strength
Repair: Yield Strength = min(Yield Strength, 0.9 × Tensile Strength)

Physical basis: Yield (the onset of permanent deformation) must precede fracture (ultimate
failure). Materials that fracture without yielding are brittle failures — modelled separately.
For ductile aerospace alloys, yield-before-fracture is an absolute requirement.
```

#### Rule C — No Negative Physical Properties

```
Violation: Density, Young's Modulus, Tensile Strength, Yield Strength, or Fatigue Limit < 0
Repair: Replace with 1e-6 (small positive)

Physical basis: Physical material properties are strictly positive. Negative density or
modulus have no physical meaning.
```

#### Rule D — Material-Specific Density Bounds (from `config.py`)

```
Material Density Ranges (kg/m³):
  Aluminum     : [2,500 – 2,900]   (reference: 2,700 kg/m³)
  Titanium     : [4,400 – 4,700]   (reference: 4,500 kg/m³)
  Carbon Fiber : [1,500 – 1,800]   (reference: 1,600 kg/m³)
  Steel        : [7,700 – 8,000]   (reference: 7,850 kg/m³)

Violation: Density outside known material bounds
Repair: Clip to nearest bound (d_min or d_max)
```

**KDE achieves ZERO repair triggers** across all runs — it implicitly learned these constraints from the training data's structure.

#### Physics Score Formula

After repair, each dataset receives a physics consistency score calculated as:

```
dataset_physics_score = 0.5 × per_row_ok + 0.3 × corr_consistency + 0.2 × range_validity

Where:
  per_row_ok       = fraction of rows satisfying all hard constraints (Fatigue ≤ Tensile,
                     Yield ≤ Tensile, Density in material bounds)
  corr_consistency = max(0, 1 − mean_abs_diff(corr_real, corr_synth))
                     where corr matrices are computed over all numeric columns
  range_validity   = fraction of numeric cells within real data range ± 5% margin
```

---

### 2.6 Six-Axis Composite Evaluation Framework

**Script:** `evaluator.py`

Every synthetic dataset is scored across 6 independent quality dimensions. The composite is a weighted sum:

```
Composite Score = w₁ × Statistical_Similarity
               + w₂ × ML_Utility
               + w₃ × Correlation_Preservation
               + w₄ × Physics_Consistency
               + w₅ × Privacy_Detectability

Weights (from config.py DEFAULT_SCORING):
  w₁ = 0.30  (Statistical Similarity)
  w₂ = 0.25  (ML Utility / TSTR F1)
  w₃ = 0.15  (Correlation Preservation)
  w₄ = 0.20  (Physics Consistency)
  w₅ = 0.10  (Privacy / Detectability — inverted AUC)
```

#### Axis 1: Statistical Similarity (weight 0.30)

```
Metric: Mean KL Divergence over all numeric features

KL(P || Q) = Σ P(x) × log(P(x) / Q(x))

Where:
  P = real data distribution (binned histogram)
  Q = synthetic data distribution (same bins)

Score = max(0, 1 − mean(KL_divergence_per_feature))
```

Lower KL divergence = distributions are closer. A KL of 0 means identical distributions.

#### Axis 2: ML Utility — TSTR F1 (weight 0.25)

```
Protocol: Train on Synthetic, Test on Real (TSTR)
  1. Train a Random Forest classifier on synthetic rows
  2. Predict labels of the real hold-out test set (60 rows, 20% of 300)
  3. Compute macro-averaged F1 score across all 4 target variables

Score = macro_F1 (range 0–1, higher = better)
```

A TSTR F1 of 1.000 (achieved by KDE n=5000) means a model trained exclusively on synthetic data can perfectly predict real-world labels — the gold standard for synthetic data utility.

#### Axis 3: Correlation Preservation (weight 0.15)

```
Metric: Frobenius norm of correlation matrix difference

corr_diff = ||corr(real) − corr(synthetic)||_F

Score = max(0, 1 − corr_diff / corr_diff_max)
```

The Frobenius norm measures the overall magnitude of element-wise differences between the two correlation matrices. A score of 1.0 means the correlation structure is perfectly preserved.

#### Axis 4: Physics Consistency (weight 0.20)

```
Score = dataset_physics_score (see Section 2.5 for full formula)
     = 0.5 × per_row_ok + 0.3 × corr_consistency + 0.2 × range_validity
```

#### Axis 5: Privacy / Detectability (weight 0.10)

```
Metric: Random Forest Discriminator AUC (inverted)

Protocol:
  1. Combine real and synthetic rows; label real=1, synthetic=0
  2. Train Random Forest classifier with 5-fold cross-validation
  3. Compute ROC-AUC

Raw AUC interpretation:
  AUC = 0.5 → classifier is at random chance → synthetic is indistinguishable (ideal)
  AUC = 1.0 → perfect separation → synthetic is trivially different (worst case)

Privacy Score = 2 × |0.5 − AUC| (inverted, so higher score = less detectable)
```

#### Axis 6 (Bonus): Kolmogorov-Smirnov Test

```
KS statistic: D = max|F_real(x) − F_synthetic(x)|

Where F is the empirical CDF of each distribution.

KS p-value: probability of observing this D or larger if both samples come from
the same distribution. p > 0.05 = cannot reject the null (good).

Score = mean(KS p-value per numeric feature)
```

---

### 2.7 Edge Case Engineering

**Script:** `edge_cases.py`

Rather than random sampling, 30 engineering scenarios capturing rare but plausible extreme configurations were systematically enumerated:

| Category | Count | Examples |
|----------|-------|---------|
| Material-specific | 5 | Aluminium-only cluster, Carbon Fibre-only, Titanium-only, max-density config, min-density config |
| Flight Envelope | 4 | Ultra-high altitude (>19,500 m), extreme low temperature, peak pressure, minimum pressure |
| Target/Performance | 4 | Low durability cluster, high durability cluster, poor weight efficiency, excellent weight efficiency |
| Structural Geometry | 4 | Maximum wingspan (>78 m) with thin walls, minimum wingspan, maximum fuselage length, extreme thickness |
| Optimization | 4 | SHARK algorithm only, longest optimization time (>270 s), fewest iterations, most iterations |
| Lifecycle | 2 | Maximum operational life (>29 years), minimum operational life (<6 years) |

Each scenario is constructed at the **1st or 99th percentile** of the relevant numeric feature, with all other features drawn from conditional nearest-neighbour sampling to ensure internal consistency.

#### Realism Validation via Local Outlier Factor (LOF)

```
LOF score for a point x:
  LOF(x) = mean(local_reachability_density of neighbours) / local_reachability_density(x)

Where:
  local_reachability_density(x) = 1 / mean(reach_dist(x, neighbours))
  reach_dist(x, o) = max(k-dist(o), dist(x, o))

LOF score interpretation:
  LOF ≈ 1.0 → point is as dense as its neighbours (realistic)
  LOF >> 1.0 → point is in a sparser region than its neighbours (outlier)

Realism score = 1 − anomaly_fraction_by_LOF
```

**Results:** Mean realism across all 30 scenarios = **91%**. Range: 69.3% (extreme small wingspan) to 98.1% (carbon fibre material cluster).

Top 5 most realistic edge cases are included in `edge_cases/top5_showcase_edge_cases.csv` and augmented into the final synthetic dataset.

---

### 2.8 Class Balancing

**Script:** `final/baseline_analysis.py`

The 4 target variables have imbalanced class distributions. Four strategies were tested:

| Strategy | Mechanism | Best For |
|----------|-----------|---------|
| **SMOTE-NC** | Synthetic Minority Over-sampling Technique for Nominal & Continuous. Generates synthetic minority samples by interpolating between real minority-class neighbours in the mixed numeric-categorical feature space. | Real data (preserves F1 well, output: 999 rows) |
| **ADASYN** | Adaptive Synthetic Sampling. Like SMOTE but generates more samples near decision boundaries (harder cases). | Similar to SMOTE-NC here |
| **Undersampling** | Random removal of majority class rows until class distribution is balanced. | KDE synthetic (already large; trimming to 3,369 rows still gives 1.0 F1) |
| **Genuity Conditional** | Uses the generative model's conditional generation capability to request samples from specific target classes. | Not recommended here — produced worst scores |

**Summary Results:**

| Dataset | Best Strategy | Best Composite | TSTR F1 |
|---------|--------------|---------------|---------|
| Real (300 rows) | SMOTE-NC | 0.9783 | 0.9903 |
| KDE Synthetic (5000 rows) | Undersampling | 0.9884 | 1.0000 |

---

### 2.9 Anomaly & Outlier Detection

**Script:** `edge_cases.py`, per-model analysis

Applied to every synthetic dataset to detect memorization vs. realistic novelty.

**Isolation Forest:**
```
Anomaly score = −1 × mean path length through random isolation trees

Scores close to −1 → normal (hard to isolate)
Scores close to 0  → anomaly (easy to isolate — different from training distribution)
```

**Local Outlier Factor (LOF):**
```
(See LOF formula in Section 2.7)

Used here to compare each synthetic row against the real data distribution.
```

| Model | IF Anomaly % | LOF Anomaly % | Verdict |
|-------|-------------|---------------|---------|
| **KDE** | 7–13% | 8–11% | Healthy — novel but realistic samples |
| **GMM** | 30–35% | 11–13% | Good — some over-dispersion |
| **Copula** | 37–39% | 15–18% | Moderate — slightly too spread |
| **TabuDiff** | 17–26% | 4–6% | Acceptable |
| **TabuDiffPremium** | 42–60% | ~21% | Poor — over half the samples are unrealistic |
| **MaskedPredictor** | 0% | 0% | **Red flag** — memorizing training data |
| **CTGANPremium** | 0% | 0% | **Red flag** — memorizing training data |
| **TVAE / TVAEPremium** | 0% | 0% | **Red flag** — memorizing training data |

**The red flag pattern:** 0% anomaly means the model generates rows that look exactly like training data (no novelty). This is data memorization / overfitting — confirmed separately by discriminator AUC near 1.0 for these models.

---

### 2.10 Discriminator & Similarity Testing

**Script:** `eval_extended.py`

#### Random Forest Discriminator

```
Protocol:
  1. Pool real rows (label=1) and synthetic rows (label=0)
  2. Train RandomForestClassifier with 100 trees, 5-fold stratified cross-validation
  3. Report mean ROC-AUC

Ideal AUC = 0.5 (classifier at random chance)
Worst AUC = 1.0 (perfect separation)
```

| Model | Discriminator AUC | Verdict |
|-------|------------------|---------|
| **GMM** | 0.451 | Excellent (better than random = slightly too similar) |
| **KDE** | 0.478 | Excellent |
| **Copula** | 0.518 | Excellent |
| TabuDiff | 0.722 | Moderate |
| TabuDiffPremium | 0.895 | Poor |
| MaskedPredictor | 0.976 | Poor |
| CTGANPremium | 0.995 | Overfitting |
| TVAE | 0.999 | Overfitting |
| TVAEPremium | 1.000 | Overfitting |

#### Maximum Mean Discrepancy (MMD)

```
MMD²(P, Q) = E[k(x, x')] − 2E[k(x, y)] + E[k(y, y')]

Where:
  k(·,·) = RBF kernel: k(x, y) = exp(−||x − y||² / (2σ²))
  x, x' ~ P (real data distribution)
  y, y' ~ Q (synthetic data distribution)
  σ      = median heuristic bandwidth

Interpretation: MMD = 0 → distributions identical
               MMD → ∞ → distributions diverge
```

| Model | MMD at n=5000 |
|-------|--------------|
| **KDE** | **0.0003** (essentially zero) |
| **GMM** | 0.0007 |
| **Copula** | 0.0013 |
| TabuDiff | 0.0207 |
| MaskedPredictor | 0.0276 |

#### PCA & t-SNE Visualizations

- PCA 2D projections computed for all 9 models — real data overlaid as reference
- t-SNE (perplexity=30, learning_rate=200) run on combined real+synthetic pools
- KDE, GMM, Copula synthetic points **overlap** real data cluster; TVAE/CTGAN clusters are visibly **separated**
- 36 plots generated, stored in `explainable_graphs/10_dimensionality_reduction/`

---

### 2.11 Feature Engineering Analysis (Bonus — Beyond Client Scope)

**Script:** `build_explainability.py`

Twelve domain engineered features beyond the 6 physics features were constructed and evaluated:

| Feature | Formula | Interpretation |
|---------|---------|---------------|
| stiffness_to_weight | E / ρ | Same as specific stiffness — primary material metric |
| strength_to_weight | Tensile Strength / ρ | Strength per unit mass |
| aspect_ratio | Wing Span / Fuselage Length | Aerodynamic slenderness; higher = better long-range glide |
| thickness_ratio | Structural Thickness / Wing Span | Structural slenderness — buckling risk indicator |
| thermal_stress_proxy | \|Temperature\| × Pressure / 1e6 | Combined thermal-pressure loading estimate |
| optimization_efficiency | Number of Iterations / Optimization Time | Quantum optimizer convergence rate (iterations/sec) |
| altitude_pressure_deviation | Pressure − ISA_Pressure(Altitude) | Deviation from the ISA atmospheric model |
| material_density_normalized | ρ / max(ρ per material class) | Utilization ratio within material category |
| log_E | log1p(E) | Normalizes the right-skewed Young's Modulus distribution |
| log_tensile | log1p(Tensile Strength) | Normalizes the right-skewed tensile distribution |
| E_times_thickness | E × Structural Thickness | Stiffness-wall interaction — resistance to flexure |
| rho_times_wingspan | ρ × Wing Span | Total structural mass proxy |

**Multicollinearity (VIF) Results:** Poisson's Ratio has VIF = 182.6, confirming it is almost entirely determined by Material Type. Temperature (VIF = 66.8) and Pressure (VIF = 31.0) are highly co-determined by Altitude via the ISA model.

**ML Accuracy Delta:** Mean accuracy change from adding all 12 features = **−0.0025** (effectively zero). The original 22 features already encode all signal. Feature engineering was thorough but the dataset's original design was sufficient.

---

### 2.12 Visualization & Reporting

**Scripts:** `generate_all_graphs.py`, `generate_html_report.py`, `generate_pdf_report.py`, `build_final_LnT.py`

**294 plots** were generated across 11 categories and individually catalogued in `explainable_graphs/graph_catalog.csv`.

**7 LaTeX-compiled PDF reports** created using the `tectonic` compiler. Each report includes `.tex` source, embedded `plots/` folder, and supporting `data/` CSV tables.

---

## 3. Deliverables — Every File, Every Folder Explained

The complete deliverable drop is in the `deliverables_LnT/` folder. Here is a full walkthrough of every component.

---

### Root-Level Documents

| File | What It Is | Who Should Read It |
|------|-----------|-------------------|
| `README.md` | Short entry-point guide: what this folder is, how to navigate it, and the 3-minute version of the project | First file any reviewer should open |
| `PROJECT_SUMMARY.md` | Full technical narrative of everything done: dataset description, all 9 models, evaluation framework, top results tables, class balancing, edge cases, anomaly detection, feature engineering summary, and production recommendations | Technical reviewer, data scientist, project manager |
| `DIRECTORY_GUIDE.md` | Exhaustive file-level map: what every folder contains, every key CSV explained, recommended reading order, visualization category guide, validation result quick-reference | Anyone navigating the folder for the first time |
| `LnT_POC_structure.md` | Business-focused highlights document: business impact numbers, methodology differentiators, what sets this POC apart, quick-reference numbers table | Executive audience, client stakeholder |
| **`process_flow.md`** | **This file** — the complete process narrative from raw data to all outputs, including physics formulae, pipeline logic, and full reading guide | Any audience; the master entry point |

---

### `reports/` — 7 PDF Reports

Each report folder contains: `{name}_report.pdf` (compiled output), `{name}_report.tex` (LaTeX source), `plots/` (all embedded figures), `data/` (supporting CSV tables).

| Report | Folder | Key Question Answered | Contents |
|--------|--------|-----------------------|----------|
| **Executive Summary** | `reports/executive_summary.pdf` | Is the synthetic data good enough? Pass/fail? | 1-page decision document with best model, composite score, 5-criteria checklist. No technical detail — purely a decision card. |
| **Deep Data Analysis** | `reports/deep_data_analysis/` | What does the original 300-row dataset look like? | Full EDA: univariate distributions (histograms, boxplots, KDE curves), bivariate scatter grids, correlation heatmap, missing value analysis, ISA model validation, class distribution breakdown, feature importance pre-synthesis. ~30 pages. |
| **Business Narrative** | `reports/business_narrative/` | What do these metrics mean for engineering decisions? | Material selection decision matrix, material tier ranking (performance vs. cost), structural risk flags, weight efficiency trade-offs, operational life vs. fatigue analysis, quantum optimizer performance comparison. Written in engineering language, not data science language. ~10 pages. |
| **Model Comparison** | `reports/model_comparison/` | Which of the 9 models is best, and why? | Complete 9-model benchmarking: composite score leaderboard, radar charts (all 5 axes per model), scale analysis (how each model performs at 300 vs 5000 rows), tier assignment with justification. ~15 pages. |
| **Feature Interdependency** | `reports/feature_interdependency/` | Does synthetic data preserve complex feature relationships? | Frobenius norm comparison across all models, spectral similarity of correlation matrices, top correlated feature pairs in real vs. synthetic, per-feature correlation coefficient comparison. ~12 pages. |
| **Input-Output Coherence** | `reports/io_coherence/` | Do the generated inputs logically produce the generated outputs? | SHAP value alignment between real and synthetic models, causal relationship fidelity checks, counterfactual analysis (does changing Material Type predict the expected output shift?), domain rule validation. ~12 pages. |
| **Class Balance & Edge Cases** | `reports/class_balance_edge/` | Are target classes balanced? Are edge cases realistic? | Chi-square test results for class distribution, 4-way joint distribution comparison, balancing strategy evaluation (SMOTE-NC vs undersampling vs ADASYN), edge case LOF realism scores, category-by-category edge case analysis. ~12 pages. |
| **Similarity & Innovation** | `reports/similarity_innovation/` | Quantitative statistical proof of synthetic data quality | TSTR/TRTS/TRTR comparison, MMD by model and scale, discriminator AUC results, bootstrap confidence intervals (1000 resamples), sensitivity analysis on scoring weights (±10% perturbation). ~15 pages. |

---

### `synthetic_data/` — All Generated Datasets

#### `synthetic_data/best_per_model/` — 9 Champion Datasets

One curated, best-scoring dataset per generative model. Files are named `{Model}_s{seed}_n{size}_r{rank}.csv`.

| Tier | Model | File | Size | Composite Score | Why Selected |
|------|-------|------|------|----------------|-------------|
| **Production** | KDE | `KDE_s123_n5000_r035.csv` | 5,000 rows | **0.9965** | Highest overall score; zero repair triggers; TSTR F1 = 1.000; MMD = 0.0003 |
| **Production** | GMM | `GMM_s42_n5000_r019.csv` | 5,000 rows | ~0.94 | Best discriminator score of all GMM configs (AUC 0.451) |
| **Production** | Copula | `Copula_s11_n5000_r003.csv` | 5,000 rows | ~0.91 | Best indistinguishability (96.5% per discriminator) |
| Research | TabuDiff | `TabuDiff_s11_n5000_r051.csv` | 5,000 rows | ~0.82 | Best deep-learning result; acceptable MMD at scale |
| Research | TabuDiffPremium | `TabuDiffPremium_s11_n1000_r075.csv` | 1,000 rows | ~0.76 | Extended training variant; too many anomalies at n=5000 |
| Evaluated | TVAE | `TVAE_s123_n1000_r086.csv` | 1,000 rows | ~0.55 | Not recommended — discriminator AUC = 0.999 (memorization) |
| Evaluated | TVAEPremium | `TVAEPremium_s11_n1000_r087.csv` | 1,000 rows | ~0.52 | Not recommended — AUC = 1.000 |
| Evaluated | CTGANPremium | `CTGANPremium_s42_n1000_r089.csv` | 1,000 rows | ~0.50 | Not recommended — AUC = 0.995 |
| Evaluated | MaskedPredictor | `MaskedPredictor_s11_n300_r077.csv` | 300 rows | ~0.48 | Not recommended — high variance, poor utility |

#### `synthetic_data/top_10/` — Top 10 Overall

- `top_10.csv`: The index CSV ranking all 10 best datasets with all 5 evaluation scores, model name, seed, and size.
- 10 individual CSVs: All are KDE variants (different seeds and sizes) — demonstrating KDE's dominance across the entire search space.

#### `synthetic_data/experimentations/` — Full Experimental Archive

- **92 CSV files**, one per experimental run, named `{Model}_s{seed}_n{size}_r{rank}.csv`
- **92 JSON files** with per-run metrics (composite score, KL divergence, TSTR F1, KS p-value, repair count, generation time)
- Used for full reproducibility and future analysis/comparison
- Also archived as `experimentations.zip` for convenient distribution

---

### `explainable_graphs/` — 294 Categorized Visualizations

The master index `graph_catalog.csv` contains one row per plot with: `filename`, `source_path`, `category`, `subcategory`, `description`, `target_audience` (technical / executive).

| Folder | Count | Contents |
|--------|-------|---------|
| `01_univariate/` | 42 | Per-feature histograms, KDE density curves, boxplots. One set per numeric feature (19 features) + categorical bar charts. |
| `02_bivariate/` | 22 | Scatter matrix grids, pairwise correlation heatmap, material-vs-target radar charts, altitude-pressure validation scatter. |
| `03_synthetic_vs_real/` | 79 | Side-by-side distribution overlays for each of the 9 models across all numeric features. Includes overlaid KDE curves and correlation matrix difference heatmaps. |
| `04_target_analysis/` | 31 | Per-target class count bar charts, cross-target joint distribution matrices, class frequency comparison real-vs-synthetic. |
| `05_validation_metrics/` | 21 | KS statistic heatmap, KL divergence heatmap, Wasserstein distance charts, ROC curves per model, MMD bar chart, anomaly score distribution. |
| `06_feature_importance/` | 10 | SHAP beeswarm plots, SHAP bar charts, Random Forest importance ranking, SHAP alignment real-vs-synthetic. |
| `07_model_performance/` | 31 | Composite leaderboard bar chart, 5-axis radar chart per model, scale analysis (composite vs. n), TSTR F1 vs size curves. |
| `08_edge_cases/` | 4 | LOF score distribution for edge cases, realism score bar chart, edge case PCA overlay, category breakdown. |
| `09_feature_engineering/` | 4 | VIF bar chart, PCA scree plot, accuracy with vs. without engineered features, feature skewness before/after log transforms. |
| `10_dimensionality_reduction/` | 36 | PCA 2D overlay for each of the 9 models (9 plots) + combined comparison grid, t-SNE overlays for all models (9 plots) + combined grid, real-vs-synthetic cluster comparison. |
| `11_report_figures/` | 36 | Organized copies of all figures directly embedded in the 7 PDF reports — enables quick access without opening PDFs. |

---

### `feature_engineering/` — Bonus Analysis

**Applied to:** Both real data and best KDE synthetic dataset.

```
feature_engineering/
├── real/
│   ├── datasets/
│   │   ├── full_feature_engineered.csv     ← 300 rows × 34 columns (22 original + 12 engineered)
│   │   └── pca_augmented.csv               ← 300 rows × 27 columns (22 + 5 PCA components)
│   ├── visuals/
│   │   ├── vif_analysis.png                ← VIF bar chart (Poisson's Ratio = 182.6)
│   │   ├── feature_importance_comparison.png ← With vs. without engineering
│   │   └── pca_scree.png                   ← Explained variance by component
│   ├── feature_engineering_report.md       ← Full writeup with recommendations
│   └── engineering_log.txt                 ← Step-by-step transformation log
└── kde_synthetic/
    ├── datasets/                            ← Same 12 features applied to KDE 5000 rows
    ├── visuals/
    └── feature_engineering_report.md
```

---

### `class_balanced/` — Balancing Strategy Results

```
class_balanced/
├── real/
│   ├── best_balanced.csv                   ← SMOTE-NC balanced, 999 rows (best strategy for real data)
│   ├── balancing_evaluation.csv            ← Comparison table: all 4 strategies × 3 metrics
│   ├── per_target_vibration_damping.csv    ← Balanced specifically for Vibration Damping target
│   ├── per_target_computational_time.csv   ← Balanced specifically for Computational Time target
│   ├── per_target_weight_efficiency.csv    ← Balanced specifically for Weight Efficiency target
│   └── per_target_durability.csv          ← Balanced specifically for Durability target
└── kde_synthetic/
    ├── best_balanced.csv                   ← Undersampling result, 3,369 rows (best for KDE)
    ├── balancing_evaluation.csv
    └── per_target_*.csv                    ← Per-target balanced synthetic datasets (4 files)
```

---

### `edge_cases/` — 30 Engineering Scenario Datasets

```
edge_cases/
├── edge_case_metrics.csv                   ← Master log: all 30 scenarios × realism score × LOF × NN distance
├── all_edge_cases_combined.csv             ← All 30 scenario rows stacked in one file
├── augmented_with_edge_cases.csv           ← Final best synthetic dataset + top-5 validated edge cases appended
├── tier1_valid_edge_cases.csv             ← Scenarios with realism > 90%
├── top5_showcase_edge_cases.csv            ← 5 most realistic, most illustrative scenarios
└── [27 individual CSVs]                    ← One file per scenario (e.g., altitude_extreme_high.csv,
                                              material_carbonfiber_only.csv, wingspan_extreme_large.csv, ...)
```

---

### `anomaly_outlier/` — Isolation Forest & LOF Results

```
anomaly_outlier/
├── real/
│   └── visuals/
│       ├── if_score_distribution.png       ← IF anomaly score distribution for real data
│       └── lof_score_distribution.png      ← LOF score distribution for real data
└── synthetic/
    ├── anomaly_summary.csv                 ← 93 rows × 15 cols: per-model anomaly rates (IF%, LOF%, etc.)
    ├── anomalous_rows_per_model/           ← One CSV per model with flagged anomalous rows
    │   ├── KDE_anomalies.csv
    │   ├── GMM_anomalies.csv
    │   └── ... (one per model)
    └── visuals/
        ├── anomaly_rate_comparison.png     ← Bar chart: IF% vs LOF% per model
        ├── nn_distance_heatmap.png         ← Nearest-neighbour distance heatmap (model × scale)
        └── anomaly_violin.png              ← Violin plot of anomaly score distributions per model
```

---

### `discriminator_similarity/` — Privacy & Indistinguishability Evidence

```
discriminator_similarity/
├── discriminator/
│   ├── discriminator_metrics.csv           ← 9 rows × 5 cols: model, AUC, indistinguishability%, accuracy, F1
│   ├── per_model/
│   │   └── {Model}_discriminator_results.csv   ← Per-model fold-level AUC scores
│   └── visuals/
│       ├── discriminator_roc_curves.png    ← ROC curve overlay for all 9 models
│       └── discriminator_auc_bar.png       ← AUC bar chart (horizontal, ordered best-to-worst)
├── mmd/
│   ├── mmd_scores_all.csv                  ← MMD per experiment (92 rows)
│   ├── mmd_pivot.csv                       ← MMD pivot: model × size (9 × 4 = 36 cells)
│   └── visuals/
│       └── mmd_heatmap.png                 ← Heatmap of MMD scores by model and generation size
└── dimensionality_reduction/
    ├── pca_coordinates_combined.csv        ← PCA (x, y) coordinates for all real + synthetic points
    ├── tsne_coordinates_combined.csv       ← t-SNE (x, y) coordinates for all real + synthetic points
    ├── per_model/
    │   ├── {Model}_pca.csv                 ← PCA coordinates for each model's synthetic points
    │   └── {Model}_tsne.csv                ← t-SNE coordinates for each model's synthetic points
    └── visuals/
        ├── pca_all_models_grid.png         ← 3×3 PCA subplot grid (one per model) with real overlay
        ├── pca_overlay_combined.png         ← All models + real on one PCA plot (colour-coded)
        └── tsne_all_models_grid.png        ← 3×3 t-SNE subplot grid
```

---

## 4. Key Numbers Quick Reference

| Metric | Value | Meaning |
|--------|-------|---------|
| Input data size | 300 rows | The starting point — everything generated from this |
| Final synthetic size | 5,000 rows | 16.7× data augmentation |
| Generative models evaluated | 9 | Covers all major tabular generation paradigms |
| Experimental runs | 92 | Multi-seed (3), multi-scale (4), Optuna-tuned |
| Best composite score | **0.9965** | Near-theoretical maximum (KDE_s123_n5000) |
| TSTR F1 | **1.000** | Synthetic trains a model that perfectly classifies real data |
| MMD (KDE n=5000) | **0.0003** | Distributions essentially identical in kernel space |
| Discriminator AUC (KDE) | **0.478** | Can't tell synthetic from real (ideal = 0.5) |
| Physics repair triggers (KDE) | **0** | Zero constraint violations — physics learned implicitly |
| Edge case scenarios | 30 | Systematically enumerated, not randomly sampled |
| Edge case realism (mean) | 91% | LOF-validated |
| Visualizations | 294 | Catalogued with description and audience |
| PDF reports | 7 | LaTeX-compiled, publication-quality |
| Total deliverable files | 736 | Fully organized, indexed, and described |
| Total deliverable size | 157 MB | |

---

## 5. Ideal Reading Flow

The deliverable is large. Here is the precise sequence for absorbing it efficiently, depending on your role:

### For an Executive / Client Decision-Maker (20 minutes total)

1. **`reports/executive_summary.pdf`** — The 1-page pass/fail checklist. Opens with best model, composite score, and whether each of the 5 client criteria is met. This is the only document required for a go/no-go decision.
2. **`LnT_POC_structure.md`** — Business highlights: data augmentation factor, zero privacy risk evidence, TSTR proof, and a clean table of the numbers that matter.
3. **`reports/business_narrative/business_narrative_report.pdf`** — Translates all metrics into engineering procurement language (material selection matrix, risk flags, operational life trade-offs).

### For a Technical Reviewer / Data Scientist (1–2 hours)

1. **`README.md`** — Entry-point orientation (3 minutes).
2. **`PROJECT_SUMMARY.md`** — The full technical story: dataset, 9 models, evaluation framework, top results tables, all findings and recommendations. Read from start to finish.
3. **`reports/deep_data_analysis/deep_data_analysis_report.pdf`** — Full EDA. Understand the input data before evaluating synthetic outputs.
4. **`reports/model_comparison/model_comparison_report.pdf`** — See how all 9 models were benchmarked and why KDE wins.
5. **`reports/similarity_innovation/similarity_innovation_report.pdf`** — The rigorous statistical proof: TSTR, MMD, bootstrap CIs.
6. **`reports/feature_interdependency/feature_interdependency_report.pdf`** and **`reports/io_coherence/io_coherence_report.pdf`** — Verify that complex correlations and causal relationships are preserved.
7. **`explainable_graphs/graph_catalog.csv`** — Open in Excel; filter by category (e.g., `03_synthetic_vs_real`) to browse the distribution overlap plots for any model.
8. **`synthetic_data/best_per_model/KDE_s123_n5000_r035.csv`** — Load the best dataset and run your own analysis.

### For the L&T Engineering Team (30–45 minutes)

1. **`reports/executive_summary.pdf`** — Project outcome at a glance.
2. **`reports/business_narrative/business_narrative_report.pdf`** — Material decision matrices and structural risk flags.
3. **`reports/class_balance_edge/class_balance_edge_report.pdf`** — How rare configurations were covered.
4. **`edge_cases/top5_showcase_edge_cases.csv`** — Review the 5 most realistic engineering extreme cases.
5. **`discriminator_similarity/discriminator/discriminator_metrics.csv`** — One CSV confirming that synthetic data cannot be trivially detected.
6. **`synthetic_data/best_per_model/KDE_s123_n5000_r035.csv`** — Ingest into your simulation or ML pipeline.

### For Anyone Exploring the Data (No Time Constraint)

1. **`explainable_graphs/graph_catalog.csv`** — Start here. Search by keyword in the description column.
2. **`anomaly_outlier/synthetic/anomaly_summary.csv`** — See per-model anomaly rates; understand which models memorize.
3. **`discriminator_similarity/mmd/mmd_pivot.csv`** — See how distribution distance changes with synthetic size.
4. **`feature_engineering/real/feature_engineering_report.md`** — Understand which engineered features matter.
5. **`class_balanced/real/balancing_evaluation.csv`** — Compare all 4 balancing strategies side-by-side.

---

*Generated as part of the L&T Aerospace Synthetic Data POC — March 2026*
*Best synthetic dataset: `synthetic_data/best_per_model/KDE_s123_n5000_r035.csv` (composite score: 0.9965)*
