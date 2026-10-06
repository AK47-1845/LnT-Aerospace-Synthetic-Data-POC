# Profile: Copula

## Summary of Strengths and Weaknesses
- **Capability:** Copula provides robust generative mechanics suitable for continuous tabular data.
- **Strengths:** Look at the composite score tracking. Provides good baseline performance.
- **Weaknesses:** May occasionally drift near complex boundary edges (check `repair_count`).

**Suitability Statement:** Best utilized when structural variance needs to be simulated without breaking strict tabular paradigms.

## Recommended Hyperparameters (Best Run)
{'physics_consistency': 0.9927070293028892, 'mean_ks_pval': 0.8796045814449814, 'mean_kl_div': 0.0182355720734719, 'statistical_similarity': 0.981764427926528, 'ml_utility': 0.3733333333333333, 'privacy_detectability': 0.981764427926528, 'correlation_preservation': 0.9756900976762972, 'composite_score': 0.830934025015967, 'repair_count': 0, 'Model': 'Copula', 'Seed': 11, 'Size': 5000}

## Sample Provenance (Best run dataset)
- Provenance points to: `synthetic_Copula_..._best_provenance.json`

## Reproducibility Snippet
```python
import pandas as pd
df = pd.read_csv("d:/aero/artifacts/experiments/20260315_100903/synth_datasets/...")
# compute physical score...
```
