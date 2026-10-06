# Profile: KDE

## Summary of Strengths and Weaknesses
- **Capability:** KDE provides robust generative mechanics suitable for continuous tabular data.
- **Strengths:** Look at the composite score tracking. Provides good baseline performance.
- **Weaknesses:** May occasionally drift near complex boundary edges (check `repair_count`).

**Suitability Statement:** Best utilized when structural variance needs to be simulated without breaking strict tabular paradigms.

## Recommended Hyperparameters (Best Run)
{'physics_consistency': 0.9973210802948254, 'mean_ks_pval': 0.9974648488546416, 'mean_kl_div': 0.0040074815317019, 'statistical_similarity': 0.995992518468298, 'ml_utility': 1.0, 'privacy_detectability': 0.995992518468298, 'correlation_preservation': 0.9910702676494182, 'composite_score': 0.9965217635936972, 'repair_count': 0, 'Model': 'KDE', 'Seed': 123, 'Size': 5000}

## Sample Provenance (Best run dataset)
- Provenance points to: `synthetic_KDE_..._best_provenance.json`

## Reproducibility Snippet
```python
import pandas as pd
df = pd.read_csv("d:/aero/artifacts/experiments/20260315_100903/synth_datasets/...")
# compute physical score...
```
