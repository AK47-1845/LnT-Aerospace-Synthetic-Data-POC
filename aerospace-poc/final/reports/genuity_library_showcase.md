# Genuity Synthetic Data Generation Library — Showcase Document

**Version:** 1.0.0
**Domain:** Aerospace & High-Fidelity Tabular Data
**Classification:** Internal Technical Documentation

---

## 1. Overview

### 1.1 What Is Genuity?

Genuity is a proprietary tabular synthetic data generation suite designed to address the growing need for high-fidelity, privacy-preserving synthetic datasets in engineering and scientific domains. Built as version 1.0.0, Genuity provides a unified API that abstracts across multiple generation paradigms — from classical statistical resampling to state-of-the-art deep generative models — while embedding compliance and privacy controls directly into the pipeline.

The library was developed in response to a common but underserved problem: organizations that hold sensitive tabular data (engineering test results, structural simulations, proprietary telemetry) need synthetic copies they can share, augment, and use for downstream ML tasks — without exposing real records and without sacrificing statistical fidelity.

### 1.2 Architecture

Genuity is built as a modular Python package with five core submodules:

```
genuity/
├── data_processor/       # Preprocessing and postprocessing pipelines
│   ├── TabularPreprocessor
│   ├── TabularPostprocessor
│   └── DifferentialPrivacyProcessor
├── core_generator/       # Model classes for all generation paradigms
│   ├── CTGANAPI
│   ├── CTGANPremiumAPI
│   ├── TVAEAPI
│   ├── TVAEPremiumAPI
│   ├── TabuDiffBasicAPI
│   ├── TabuDiffPremiumAPI
│   ├── CopulaAPI
│   └── MaskedPredictorAPI
├── evaluation/           # Tiered evaluation metrics
│   ├── Tier1Evaluator    # Schema, ranges, nulls, row count
│   └── Tier2Evaluator    # KS, TSTR, TRTS, FI-MAE, MMD, discriminator AUC
├── compliance/           # PII detection and regulatory checks
│   └── check_compliance_and_pii
└── utils/                # Logging, serialization, helpers
```

Each submodule is independently importable, and the top-level `genuity` namespace provides convenience wrappers for the most common workflows.

### 1.3 Why Genuity Was Built

Existing open-source tools such as SDV, CTGAN (standalone), and Gretel each solve parts of the problem but share a common limitation: they do not provide a principled framework for *selecting* the right generation strategy for a given dataset. A practitioner using CTGAN on a physics-constrained aerospace dataset will obtain plausible-looking marginal distributions while violating the precise mathematical relationships between features — making the synthetic data useless for downstream ML tasks.

Genuity was built around three core design principles:

1. **Unified API**: All generation paradigms expose the same `fit`, `generate`, and `evaluate` interface, enabling systematic A/B comparisons.
2. **Built-in evaluation**: Every generation run automatically produces a composite quality score, making it impossible to ship synthetic data without a documented fidelity certificate.
3. **Compliance first**: PII detection and differential privacy are first-class citizens of the pipeline, not afterthoughts.

---

## 2. Model Catalogue

Genuity ships with nine model classes spanning four algorithmic families.

| Model | Class | Algorithm Type | Key Parameters | When to Use |
|---|---|---|---|---|
| CTGAN | `CTGANAPI` | GAN (Conditional Tabular GAN) | `epochs`, `batch_size`, `embedding_dim` | Large datasets, complex categorical distributions |
| CTGANPremium | `CTGANPremiumAPI` | Enhanced CTGAN with tuned discriminator | `epochs`, `batch_size`, `embedding_dim`, `discriminator_steps` | Production use with categorical-heavy schemas |
| TVAE | `TVAEAPI` | Variational Autoencoder | `latent_dim`, `epochs` | Continuous-heavy datasets with smooth distributions |
| TVAEPremium | `TVAEPremiumAPI` | Enhanced TVAE with KL annealing | `latent_dim`, `epochs`, `beta` | Production use requiring improved reconstruction |
| TabuDiffBasic | `TabuDiffBasicAPI` | Tabular Diffusion Model | `diffusion_steps`, `noise_schedule` | When feature importance alignment matters more than marginals |
| TabuDiffPremium | `TabuDiffPremiumAPI` | Enhanced Diffusion with conditioning | `diffusion_steps`, `noise_schedule`, `conditioning` | Premium diffusion for structured tabular data |
| Copula | `CopulaAPI` | Gaussian Copula | `covariance_type` | Preserving pairwise correlations in low-dimensional data |
| MaskedPredictor | `MaskedPredictorAPI` | Masked autoregressive model | `mask_ratio`, `hidden_dim` | Sequential or structured data with known feature order |
| DP-TVAE | `TVAEAPI` + `DifferentialPrivacyProcessor` | VAE with Differential Privacy | `epsilon`, `delta`, `latent_dim` | Privacy-sensitive applications with regulatory requirements |

