# Genuity Documentation

> **Genuity** is a comprehensive synthetic data generation library for tabular data.

---

## Table of Contents

1. [Installation](#installation)
2. [Compliance Module](#compliance-module)
3. [Data Processor Module](#data-processor-module)
4. [Core Generator Module](#core-generator-module)
   - [CTGAN](#ctgan)
   - [TVAE](#tvae)
   - [TabuDiff](#tabudiff)
   - [Copula](#copula)
   - [Masked Predictor](#masked-predictor)
   - [Differential Privacy](#differential-privacy)

---

## Installation

```bash
pip install genuity==1.0.0
```

```python
import genuity
genuity.activate_license("YOUR_LICENSE_KEY")
```

---

## Compliance Module

The Compliance module provides PII (Personally Identifiable Information) detection and removal capabilities to ensure privacy compliance before synthetic data generation.

### Import

```python
from genuity.compliance import check_compliance_and_pii, get_pii_columns_heuristic
```

### Functions

---

#### `check_compliance_and_pii(df, api_key=None)`

Analyzes the DataFrame for PII columns and removes them.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `pd.DataFrame` | *required* | The input dataframe to analyze |
| `api_key` | `str` | `None` | OpenAI API key. If `None`, tries `OPENAI_API_KEY` env var. If unavailable, uses heuristic method |

**Returns:**

| Key | Type | Description |
|-----|------|-------------|
| `original_columns` | `list` | Original column names |
| `pii_columns_detected` | `list` | Columns identified as PII |
| `dataframe` | `pd.DataFrame` | Cleaned dataframe with PII columns removed |
| `cleaned_columns` | `list` | Column names after PII removal |
| `cleaned_data_sample` | `list[dict]` | Sample of cleaned data (first 5 rows) |

**Example:**

```python
import pandas as pd
from genuity.compliance import check_compliance_and_pii

df = pd.DataFrame({
    "user_name": ["Alice", "Bob"],
    "email": ["alice@example.com", "bob@example.com"],
    "age": [25, 30],
    "purchase_amount": [100.50, 250.00]
})

result = check_compliance_and_pii(df)
# result["pii_columns_detected"] -> ["user_name", "email"]
# result["dataframe"] -> DataFrame with only "age" and "purchase_amount"
```

---

#### `get_pii_columns_heuristic(columns)`

Identifies PII columns using keyword matching (no API required).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `columns` | `list[str]` | List of column names to analyze |

**Returns:**

`list[str]` — Column names identified as PII

**Detected Keywords:**

- **Names:** `name`, `first_name`, `last_name`, `surname`, `fullname`
- **Contact:** `email`, `phone`, `mobile`, `address`, `zip`, `postal`
- **Identifiers:** `ssn`, `passport`, `license`, `id_number`
- **Financial:** `card`, `credit`, `debit`, `bank`, `account`
- **Security:** `password`, `secret`, `token`, `credential`
- **Dates:** `dob`, `date_of_birth`, `birth`

**Example:**

```python
from genuity.compliance import get_pii_columns_heuristic

columns = ["customer_name", "email_address", "purchase_total", "phone_number"]
pii_cols = get_pii_columns_heuristic(columns)
# pii_cols -> ["customer_name", "email_address", "phone_number"]
```

---

## Data Processor Module

The Data Processor module provides preprocessing and postprocessing capabilities for tabular data, designed to work with synthetic data generators.

### Import

```python
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
```

---

### Class: `TabularPreprocessor`

Preprocesses raw tabular data for synthetic data generation.

**Features:**
- Auto-detection of column types (continuous, categorical, binary, long-text)
- Multiple imputation strategies
- One-hot encoding for categorical features
- QuantileTransformer scaling for continuous features
- Optional PCA dimensionality reduction
- Outlier detection and flagging

#### Constructor

```python
TabularPreprocessor(
    cardinality_ratio=0.05,
    min_cardinality_cap=10,
    max_cardinality_cap=50,
    outlier_iqr_multiplier=1.5,
    max_text_length=500,
    imputation_strategy="auto",
    random_state=42,
    n_pca_components=0,
    verbose=True
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cardinality_ratio` | `float` | `0.05` | Ratio of unique values to determine categorical (5% unique → categorical) |
| `min_cardinality_cap` | `int` | `10` | Minimum unique values threshold for categorical |
| `max_cardinality_cap` | `int` | `50` | Maximum unique values threshold for categorical |
| `outlier_iqr_multiplier` | `float` | `1.5` | IQR multiplier for outlier detection |
| `max_text_length` | `int` | `500` | Max character length before classifying as long-text |
| `imputation_strategy` | `str` | `"auto"` | Imputation method (see below) |
| `random_state` | `int` | `42` | Random seed for reproducibility |
| `n_pca_components` | `int` | `0` | Number of PCA components (0 = disabled) |
| `verbose` | `bool` | `True` | Print progress messages |

**Imputation Strategies:**

| Strategy | Description |
|----------|-------------|
| `"auto"` | `median` for numeric, `mode` for categorical |
| `"mean"` | Fill with column mean |
| `"median"` | Fill with column median |
| `"mode"` | Fill with most frequent value |
| `"constant"` | Fill with `0` (numeric) or `"__MISSING__"` (categorical) |
| `"quantile:q"` | Fill with q-th quantile (e.g., `"quantile:0.25"`) |
| `"random_uniform"` | Random values between min and max |
| `"random_normal"` | Random values from column's normal distribution |
| `"random"` | Random categorical value weighted by frequency |
| `"knn:k"` | K-Nearest Neighbors imputation (e.g., `"knn:5"`) |
| `"ml"` | Machine Learning imputation (RandomForest) |

---

#### Methods

##### `fit_transform(df) → dict`

Fits the preprocessor to the data and transforms it.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | Raw input dataframe |

**Returns:**

| Key | Type | Description | Usage Note |
|-----|------|-------------|------------|
| `preprocessed` | `pd.DataFrame` | Combined features (Continuous + Categorical + Flags + PCA) | **Contains metadata columns.** Do NOT pass to CTGAN directly without filtering. |
| `continuous` | `pd.DataFrame` | Scaled continuous columns | Safe for training. |
| `categorical` | `pd.DataFrame` | One-hot encoded categorical columns | Safe for training. |
| `outlier_flags` | `pd.DataFrame` | Binary outlier indicator columns | **Metadata.** Generated by default. Exclude from CTGAN training data. |
| `pca_features` | `pd.DataFrame` | PCA components (if enabled) | **Metadata.** Exclude if training on original features. |
| `long_text` | `pd.DataFrame` | Long-text columns (pass-through) | Ignored by numerical models. |

> [!WARNING]
> **Important:** The `preprocessed` DataFrame includes metadata (outlier flags, PCA) which can cause dimension mismatches in models like CTGAN. Always explicitly select/concatenate `continuous` and `categorical` parts for training if you don't want these metadata features.

**Example:**

```python
from genuity.data_processor import TabularPreprocessor
import pandas as pd

df = pd.read_csv("data.csv")
preprocessor = TabularPreprocessor(verbose=True)
result = preprocessor.fit_transform(df)

# Use preprocessed data for training
train_data = result["preprocessed"]
```

---

##### `save(filepath)`

Saves the fitted preprocessor state to disk.

```python
preprocessor.save("preprocessor.joblib")
```

---

##### `TabularPreprocessor.load(filepath) → TabularPreprocessor`

Class method to load a saved preprocessor.

```python
preprocessor = TabularPreprocessor.load("preprocessor.joblib")
```

---

##### `get_column_info() → dict`

Returns metadata about detected column types.

```python
info = preprocessor.get_column_info()
# {
#     "original_columns": [...],
#     "continuous_columns": [...],
#     "categorical_columns": [...],
#     "binary_columns": [...],
#     "long_text_columns": [...],
#     "outlier_bounds": {...},
#     "feature_names": [...],
#     "is_fitted": True
# }
```

---

##### `get_output_info() → list`

Returns metadata about one-hot encoded categorical features (for CTGAN conditional sampling).

```python
info = preprocessor.get_output_info()
# [
#     {"name": "gender", "num_categories": 2, "start_idx": 5, "end_idx": 7},
#     {"name": "city", "num_categories": 10, "start_idx": 7, "end_idx": 17}
# ]
```

---

### Class: `TabularPostprocessor`

Reconstructs original data format from preprocessed synthetic data.

#### Constructor

```python
TabularPostprocessor(
    preprocessor_path=None,
    preprocessor_object=None,
    verbose=True
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `preprocessor_path` | `str` | Path to saved preprocessor file |
| `preprocessor_object` | `TabularPreprocessor` | Fitted preprocessor instance |
| `verbose` | `bool` | Print progress messages |

> **Note:** Provide either `preprocessor_path` OR `preprocessor_object`, not both.

---

#### Methods

##### `inverse_transform_modified_data(modified_df) → pd.DataFrame`

Reconstructs original data format from preprocessed/synthetic data.

**Features:**
- Inverse scales continuous columns
- Decodes one-hot encoded categoricals via argmax
- Clips values to original data range
- Rounds numeric values to 3 decimal places
- Restores original column order

**Example:**

```python
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor

# Preprocess
preprocessor = TabularPreprocessor()
result = preprocessor.fit_transform(df)

# ... train model and generate synthetic data ...
synthetic_preprocessed = model.generate(1000)

# Postprocess
postprocessor = TabularPostprocessor(preprocessor_object=preprocessor)
synthetic_original = postprocessor.inverse_transform_modified_data(synthetic_preprocessed)
```

---

##### `transform_new_data(df) → dict`

Transforms new raw data using saved preprocessor state.

**Returns:** Same structure as `TabularPreprocessor.fit_transform()`

```python
postprocessor = TabularPostprocessor(preprocessor_path="preprocessor.joblib")
new_result = postprocessor.transform_new_data(new_df)
```

---

##### `get_column_mapping() → dict`

Returns column type metadata.

```python
mapping = postprocessor.get_column_mapping()
```

---

## Core Generator Module

The Core Generator module provides multiple synthetic data generation methods.

### Import

```python
from genuity.core_generator import (
    # CTGAN
    CTGANAPI, CTGANPremiumAPI,
    # TVAE
    TVAEAPI, TVAEPremiumAPI,
    # TabuDiff
    TabuDiffBasicAPI, TabuDiffPremiumAPI,
    # Copula
    CopulaAPI,
    # Masked Predictor
    MaskedPredictorAPI,
    # Differential Privacy
    DifferentialPrivacyProcessor, apply_differential_privacy
)
```

---

### CTGAN

Conditional Tabular GAN for synthetic data generation.

#### `CTGANAPI` (Basic)

Standard CTGAN implementation. Requires **One-Hot Encoded** data as a numpy float array.

**CRITICAL: Input Data Requirements**
1.  **Strict Dimension Match:** The input array `data` width MUST equal `len(continuous_cols) + len(categorical_cols)`.
2.  **No Metadata:** You MUST filter out outlier flags, PCA columns, or any other metadata columns from `TabularPreprocessor` before passing data to `fit()`.
3.  **Indices:** `continuous_cols` and `categorical_cols` must be lists of INTEGER INDICES (0, 1, 2...), not column names.
4.  **Output Info:** You MUST pass `output_info` (from preprocessor) for correct Gumbel-Softmax sampling.

```python
from genuity.core_generator import CTGANAPI

api = CTGANAPI()

# INCORRECT Usage (Do NOT do this):
# api.fit(df, ...)  # Error: CTGAN expects numpy array
# api.fit(data, continuous_cols=["age"], ...) # Error: Expects indices [0]
# api.fit(result['preprocessed'].values, ...) # Error: Contains metadata columns

# CORRECT Usage:
# 1. Filter data to include ONLY Continuous and One-Hot Categorical columns
# 2. Pass INDICES for these columns
api.fit(
    data=clean_numpy_data, 
    continuous_cols=[0, 1, 2], 
    categorical_cols=[3, 4, 5, 6, 7], 
    epochs=1000,
    output_info=preprocessor_output_info
)

synthetic = api.generate(n_samples=1000)
api.save("model.pt")
api.load("model.pt")
```

| Method | Parameters | Description |
|--------|------------|-------------|
| `fit` | `data` (np.ndarray)<br>`continuous_cols` (list[int])<br>`categorical_cols` (list[int])<br>`epochs` (int)<br>`output_info` (list[dict]) | Train the Model.<br>**data**: Float array of features.<br>**cols**: Indices of features.<br>**output_info**: Required for categorical sampling. |
| `generate` | `n_samples` (int) | Generate `n_samples` synthetic rows (returns float array). |
| `save` | `filepath` (str) | Save model state to disk. |
| `load` | `filepath` (str) | Load model state from disk. |

#### `CTGANPremiumAPI` (Premium)

Offers advanced architectures (`basic`, `premium`, `enterprise`) and feature importance analysis.
Inherits same **Strict Input Requirements** as Basic version.

**CRITICAL:**
- **One-Hot Encoded** float array input.
- **Filter Metadata:** Exclude outlier/PCA columns from Preprocessor.
- **Indices:** Use column indices, not names.
- **Output Info:** Required for correct sampling.

```python
from genuity.core_generator import CTGANPremiumAPI

# 1. Prepare Data (Same filtering as Basic)
# ... (see Basic example for preprocessor/filtering steps) ...

# 2. Initialize & Train
api = CTGANPremiumAPI(model_type="premium")

api.fit(
    data=clean_numpy_data, 
    continuous_cols=[0, 1, 2], 
    categorical_cols=[3, 4, 5], 
    epochs=1000,
    output_info=preprocessor_output_info,
    premium_features={
        "use_spectral_norm": True,
        "use_gradient_penalty": True
    }
)

# 3. Analyze
importance = api.get_feature_importance()
print(importance)

# 4. Generate
synthetic = api.generate(n_samples=1000)
```

| Method | Parameters | Description |
|--------|------------|-------------|
| `fit` | Same as Basic + `premium_features` (dict) | Train Premium Model. |
| `get_feature_importance` | None | Returns dict of feature importance scores. |
| `generate` | `n_samples` (int) | Generate synthetic samples. |

---

### TVAE

Tabular Variational Autoencoder for synthetic data generation.

#### `TVAEAPI` (Basic)

**Distinct Feature:** Unlike CTGAN, TVAE handles **Raw DataFrames** directly. It has an internal preprocessor (MinMaxScaler + OneHotEncoder).

**Capabilities:**
- **Auto-detection:** Automatically identifies continuous vs. categorical columns (if not provided).
- **Missing Values:** Robustly handles missing data (imputes numerics with mean, handles categorical NaNs).

**Recommended Usage:** Pass the raw DataFrame.

```python
from genuity.core_generator import TVAEAPI

api = TVAEAPI()

# Mode 1: Raw DataFrame (Recommended)
# No need for manual TabularPreprocessor!
api.fit(df, epochs=300) 

# Mode 2: Numpy (Legacy)
# api.fit(numpy_data, continuous_cols=[0,1], ...)

# Generate (returns DataFrame if input was DataFrame)
synthetic_df = api.generate(1000)
```

| Method | Description |
|--------|-------------|
| `fit(data, ...)` | Train model. Passing `pd.DataFrame` uses internal preprocessing automatically. |
| `generate(n_samples)` | Generate synthetic data (returns DataFrame if input was DataFrame) |
| `get_feature_importance()` | Get feature importance |
| `save(filepath)` | Save model |
| `load(filepath)` | Load model |

> [!IMPORTANT]
> **Constraints & Best Practices**:
> - **No DateTime**: Convert dates to timestamps (int/float) before training. Passing raw dates will treat them as high-cardinality categorical data and may crash memory.
> - **High Cardinality**: For columns with >50 categories, consider grouping them or using `TabularPreprocessor` with custom logic, as TVAE's One-Hot encoding can become expensive.
> - **Device**: TVAE automatically uses CUDA if available. Models saved on GPU can be loaded on CPU safely.

#### `TVAEPremiumAPI` (Premium)

Premium features:
- **VampPrior**: Better prior distribution
- **Cyclical KL Annealing**: Better training stability
- **Quality Gating**: Filter low-quality samples

```python
from genuity.core_generator import TVAEPremiumAPI

api = TVAEPremiumAPI(model_type="premium")

# Pass premium configuration via dictionary
api.fit(df, epochs=300, premium_features={
    "use_vamp_prior": True,
    "use_cyclical_annealing": True
})
```

---

### TabuDiff

Tabular Diffusion Models for high-quality synthetic data.

#### `TabuDiffBasicAPI` / `TabuDiffPremiumAPI`

**Requirements:**
1. **Strict Pipeline**: TabuDiff works best with `TabularPreprocessor` and `TabularPostprocessor`.
2. **Numeric Input**: The API expects numeric tensors/matrices (Numpy/Torch).
3. **Dictionary Output**: `TabularPreprocessor` returns a dictionary; extract `["preprocessed"]`.

**Complete Workflow:**

```python
from genuity.core_generator import TabuDiffBasicAPI, TabuDiffPremiumAPI
from genuity.data_processor.data_preprocess import TabularPreprocessor
from genuity.data_processor.data_postprocess import TabularPostprocessor

# 1. Preprocess
preprocessor = TabularPreprocessor()
# Note: Returns a Dict!
pre_output = preprocessor.fit_transform(df) 
# Extract the merged numeric matrix
X_train = pre_output["preprocessed"].values 

# 2. Train
api = TabuDiffBasicAPI() # or TabuDiffPremiumAPI()
# Fit directly on Numpy array
api.fit(X_train)

# 3. Generate
# Returns Matrix (DataFrame without column names or types restored yet)
syn_matrix = api.generate_dataframe(num_samples=1000)

# 4. Postprocess
# IMPORTANT: Pass preprocessor object as 'preprocessor_object' kwarg
post = TabularPostprocessor(preprocessor_object=preprocessor)

# IMPORTANT: Use 'inverse_transform_modified_data'
# And provide column names for the matrix
syn_df = post.inverse_transform_modified_data(
    pd.DataFrame(syn_matrix.values, columns=preprocessor.feature_names_)
)
```

| Method | Description |
|--------|-------------|
| `fit(data)` | Train on Numpy/Tensor/DataFrame. |
| `fit_dataframe(df)` | Wrapper for DataFrame input. |
| `generate_dataframe(n)` | Generate synthetic matrix (DataFrame). |

> [!WARNING]
> **Common Pitfalls**:
> - `TabularPostprocessor(preprocessor)` will fail. Use `TabularPostprocessor(preprocessor_object=preprocessor)`.
> - `post.inverse_transform(df)` does not exist. Use `post.inverse_transform_modified_data(df)`.

---

### Copula

Gaussian Copula for modeling multivariate distributions.

**Best for:** Smaller datasets relative to feature count, or when capturing exact correlations is critical.

**Requirements:**
1. **Indices**: You must explicitly tell Copula which columns are Continuous and which are Categorical (by index).
2. **Preprocessor Integration**: Use `TabularPreprocessor` to handle Mixed Types -> Numeric conversion.
3. **Data Type**: Accepts Numpy Array.

**Complete Workflow:**

```python
from genuity.core_generator import CopulaAPI
from genuity.data_processor.data_preprocess import TabularPreprocessor
from genuity.data_processor.data_postprocess import TabularPostprocessor

# 1. Preprocess
preprocessor = TabularPreprocessor()
pre_output = preprocessor.fit_transform(df)
# Extract the merged numeric matrix
X_train = pre_output["preprocessed"].values
output_info = preprocessor.get_output_info()

# 2. Calculate Indices
# Extract categorical ranges from output_info (start_idx to end_idx)
cat_indices = []
for info in output_info:
    cat_indices.extend(range(info['start_idx'], info['end_idx']))

# All other columns are treated as continuous
n_features = X_train.shape[1]
cont_indices = [i for i in range(n_features) if i not in cat_indices]

# 3. Fit
model = CopulaAPI()
model.fit(
    data=X_train,
    continuous_cols=cont_indices,
    categorical_cols=cat_indices,
    # CRITICAL: Tell model data is already transformed
    pretransformed=True,        
    # CRITICAL: Provide output_info for reconstruction logic
    output_info=output_info     
)

# 4. Generate
syn_matrix = model.generate(n_samples=1000)

# 5. Postprocess
post = TabularPostprocessor(preprocessor_object=preprocessor)
syn_df = post.inverse_transform_modified_data(
    pd.DataFrame(syn_matrix, columns=preprocessor.feature_names_)
)
```

| Method | Description |
|--------|-------------|
| `fit(data, continuous_cols, categorical_cols)` | Fit copula. Pass `pretransformed=True`. |
| `generate(n_samples)` | Generate synthetic samples (Numpy). |
| `save(filepath)` | Save model. |
| `load(filepath)` | Load model. |

---

### Masked Predictor

Iterative mask-and-predict synthetic data generator.

**Best for:** High-fidelity generation where capturing complex dependencies is key.

**Requirements:**
1. **Preprocessor Integration**: Requires `TabularPreprocessor` to ensure all data is numeric.
2. **Data Type**: Accepts **Pandas DataFrame** of numeric values (not Numpy).
3. **Workflow**: `Preprocessor` (Dict) -> Extract `["preprocessed"]` (DataFrame) -> `MaskedPredictor`.

**Complete Workflow:**

```python
from genuity.core_generator import MaskedPredictorAPI
from genuity.data_processor.data_preprocess import TabularPreprocessor
from genuity.data_processor.data_postprocess import TabularPostprocessor

# 1. Preprocess
preprocessor = TabularPreprocessor()
pre_output = preprocessor.fit_transform(df)
# Extract preprocessed data as DATAFRAME (not numpy)
# because MaskedPredictor needs column names to track masks
df_numeric = pre_output["preprocessed"]

# 2. Fit
api = MaskedPredictorAPI()
# Fit on numeric DataFrame
api.fit(df_numeric)

# 3. Generate
# Returns numeric DataFrame
syn_numeric_df = api.generate()

# 4. Postprocess
post = TabularPostprocessor(preprocessor_object=preprocessor)
syn_df = post.inverse_transform_modified_data(syn_numeric_df)
```

| Method | Description |
|--------|-------------|
| `fit(df)` | Fit to numeric DataFrame. |
| `generate()` | Generate synthetic DataFrame. |
| `fit_generate(df)` | Fit and generate in one step. |

---

### Differential Privacy

### Differential Privacy

Apply differential privacy to **RAW** data before processing (Input Perturbation).

**Why raw data?** Applying noise after one-hot encoding destroys the structural integrity of the features (e.g., turning 0/1 into 0.05/0.95), which confuses downstream models.

**Workflow:** `DF (Raw)` -> `DifferentialPrivacy` -> `Preprocessor` -> `Model`.

#### `DifferentialPrivacyProcessor`

```python
from genuity.core_generator import DifferentialPrivacyProcessor, TVAEAPI
from genuity.data_processor.data_preprocess import TabularPreprocessor

# 1. Apply DP to Raw Data
dp = DifferentialPrivacyProcessor(
    epsilon=1.0,           # Privacy budget (lower = more private)
    noise_scale=0.1,       # Scale factor for noise
    categorical_noise_prob=0.05
)

# Returns perturbed DataFrame (same mixed types as input)
df_private = dp.apply_dp(df_raw, method="laplace")

# 2. Preprocess (on private data)
preprocessor = TabularPreprocessor()
pre_output = preprocessor.fit_transform(df_private)
df_model_input = pre_output["preprocessed"]

# 3. Train Model
model = TVAEAPI()
model.fit(df_model_input)
syn_df = model.generate(1000)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `epsilon` | `1.0` | Privacy budget |
| `delta` | `1e-5` | Privacy parameter |
| `noise_scale` | `0.1` | Noise scaling factor |
| `categorical_noise_prob` | `0.05` | Probability of flipping categorical values |
| `numerical_noise_std` | `0.01` | Std dev for numerical noise |

**Methods:**
- `minimal`: Very small noise (default)
- `laplace`: Laplace mechanism
- `gaussian`: Gaussian mechanism

#### Quick Function

```python
from genuity.core_generator import apply_differential_privacy

df_private = apply_differential_privacy(
    df, epsilon=1.0, method="minimal",
    preserve_columns=["target"]
)
```

---

## Evaluation Module

The `genuity.evaluation` module provides a comprehensive suite for assessing the quality of synthetic data compared to real data across 5 key dimensions:
1. **Similarity**: Statistical distribution matching (KS Test, Correlation).
2. **Utility**: ML efficiency (Train on Synthetic, Test on Real).
3. **Privacy**: Risk of re-identification (Distance to Closest Record).
4. **Detectability**: Adversarial detection (Can a classifier distinguish Real vs Fake?).
5. **Missingness**: Preservation of null value patterns.

### Recommended API: `evaluate_synthetic_data`

The easiest way to run evaluations. Wraps the `UnifiedEvaluator` class.

```python
from genuity.evaluation import evaluate_synthetic_data

# 1. Load Data (DataFrames or Numpy Arrays)
results = evaluate_synthetic_data(
    real_data=real_df,
    synthetic_data=syn_df,
    target_column="income",           # Optional: for Utility metrics
    categorical_columns=["gender"],   # Optional: Auto-detected if None
    metrics=['similarity', 'utility'] # Optional: Run only specific metrics
)

# 2. Access Results
print("Overall Score:", results['overall_scores']['overall'])
print("Similarity:", results['similarity'])
```

### Class-Based API: `UnifiedEvaluator`

For more control or integration into pipelines.

```python
from genuity.evaluation import UnifiedEvaluator

evaluator = UnifiedEvaluator(
    real_data=real_df,
    synthetic_data=syn_df
)

# Run full evaluation
results = evaluator.evaluate(generate_plots=True)
```

| Function / Class | Description |
|------------------|-------------|
| `evaluate_synthetic_data(...)` | **Main Entry Point**. Auto-handles preprocessing/postprocessing differences. |
| `UnifiedEvaluator` | underlying class. |
| `ComprehensiveSyntheticEvaluator` | Low-level evaluator if you need granular control over metrics. |

---

## API Input Format Reference

| API | Data Input | `continuous_cols` | `categorical_cols` |
|-----|------------|-------------------|-------------------|
| **TVAEAPI** | DataFrame or ndarray | Column **names** (optional, auto-detected) | Column **names** (optional) |
| **TVAEPremiumAPI** | DataFrame or ndarray | Column **names** (optional, auto-detected) | Column **names** (optional) |
| **CTGANAPI** | **numpy array** (preprocessed) | Column **INDICES** (required) | Column **INDICES** (required) |
| **CTGANPremiumAPI** | **numpy array** (preprocessed) | Column **INDICES** (required) | Column **INDICES** (required) |
| **CopulaAPI** | **numpy array** (preprocessed) | Column **INDICES** (required) | Column **INDICES** (required) |
| **TabuDiffBasicAPI** | DataFrame | Not needed | Not needed |
| **TabuDiffPremiumAPI** | DataFrame | Not needed | Not needed |
| **MaskedPredictorAPI** | DataFrame | Not needed | Not needed |

> **Key Insight**: 
> - **TVAE, TabuDiff, MaskedPredictor** handle preprocessing internally — pass raw DataFrames directly.
> - **CTGAN, Copula** require preprocessed numpy arrays with column indices.

---

## Complete Workflow Examples

### Example 1: TVAE (Simple — Recommended)

TVAE handles preprocessing internally, so you can pass raw DataFrames:

```python
import pandas as pd
from genuity.compliance import check_compliance_and_pii
from genuity.core_generator import TVAEAPI

# 1. Load data
df = pd.read_csv("customer_data.csv")

# 2. Remove PII
compliance_result = check_compliance_and_pii(df)
clean_df = compliance_result["dataframe"]

# 3. Train TVAE (handles preprocessing internally)
model = TVAEAPI()
model.fit(clean_df, epochs=100)  # Pass raw DataFrame directly

# 4. Generate synthetic data (returns DataFrame)
synthetic_df = model.generate(1000)

# 5. Save
synthetic_df.to_csv("synthetic_data.csv", index=False)
```

### Example 2: CTGAN (Correct Workflow)

CTGAN requires a specific data format: ONE-HOT ENCODED categorical columns, but converted to a float array. It also strictly requires that the input array dimensions match the model configuration.

**CRITICAL: `TabularPreprocessor` adds metadata columns (Outlier Flags, PCA features) by default. You MUST filter these out before passing data to CTGAN.**

```python
from genuity.data_processor import TabularPreprocessor, TabularPostprocessor
from genuity.core_generator import CTGANAPI
import pandas as pd
import numpy as np

# 1. Load Data
df = pd.read_csv("data.csv")

# 2. Preprocess
preprocessor = TabularPreprocessor(verbose=True)
result = preprocessor.fit_transform(df)

# ======================================================================
# 3. FILTER COLUMNS (CRITICAL STEP)
# CTGAN only supports Continuous and One-Hot Categorical columns.
# TabularPreprocessor adds 'outlier_flags' and 'pca_features' which 
# MUST be excluded to prevent dimension mismatches.
# ======================================================================

cont_df = result['continuous']
cat_df = result['categorical']
training_data = pd.concat([cont_df, cat_df], axis=1)

# 4. Setup Indices
n_continuous = cont_df.shape[1]
n_total = training_data.shape[1]

continuous_indices = list(range(n_continuous))
categorical_indices = list(range(n_continuous, n_total))
output_info = preprocessor.get_output_info()

# 5. Train
data = training_data.values.astype(np.float32)
model = CTGANAPI()
model.fit(
    data, 
    continuous_cols=continuous_indices, 
    categorical_cols=categorical_indices,
    epochs=100,
    output_info=output_info
)

# 6. Generate
synthetic_raw = model.generate(n_samples=1000)
fake_df_raw = pd.DataFrame(synthetic_raw, columns=training_data.columns)

# 7. Postprocess
# Postprocessor automatically handles the missing filtered columns
postprocessor = TabularPostprocessor(preprocessor_object=preprocessor)
synthetic_data = postprocessor.inverse_transform_modified_data(fake_df_raw)
```

### Example 3: TabuDiff (Simple)

```python
import pandas as pd
from genuity.core_generator import TabuDiffBasicAPI

df = pd.read_csv("data.csv")

api = TabuDiffBasicAPI()
api.fit_dataframe(df, verbose=True)
synthetic_df = api.generate_dataframe(num_samples=1000)
```

---


---

## Utils Module

The `genuity.utils` module provides helper functions for logging, visualization, and device management.

### Device Utils (`genuity.utils.device`)

Handle PyTorch device selection (CPU/CUDA/MPS).

```python
from genuity.utils.device import get_device, get_device_info

device = get_device()  # Returns torch.device('cuda') if available
info = get_device_info()
print(info)
```

### Logger Utils (`genuity.utils.logger`)

Standardized logging for the library.

```python
from genuity.utils.logger import setup_logger

logger = setup_logger("my_model")
logger.info("Training started...")
```

### Visual Utils (`genuity.utils.visual`)

Beautiful terminal output and progress tracking.

```python
from genuity.utils.visual import print_banner, print_success, print_metrics_table

print_banner("Training Complete")
print_success("Model saved successfully")

metrics = {"Accuracy": 0.95, "Loss": 0.02}
print_metrics_table(metrics, "Results")
```

---

*Documentation generated for Genuity v1.0.0*
