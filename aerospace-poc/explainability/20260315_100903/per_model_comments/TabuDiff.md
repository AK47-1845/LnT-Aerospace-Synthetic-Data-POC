# Profile: TabuDiff

## Summary of Strengths and Weaknesses
- **Capability:** TabuDiff provides robust generative mechanics suitable for continuous tabular data.
- **Strengths:** Look at the composite score tracking. Provides good baseline performance.
- **Weaknesses:** May occasionally drift near complex boundary edges (check `repair_count`).

**Suitability Statement:** Best utilized when structural variance needs to be simulated without breaking strict tabular paradigms.

## Recommended Hyperparameters (Best Run)
{'physics_consistency': 0.9836161186660548, 'mean_ks_pval': 0.2180141477885967, 'mean_kl_div': 0.0615079812847204, 'statistical_similarity': 0.9384920187152797, 'ml_utility': 0.4366666666666666, 'privacy_detectability': 0.9384920187152797, 'correlation_preservation': 0.9453870622201828, 'composite_score': 0.8230947572190168, 'repair_count': 0, 'Model': 'TabuDiff', 'Seed': 11, 'Size': 5000}

## Sample Provenance (Best run dataset)
- Provenance points to: `synthetic_TabuDiff_..._best_provenance.json`

## Reproducibility Snippet
```python
import pandas as pd
df = pd.read_csv("d:/aero/artifacts/experiments/20260315_100903/synth_datasets/...")
# compute physical score...
```