### 2.1 Model Family Descriptions

#### GAN Family (CTGAN, CTGANPremium)

Conditional Tabular GAN (Xu et al., 2019) is the most widely cited deep learning baseline for tabular synthesis. Genuity's `CTGANAPI` wraps the reference implementation with the library's preprocessing and evaluation pipelines. `CTGANPremiumAPI` adds:

- Spectral normalization on the discriminator for training stability
- Adaptive learning rate scheduling
- Automatic mode-specific normalization for skewed continuous columns

**Characteristic behavior**: GANs excel when the training dataset is large (>5,000 rows) and the target distribution is high-entropy. On small, physics-constrained datasets, mode collapse and training instability are common failure modes.

#### VAE Family (TVAE, TVAEPremium, DP-TVAE)

Tabular VAE encodes each row into a continuous latent space and decodes synthetic rows by sampling from the learned posterior. The VAE objective explicitly balances reconstruction fidelity (ELBO reconstruction term) against latent space regularity (KL divergence term).

`TVAEPremiumAPI` introduces beta-annealing to reduce posterior collapse on sparse categorical columns. `DP-TVAE` combines the standard TVAE with Genuity's `DifferentialPrivacyProcessor`, which applies the Gaussian mechanism to gradients during training, providing (epsilon, delta)-differential privacy guarantees.

**Characteristic behavior**: VAEs tend to over-smooth distributions, producing synthetic data that looks statistically plausible at the marginal level but lacks the sharp boundaries present in physics datasets.

#### Diffusion Family (TabuDiffBasic, TabuDiffPremium)

TabuDiff adapts the denoising diffusion probabilistic model (DDPM) framework to tabular data by treating each row as a vector in mixed continuous-categorical space. The forward process gradually adds Gaussian noise to continuous columns while applying discrete corruption to categorical columns. The reverse process learns to denoise.

**Characteristic behavior**: TabuDiff shows an interesting property: even when its marginal distributions diverge from the real data (KS pass rate 0.43 at 1,000 rows), its **feature importance rankings** remain well-aligned with real data. This makes TabuDiff suitable for explainability studies where the relative importance of features matters more than exact value ranges.

#### Statistical Family (Copula, MaskedPredictor)

`CopulaAPI` fits a Gaussian copula to the real data, capturing pairwise rank correlations before sampling from the fitted joint distribution. This is computationally inexpensive and produces well-calibrated correlations, but assumes Gaussian dependence structure.

`MaskedPredictorAPI` implements a masked autoregressive approach: features are ordered, and each feature is predicted conditioned on a random mask of the others. This preserves conditional dependencies but requires a meaningful feature ordering.

---

## 3. API Reference

### 3.1 TabularPreprocessor

The `TabularPreprocessor` class handles all data transformations required before passing data to a generative model. It applies column-type-specific transformations and stores the inverse mappings for postprocessing.

```python
from genuity.data_processor import TabularPreprocessor

preprocessor = TabularPreprocessor(
    categorical_columns=['material_type', 'load_case', 'failure_mode'],
    continuous_columns=['thickness_mm', 'youngs_modulus_gpa', 'yield_strength_mpa'],
    target_columns=['safety_factor', 'mass_kg']
)

# Fit on real data and transform
transformed_data = preprocessor.fit_transform(real_df)

# Retrieve output info for model construction
output_info = preprocessor.get_output_info()
# Returns: list of (dim, activation) tuples per column
```

**Key methods:**

| Method | Signature | Description |
|---|---|---|
| `fit_transform` | `(df: pd.DataFrame) -> np.ndarray` | Fit transformations and return encoded array |
| `transform` | `(df: pd.DataFrame) -> np.ndarray` | Apply fitted transformations |
| `get_output_info` | `() -> List[Tuple]` | Return (dim, activation) list for model input layer |
| `get_column_types` | `() -> Dict` | Return inferred column type mapping |

### 3.2 TabularPostprocessor

The `TabularPostprocessor` inverts the preprocessing transformations, converting raw model output arrays back to human-readable DataFrames.

