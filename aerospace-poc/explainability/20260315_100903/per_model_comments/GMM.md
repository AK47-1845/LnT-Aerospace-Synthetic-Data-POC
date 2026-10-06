# Profile: GMM

## Summary of Strengths and Weaknesses
- **Capability:** GMM provides robust generative mechanics suitable for continuous tabular data.
- **Strengths:** Look at the composite score tracking. Provides good baseline performance.
- **Weaknesses:** May occasionally drift near complex boundary edges (check `repair_count`).

**Suitability Statement:** Best utilized when structural variance needs to be simulated without breaking strict tabular paradigms.

## Recommended Hyperparameters (Best Run)
{'physics_consistency': 0.9939569879346426, 'mean_ks_pval': 0.9660375129490916, 'mean_kl_div': 0.0078520521509773, 'statistical_similarity': 0.9921479478490228, 'ml_utility': 0.4433333333333333, 'privacy_detectability': 0.9921479478490228, 'correlation_preservation': 0.9798566264488086, 'composite_score': 0.8534624040271922, 'repair_count': 0, 'Model': 'GMM', 'Seed': 42, 'Size': 5000}

## Sample Provenance (Best run dataset)
- Provenance points to: `synthetic_GMM_..._best_provenance.json`

## Reproducibility Snippet
```python
import pandas as pd
df = pd.read_csv("d:/aero/artifacts/experiments/20260315_100903/synth_datasets/...")
# compute physical score...
```
