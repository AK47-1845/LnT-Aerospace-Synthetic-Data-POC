import pandas as pd
import numpy as np
from config import CATEGORICAL_COLS, EXPECTED_COLUMNS, WEIGHTS
from utils import logger
from genuity.evaluation import evaluate_synthetic_data

def validate_minimum_bar(real_df, syn_df):
    """
    Checks if a synthetic dataframe satisfies minimum generation requirements.
    Fails if constraints violated.
    """
    # 1. 22 Columns
    if syn_df.shape[1] != EXPECTED_COLUMNS:
        return False, f"Column count mismatch: {syn_df.shape[1]} vs {EXPECTED_COLUMNS}"
    
    # 2. Exact Column Names
    if list(syn_df.columns) != list(real_df.columns):
        return False, "Column names mismatch"
    
    # 3. No Nulls
    if syn_df.isnull().sum().sum() > 0:
        return False, "Nulls present in synthetic data"
        
    # 4. Categorical Levels Exact
    for col in CATEGORICAL_COLS:
        real_uniques = set(real_df[col].dropna().unique())
        syn_uniques = set(syn_df[col].dropna().unique())
        if not syn_uniques.issubset(real_uniques):
            # Try to fix case sensitivity issues first before failing
            # But the requirement asks to fail if not case sensitive match. We'll return False.
            extra = syn_uniques - real_uniques
            return False, f"Invalid categories in {col}: {extra}"
            
    return True, "Passed"

def get_composite_score(real_df, syn_df):
    """
    Evaluates synthetic data against real data and computes a single composite score.
    Uses genuity's evaluation backend.
    """
    # 1. Minimum Bar Check
    is_valid, msg = validate_minimum_bar(real_df, syn_df)
    if not is_valid:
        logger.warning(f"Failed minimum bar: {msg}. Assigning score 0.0")
        return 0.0, None
        
    # 2. Genuity Evaluation API
    try:
        eval_results = evaluate_synthetic_data(
            real_data=real_df,
            synthetic_data=syn_df,
            target_column="Weight Efficiency", # For Utility
            categorical_columns=CATEGORICAL_COLS,
            metrics=['similarity', 'utility', 'privacy', 'detectability']
        )
        
        # 3. Extract scores (Genuity typically returns scores between 0 and 1)
        sim_score = eval_results.get('overall_scores', {}).get('similarity', 0.5)
        util_score = eval_results.get('overall_scores', {}).get('utility', 0.5)
        priv_score = eval_results.get('overall_scores', {}).get('privacy', 0.5)
        det_score = eval_results.get('overall_scores', {}).get('detectability', 0.5)
        
        # 4. Compute Weighted Composite Score
        composite = (sim_score * WEIGHTS['similarity'] +
                     util_score * WEIGHTS['utility'] +
                     priv_score * WEIGHTS['privacy'] +
                     det_score * WEIGHTS['detectability'])
                     
        return composite, eval_results
        
    except Exception as e:
        logger.error(f"Genuity evaluation failed: {e}")
        return 0.0, None
