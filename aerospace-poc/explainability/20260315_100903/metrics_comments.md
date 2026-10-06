# Metrics Definitions & Commentary

| Metric | Definition | Practical Implication | Top Model Mean | Best Run | Trend |
|---|---|---|---|---|---|
| `composite_score` | Weighted aggregated score of all components | Used to select the absolute best model | ~0.95 | High is better | Excellent |
| `physics_consistency` | Examines if variables remain within aerospace bounds | Prevents generating physically impossible aircraft | ~0.99 | High is better | Essential |
| `statistical_similarity` | Average distribution overlap between real/synth | Models must match real continuous densities | ~0.95 | High is better | Sensitive to sample size |
| `privacy_detectability` | AUC of adversary guessing real vs synth | Prevents data leakage and memorization | ~0.95 | High/0.5 is better | Important for compliance |

### Commentary
The metrics explicitly balance the generative fidelity against the structural limits required by aerospace physics constraints. 

```python
import pandas as pd
df = pd.read_csv("metrics_raw.csv")
print(df.describe())
```
