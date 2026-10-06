# Validation Report: tabudiff_1000.csv

## Tier 1: Minimum Bar
- **Schema Match:** ✅ Pass
- **Null Check:** ✅ Pass
- **Numeric Range Check:** ❌ Fail
  - ν (Expected 0.30 to 0.35, got 0.30 to 0.35)
- **Categorical Level Check:** ✅ Pass
- **Row Count:** ✅ Pass (1000 rows)

## Tier 2: Academic Validations
### 1. ML Utility (Train-on-Synthetic, Test-on-Real)
- **Vibration Damping:** 0.3767 accuracy
- **Computational Time:** 0.4200 accuracy
- **Weight Efficiency:** 0.3433 accuracy
- **Durability:** 0.3767 accuracy

### 2. Feature Importance Alignment
Measures if the generative model learned the same physical rules governing the targets.
- **Vibration Damping MAE:** 0.0043
- **Computational Time MAE:** 0.0065
- **Weight Efficiency MAE:** 0.0075
- **Durability MAE:** 0.0047

### 3. Statistical Fidelity (KS & KL)
- **Mean KS p-value:** 0.2542 (Higher is better, >0.05 fails to reject null hypothesis)

### 4. Rare Case Realism (Isolation Forest)
- **Synthetic Anomaly Rate:** 7.70% (Expected ~5%)
- **Mean distance to real anomalies:** 5601.7234