```python
from genuity.data_processor import TabularPostprocessor

postprocessor = TabularPostprocessor(preprocessor)

# Convert raw model output to DataFrame
synthetic_df = postprocessor.inverse_transform_modified_data(
    raw_output,           # np.ndarray from generator
    column_names=real_df.columns.tolist()
)
```

**Key methods:**

| Method | Signature | Description |
|---|---|---|
| `inverse_transform_modified_data` | `(data: np.ndarray, column_names: List[str]) -> pd.DataFrame` | Full inverse transform to DataFrame |
| `clip_to_training_range` | `(df: pd.DataFrame) -> pd.DataFrame` | Clip out-of-range values to training bounds |
| `enforce_categorical_vocabulary` | `(df: pd.DataFrame) -> pd.DataFrame` | Replace unseen category values with nearest match |

### 3.3 DifferentialPrivacyProcessor

The `DifferentialPrivacyProcessor` implements the Gaussian mechanism for gradient-level differential privacy. It integrates with any VAE-based model in the Genuity ecosystem.

```python
from genuity.data_processor import DifferentialPrivacyProcessor

dp = DifferentialPrivacyProcessor(
    epsilon=1.0,           # Privacy budget (lower = more private)
    delta=1e-5,            # Failure probability
    max_grad_norm=1.0,     # Gradient clipping threshold
    noise_multiplier=1.1   # Gaussian noise scale
)

# Apply DP to gradients during training
clipped_gradients = dp.apply_dp(gradients, batch_size=256)
```

**Privacy accounting**: The processor uses the moments accountant method to track cumulative privacy cost across training steps, automatically halting training if the budget would be exceeded.

### 3.4 check_compliance_and_pii

The compliance module provides automated PII detection and removal before any data enters the generation pipeline.

```python
from genuity.compliance import check_compliance_and_pii

cleaned_df, report = check_compliance_and_pii(
    df=raw_df,
    pii_patterns=['email', 'phone', 'ssn', 'name', 'ip_address'],
    regulatory_framework='GDPR',   # or 'HIPAA', 'CCPA', 'none'
    action='redact'                # or 'remove_column', 'hash'
)

print(report.pii_columns_detected)
print(report.compliance_status)
```

**Supported PII patterns**: email addresses, phone numbers, SSN/NIN, full names, IP addresses, credit card numbers, dates of birth, postal codes, free-text fields with high cardinality.

---

## 4. Benchmark Results on Aerospace Dataset

The Genuity evaluation suite was validated on a real-world aerospace structural design dataset. Full results are documented in `model_comparison_report.md`. A summary leaderboard is provided below.

### 4.1 Dataset Description

- **Rows**: 300 (real training data)
- **Features**: 22 (18 continuous, 3 categorical, 1 ID)
- **Targets**: 4 (safety_factor, deflection_mm, mass_kg, resonant_frequency_hz)
- **Material classes**: 3 (aluminium alloy, carbon fibre composite, titanium alloy)
- **Domain**: Aerospace structural design — features are physics-constrained (e.g., von Mises stress is a deterministic function of geometry and material properties)

### 4.2 Evaluation Framework

**Tier 1 (Validity)**: Schema compliance, value range checks, null count, row count match. Binary pass/fail.

**Tier 2 (Fidelity)**: Quantitative metrics computed across all numeric columns.

| Metric | Formula / Method | Weight in Composite |
|---|---|---|
| KS Pass Rate | Fraction of columns passing Kolmogorov-Smirnov test (p > 0.05) | — |
| TSTR F1 | Train-on-Synthetic, Test-on-Real macro F1 on material classification | 30% |
| FI-MAE | Mean absolute error of feature importance ranks (XGBoost) | 20% |
| Discriminator AUC | Random Forest AUC distinguishing real vs synthetic | 10% |
| MMD | Maximum Mean Discrepancy (RBF kernel) | 10% |
| KL Divergence | Average KL divergence across marginals | 30% |

**Composite Score** = 0.30 × (1 − KL) + 0.30 × TSTR_F1 + 0.20 × (1 − FI_MAE) + 0.10 × (1 − disc_AUC) + 0.10 × (1 − MMD)

### 4.3 Leaderboard

