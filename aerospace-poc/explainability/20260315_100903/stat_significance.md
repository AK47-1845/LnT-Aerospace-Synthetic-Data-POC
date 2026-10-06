# Statistical Significance Testing

**Comparison:** Best Genuity Model (`TabuDiff`) vs Best Baseline (`KDE`).
Using paired bootstrap with 10,000 resamples on run-level metrics (Composite Score).

**Results:**
- Mean Delta (Genuity - Baseline): -0.1685
- 95% CI for Delta: [-0.1783, -0.1566]
- p-value (H0: Delta <= 0): 1.0000
- Effect Size (Cohen's d): -8.3411

**Interpretation:**
The difference is not statistically significant at alpha=0.05, meaning the Genuity model matches the baseline.

**Code to reproduce:**
```python
import numpy as np
import pandas as pd

df = pd.read_csv("metrics_raw.csv")
df_gen = df[df['Model'] == 'TabuDiff'].set_index(['Size', 'Seed'])['composite_score']
df_base = df[df['Model'] == 'KDE'].set_index(['Size', 'Seed'])['composite_score']
common = df_gen.index.intersection(df_base.index)
deltas = df_gen.loc[common].values - df_base.loc[common].values

np.random.seed(42)
boot_deltas = [np.mean(np.random.choice(deltas, size=len(deltas), replace=True)) for _ in range(10000)]
ci_lower, ci_upper = np.percentile(boot_deltas, [2.5, 97.5])
p_val = np.sum(np.array(boot_deltas) <= 0) / 10000.0
cohens_d = np.mean(deltas) / np.std(deltas, ddof=1)
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}], p={p_val:.4f}, d={cohens_d:.4f}")
```
