"""
Class-Balanced Synthetic Dataset Creator
Creates balanced_1000.csv with equal class representation across all 4 targets.
Strategy: Conditional empirical resampling — sample equally from each class combination.
"""
import os
import sys
import logging
import numpy as np
import pandas as pd
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

REAL_PATH  = r"d:\aero\aerospace_structural_design_dataset.csv"
SYN_PATH   = r"d:\aero\final\per_model_datasets\empirical_1000.csv"
OUT_PATH   = r"d:\aero\final\synthetic_data\balanced_1000.csv"
TARGET_N   = 1000
SEED       = 11
TARGETS    = ["Vibration Damping", "Computational Time", "Weight Efficiency", "Durability"]

TARGET_LEVELS = {
    "Vibration Damping": ["Low", "Moderate", "High"],
    "Computational Time": ["Short", "Medium", "Long"],
    "Weight Efficiency":  ["Poor", "Good", "Excellent"],
    "Durability":         ["Low", "Medium", "High"],
}


def add_noise(df, real_df, noise_factor=0.008, seed=SEED):
    """Add slight noise to numeric columns to increase diversity."""
    rng = np.random.RandomState(seed)
    num_cols = real_df.select_dtypes(include=np.number).columns.tolist()
    result = df.copy()
    for col in num_cols:
        if col not in result.columns:
            continue
        std = real_df[col].std()
        noise = rng.normal(0, std * noise_factor, size=len(result))
        result[col] = result[col] + noise
        r_min, r_max = real_df[col].min(), real_df[col].max()
        result[col] = result[col].clip(r_min, r_max)
    return result


def balance_sequentially(syn_df, real_df, target_n=TARGET_N, seed=SEED):
    """
    Balance all 4 targets sequentially.
    For each target, ensure equal representation via oversampling.
    """
    rng = np.random.RandomState(seed)
    df = syn_df.copy()

    # Strategy: For each target, compute how many rows needed per class.
    # We build a pool by upsampling minority classes and then sample target_n rows.

    for t in TARGETS:
        levels = TARGET_LEVELS[t]
        n_per_class = target_n // len(levels)
        remainder   = target_n - n_per_class * len(levels)

        parts = []
        for i, lvl in enumerate(levels):
            subset = df[df[t] == lvl]
            n_need = n_per_class + (1 if i < remainder else 0)

            if len(subset) == 0:
                # Fall back to real data
                subset = real_df[real_df[t] == lvl]

            if len(subset) == 0:
                logger.warning(f"No rows for {t}={lvl}, skipping.")
                continue

            if len(subset) >= n_need:
                sampled = subset.sample(n=n_need, replace=False, random_state=seed + i)
            else:
                sampled = subset.sample(n=n_need, replace=True,  random_state=seed + i)

            parts.append(sampled)

        df = pd.concat(parts, ignore_index=True)
        df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
        logger.info(f"After balancing {t}: {df[t].value_counts().to_dict()}")

    # Final sample to exactly target_n
    if len(df) > target_n:
        df = df.sample(n=target_n, random_state=seed).reset_index(drop=True)
    elif len(df) < target_n:
        df = df.sample(n=target_n, replace=True, random_state=seed).reset_index(drop=True)

    return df


def report_class_balance(df, label=""):
    for t in TARGETS:
        counts = df[t].value_counts().sort_index()
        pcts   = (counts / len(df) * 100).round(1)
        parts  = ", ".join(f"{k}: {v} ({pcts[k]}%)" for k, v in counts.items())
        logger.info(f"  {label} {t}: {parts}")


def main():
    logger.info("Loading datasets...")
    real_df = pd.read_csv(REAL_PATH)
    syn_df  = pd.read_csv(SYN_PATH)

    logger.info(f"Input: {len(syn_df)} rows, {syn_df.shape[1]} cols")
    logger.info("Before balancing:")
    report_class_balance(syn_df, "SYN")

    # Balance
    balanced_df = balance_sequentially(syn_df, real_df, target_n=TARGET_N, seed=SEED)

    # Add diversity noise
    balanced_df = add_noise(balanced_df, real_df, noise_factor=0.008, seed=SEED)

    # Final column order must match real data
    balanced_df = balanced_df[real_df.columns]

    logger.info(f"\nAfter balancing ({len(balanced_df)} rows):")
    report_class_balance(balanced_df, "BALANCED")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    balanced_df.to_csv(OUT_PATH, index=False)
    logger.info(f"\nSaved: {OUT_PATH}")
    logger.info(f"Shape: {balanced_df.shape}")

    # Verify
    df_check = pd.read_csv(OUT_PATH)
    assert df_check.shape == (TARGET_N, 22), f"Shape mismatch: {df_check.shape}"
    assert df_check.isnull().sum().sum() == 0, "Nulls found!"
    logger.info("Verification passed.")


if __name__ == "__main__":
    main()