| Rank | Model | n_rows | Composite | TSTR | KS Pass | Notes |
|---|---|---|---|---|---|---|
| 1 | **Empirical (KDE+noise)** | 1000 | **0.9503** | **0.9658** | **1.0000** | Winner |
| 2 | Empirical (KDE+noise) | 600 | 0.9286 | 0.9142 | 1.0000 | Reduced size |
| 3 | TabuDiffBasic | 1000 | 0.6901 | 0.3784 | 0.4286 | FI alignment only |
| 4 | MaskedPredictor | 1000 | 0.3977 | 0.3883 | 0.0714 | Marginals violated |
| 5 | CTGAN | 1000 | 0.2511 | 0.3317 | 0.0000 | Mode collapse |
| 6 | TVAE | 1000 | <0.30 | <0.32 | 0.0000 | Over-smoothing |
| 7 | DP-TVAE (ε=1.0) | 1000 | ~0.25 | ~0.32 | 0.0000 | Privacy cost |

See `reports/model_comparison_report.md` for full per-metric breakdowns, confidence intervals, and per-column KS statistics.

---

## 5. Unique Capabilities

### 5.1 Built-in PII Compliance Checking

Unlike standalone generative model libraries, Genuity treats compliance as a prerequisite, not an option. Before any data enters the generation pipeline, `check_compliance_and_pii` scans for 15 categories of personally identifiable information using both regex patterns and statistical heuristics (e.g., detecting free-text columns with suspiciously high cardinality that may encode names or identifiers).

The compliance report is stored alongside every generated dataset, creating an auditable chain of custody suitable for GDPR Article 25 (data protection by design) documentation.

### 5.2 Differential Privacy with Configurable Epsilon

The `DifferentialPrivacyProcessor` provides (ε, δ)-differential privacy with full privacy budget accounting. Users can configure:

- `epsilon`: Privacy budget (0.1 = very strong privacy, 10.0 = weak privacy). Standard regulatory guidance suggests ε ≤ 1.0 for sensitive data.
- `delta`: Failure probability (typically 1e-5).
- Automatic training halt when budget is exhausted.
- Privacy-utility trade-off reporting: the composite score and TSTR for DP-TVAE vs standard TVAE are both logged, quantifying the privacy cost.

**Observed trade-off (aerospace dataset)**: DP-TVAE at ε=1.0 reduces composite score by approximately 0.05 compared to standard TVAE. Both models substantially underperform empirical methods, confirming that the dominant challenge is joint distribution fidelity, not privacy.

### 5.3 Unified Preprocessing/Postprocessing Pipeline

A critical problem with mixing generation libraries is that each has its own internal representation. Genuity's `TabularPreprocessor` and `TabularPostprocessor` provide a single canonical representation that all model classes consume and produce. This means:

- Mixed-type datasets (continuous + categorical + ordinal) are handled transparently.
- Postprocessed outputs are guaranteed to satisfy the original schema (data types, value ranges, categorical vocabularies).
- Switching from CTGAN to TVAE requires changing exactly one line of code.

### 5.4 TabuDiff: Diffusion Models Preserve Feature Importances

One of the most practically significant findings from the aerospace benchmark is that TabuDiffBasic, despite achieving a KS pass rate of only 0.43 (meaning 57% of continuous columns fail the Kolmogorov-Smirnov test), achieves a **feature importance MAE** comparable to the empirical baseline.

This means that while TabuDiff's synthetic values are not numerically accurate, the *relative importance* of features in predicting the target is preserved. For use cases where an engineering team wants to run feature selection or sensitivity analysis on synthetic data — without needing the exact value distributions — TabuDiff provides a useful alternative to purely statistical methods.

This property is not accidental: TabuDiff's denoising objective implicitly learns which features are most predictive of others, encoding a form of conditional structure that persists even when marginal fidelity degrades.

---

## 6. Usage Guide

### 6.1 Installation

```bash
pip install genuity==1.0.0
# or from source:
pip install -e ./genuity
```

### 6.2 Quick Start: Empirical Generation

The empirical generator (KDE resampling with Gaussian noise injection) is Genuity's highest-performing model on physics-constrained datasets and the recommended starting point.

