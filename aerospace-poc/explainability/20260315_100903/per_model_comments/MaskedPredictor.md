# Profile: MaskedPredictor

## Summary of Strengths and Weaknesses
- **Capability:** MaskedPredictor provides robust generative mechanics suitable for continuous tabular data.
- **Strengths:** Look at the composite score tracking. Provides good baseline performance.
- **Weaknesses:** May occasionally drift near complex boundary edges (check `repair_count`).

**Suitability Statement:** Best utilized when structural variance needs to be simulated without breaking strict tabular paradigms.

## Recommended Hyperparameters (Best Run)
{'physics_consistency': 0.9592035754257912, 'mean_ks_pval': 0.0182252619095362, 'mean_kl_div': 2.6108483105230644, 'statistical_similarity': 0.0, 'ml_utility': 0.4733333333333333, 'privacy_detectability': 0.0, 'correlation_preservation': 0.8640119180859713, 'composite_score': 0.4397758361313872, 'repair_count': 0, 'Model': 'MaskedPredictor', 'Seed': 11, 'Size': 300}

## Sample Provenance (Best run dataset)
- Provenance points to: `synthetic_MaskedPredictor_..._best_provenance.json`

## Reproducibility Snippet
```python
import pandas as pd
df = pd.read_csv("d:/aero/artifacts/experiments/20260315_100903/synth_datasets/...")
# compute physical score...
```
