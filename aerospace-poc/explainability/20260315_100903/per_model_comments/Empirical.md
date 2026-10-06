# Profile: Empirical

## Summary of Strengths and Weaknesses
- **Capability:** Empirical provides robust generative mechanics suitable for continuous tabular data.
- **Strengths:** Look at the composite score tracking. Provides good baseline performance.
- **Weaknesses:** May occasionally drift near complex boundary edges (check `repair_count`).

**Suitability Statement:** Best utilized when structural variance needs to be simulated without breaking strict tabular paradigms.

## Recommended Hyperparameters (Best Run)
{'physics_consistency': 0.9967142158145416, 'mean_ks_pval': 0.9999298922675424, 'mean_kl_div': 0.0020842814870237, 'statistical_similarity': 0.9979157185129762, 'ml_utility': 1.0, 'privacy_detectability': 0.9979157185129762, 'correlation_preservation': 0.9890473860484726, 'composite_score': 0.9968662384753696, 'repair_count': 0, 'Model': 'Empirical', 'Seed': 11, 'Size': 5000}

## Sample Provenance (Best run dataset)
- Provenance points to: `synthetic_Empirical_..._best_provenance.json`

## Reproducibility Snippet
```python
import pandas as pd
df = pd.read_csv("d:/aero/artifacts/experiments/20260315_100903/synth_datasets/...")
# compute physical score...
```
