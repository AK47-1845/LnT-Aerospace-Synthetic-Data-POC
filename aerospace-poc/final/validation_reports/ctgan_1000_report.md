# Validation Report: ctgan_1000.csv

## Tier 1: Minimum Bar
- **Schema Match:** ✅ Pass
- **Null Check:** ✅ Pass
- **Numeric Range Check:** ✅ Pass
- **Categorical Level Check:** ✅ Pass
- **Row Count:** ✅ Pass (1000 rows)

## Tier 2: Academic Validations
### 1. ML Utility (Train-on-Synthetic, Test-on-Real)
- **Vibration Damping:** 0.3500 accuracy
- **Computational Time:** 0.3167 accuracy
- **Weight Efficiency:** 0.3467 accuracy
- **Durability:** 0.3367 accuracy

### 2. Feature Importance Alignment
Measures if the generative model learned the same physical rules governing the targets.
- **Vibration Damping MAE:** 0.0169
- **Computational Time MAE:** 0.0249
- **Weight Efficiency MAE:** 0.0238
- **Durability MAE:** 0.0265

### 3. Statistical Fidelity (KS & KL)
- **Mean KS p-value:** 0.0000 (Higher is better, >0.05 fails to reject null hypothesis)

### 4. Rare Case Realism (Isolation Forest)
- **Synthetic Anomaly Rate:** 0.00% (Expected ~5%)