```python
import pandas as pd
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
from genuity.core_generator import EmpiricalAPI
from genuity.evaluation import Tier1Evaluator, Tier2Evaluator
from genuity.compliance import check_compliance_and_pii

# 1. Load real data
real_df = pd.read_csv('data/aerospace_structural.csv')

# 2. Compliance check
clean_df, compliance_report = check_compliance_and_pii(real_df)
print(f"PII columns removed: {compliance_report.pii_columns_detected}")

# 3. Preprocess
preprocessor = TabularPreprocessor(
    categorical_columns=['material_type', 'load_case', 'failure_mode']
)
transformed = preprocessor.fit_transform(clean_df)

# 4. Fit and generate
generator = EmpiricalAPI(
    n_samples=1000,
    bandwidth='scott',         # KDE bandwidth selection
    noise_std_fraction=0.01    # 1% Gaussian noise injection
)
generator.fit(transformed, output_info=preprocessor.get_output_info())
synthetic_raw = generator.generate(n=1000)

# 5. Postprocess
postprocessor = TabularPostprocessor(preprocessor)
synthetic_df = postprocessor.inverse_transform_modified_data(
    synthetic_raw, column_names=clean_df.columns.tolist()
)

# 6. Evaluate
tier1 = Tier1Evaluator()
tier1_result = tier1.evaluate(real_df=clean_df, synthetic_df=synthetic_df)
print(f"Tier 1 passed: {tier1_result.all_passed}")

tier2 = Tier2Evaluator(target_column='material_type')
tier2_result = tier2.evaluate(real_df=clean_df, synthetic_df=synthetic_df)
print(f"Composite score: {tier2_result.composite_score:.4f}")
print(f"TSTR F1: {tier2_result.tstr_f1:.4f}")
print(f"KS pass rate: {tier2_result.ks_pass_rate:.4f}")

# 7. Save
synthetic_df.to_csv('synthetic_data/synthetic_aerospace_data.csv', index=False)
```

### 6.3 Switching Models

Because all generators share the same API, switching from empirical to CTGAN requires only changing the model instantiation:

```python
# Replace EmpiricalAPI with any model class:
from genuity.core_generator import CTGANAPI

generator = CTGANAPI(
    epochs=300,
    batch_size=500,
    embedding_dim=128
)
generator.fit(transformed, output_info=preprocessor.get_output_info())
```

### 6.4 Adding Differential Privacy

```python
from genuity.data_processor import DifferentialPrivacyProcessor
from genuity.core_generator import TVAEAPI

dp_processor = DifferentialPrivacyProcessor(epsilon=1.0, delta=1e-5)

generator = TVAEAPI(
    latent_dim=128,
    epochs=300,
    dp_processor=dp_processor    # Pass DP processor to VAE
)
generator.fit(transformed, output_info=preprocessor.get_output_info())
```

### 6.5 Running a Full Comparison

To reproduce the aerospace benchmark or run a systematic comparison on a new dataset:

```python
from genuity.core_generator import (
    EmpiricalAPI, CTGANAPI, TVAEAPI,
    TabuDiffBasicAPI, MaskedPredictorAPI, CopulaAPI
)

models = {
    'empirical': EmpiricalAPI(n_samples=1000),
    'ctgan': CTGANAPI(epochs=300, batch_size=500),
    'tvae': TVAEAPI(latent_dim=128, epochs=300),
    'tabdiff': TabuDiffBasicAPI(diffusion_steps=1000),
    'masked': MaskedPredictorAPI(mask_ratio=0.15),
    'copula': CopulaAPI(covariance_type='full'),
}

results = {}
for name, model in models.items():
    model.fit(transformed, output_info=preprocessor.get_output_info())
    synthetic_raw = model.generate(n=1000)
    synthetic_df = postprocessor.inverse_transform_modified_data(
        synthetic_raw, column_names=clean_df.columns.tolist()
    )
    tier2_result = tier2.evaluate(real_df=clean_df, synthetic_df=synthetic_df)
    results[name] = tier2_result.composite_score
    print(f"{name}: {tier2_result.composite_score:.4f}")

best_model = max(results, key=results.get)
print(f"\nBest model: {best_model} (score: {results[best_model]:.4f})")
```

### 6.6 Interpreting Results

| Composite Score | Interpretation | Recommendation |
|---|---|---|
| ≥ 0.90 | Excellent fidelity | Safe for downstream ML training |
| 0.75 – 0.90 | Good fidelity | Suitable for most analytics use cases |
| 0.50 – 0.75 | Moderate fidelity | Use with caution; check specific metrics |
| 0.30 – 0.50 | Poor fidelity | Investigate which metrics are failing |
| < 0.30 | Very poor fidelity | Do not use for ML; re-evaluate approach |

The composite score is designed to be conservative: a model must simultaneously achieve good performance on distributional fidelity (KL, KS), predictive utility (TSTR), and indistinguishability (discriminator AUC) to score above 0.75.

---

## 7. Roadmap

Future versions of Genuity will include:

- **v1.1**: RESTful API wrapper for integration with data pipelines
- **v1.2**: Time-series extension (LSTM-based generation for sequential aerospace telemetry)
- **v1.3**: Multi-table synthesis with referential integrity constraints
- **v2.0**: Foundation model fine-tuning approach for tabular data

---

*Genuity v1.0.0 — Internal Documentation. Not for external distribution.*
