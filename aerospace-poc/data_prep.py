import os
import pandas as pd
import numpy as np
from config import DATA_PATH, EXPECTED_COLUMNS, MODELS_DIR
from utils import logger
from genuity.compliance import check_compliance_and_pii
from genuity.data_processor import TabularPreprocessor

def prepare_data():
    logger.info("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # Validation
    if df.shape[1] != EXPECTED_COLUMNS:
        raise ValueError(f"Expected {EXPECTED_COLUMNS} columns, got {df.shape[1]}")
    if df.isnull().values.any():
        logger.warning("Dataset contains nulls! Dropping for simplicity in baseline models.")
        df = df.dropna()
    
    logger.info(f"Dataset shape after load/dropna: {df.shape}")

    # PII Check
    result = check_compliance_and_pii(df)
    pii_cols = result.get("pii_columns_detected", [])
    if pii_cols:
        logger.warning(f"Detected PII columns: {pii_cols}")
    df_clean = result["dataframe"]
    
    # Preprocessing
    logger.info("Fitting TabularPreprocessor...")
    preprocessor = TabularPreprocessor(random_state=42, verbose=False)
    # Fit
    pre_result = preprocessor.fit_transform(df_clean)
    
    # Save
    prep_path = os.path.join(MODELS_DIR, "preprocessor.joblib")
    preprocessor.save(prep_path)
    logger.info(f"Saved preprocessor to {prep_path}")
    
    # For CTGAN and Copula we need continuous and one-hot categorical matrices combined, without metadata
    # as per genuity documentation: 
    #   "CRITICAL: Filter Metadata: Exclude outlier/PCA columns from Preprocessor"
    cont_df = pre_result['continuous']
    cat_df = pre_result['categorical']
    training_data_filtered = pd.concat([cont_df, cat_df], axis=1)
    
    n_continuous = cont_df.shape[1]
    n_total = training_data_filtered.shape[1]
    
    continuous_indices = list(range(n_continuous))
    categorical_indices = list(range(n_continuous, n_total))
    
    output_info = preprocessor.get_output_info()
    
    # Prepare all formats needed by various models
    dataset_info = {
        "df_raw": df_clean, # used by TVAE, MaskedPredictor, DP, TabuDiff
        "numpy_filtered": training_data_filtered.values.astype(np.float32), # used by CTGAN, Copula
        "cols_filtered": training_data_filtered.columns.tolist(),
        "continuous_indices": continuous_indices,
        "categorical_indices": categorical_indices,
        "output_info": output_info,
        "preprocessor": preprocessor
    }
    
    logger.info("Data preparation completed.")
    return dataset_info

if __name__ == "__main__":
    _ = prepare_data()
