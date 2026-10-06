# Aerospace Synthetic Data — Implementation Plan
**Status:** Active | **Date:** 2026-03-18 | **Target:** Excellent KPIs for every model × every size

---

## CURRENT STATE (Audit)

### Existing Synthetic Datasets (`per_model_datasets/`)
| Model | KS Pass Rate | TSTR | Status |
|---|---|---|---|
| Copula | 0.85–0.92 | 0.32 | 🟡 Good KS, weak TSTR |
| TabuDiff | 0.46 | 0.35 | 🟡 Moderate |
| TabuDiffPremium | 0.00 | 0.38 | ❌ Mode collapse |
| CTGAN | 0.00 | 0.35 | ❌ Mode collapse |
| CTGANPremium | 0.00 | 0.35 | ❌ Mode collapse |
| TVAE | 0.00 | 0.25 | ❌ Posterior collapse |
| DP-TVAE | 0.00 | 0.16 | ❌ DP + collapse |
| MaskedPredictor | 0.077 | 0.38 | ❌ Near failure |
| Empirical | 1.00 | 0.75–0.96 | ✅ (trivial resampling) |

**Root Cause:** 6/9 models collapse on 300-row physics-constrained data.
- CTGAN/TVAEPremium: mode collapse (GAN generates constant values)
- TVAE: posterior collapse (VAE encodes to mean only)
- Physics-constrained data has tight correlations (Material→E, ρ, Tensile) that resists neural generation

**Solution:** SDV library uses BGM (Bayesian Gaussian Mixture) per-column normalization — detects material modes, normalizes each separately → prevents collapse.

---

## IMPLEMENTATION PHASES

### PHASE 1: Generate High-Quality Synthetic Data [CRITICAL]
**Goal:** All models achieve KS ≥ 0.70, TSTR ≥ 0.65

**Step 1.1: Run SDV CTGAN (replace Genuity CTGAN failures)**
- SDV CTGANSynthesizer with BGM transformer
- Sizes: 300, 600, 1000
- Expected KS: 0.75–0.85

**Step 1.2: Run SDV TVAE (replace Genuity TVAE failures)**
- SDV TVAESynthesizer
- Sizes: 300, 600, 1000
- Expected KS: 0.75–0.85

**Step 1.3: Fix Genuity TabuDiff (use correct workflow)**
- Per docs: pass `preprocessed["preprocessed"].values` numpy
- Increase timesteps: try 100, 200
- Expected KS: 0.60–0.80

**Step 1.4: Fix Genuity MaskedPredictor (use correct workflow)**
- Per docs: pass `preprocessed["preprocessed"]` DataFrame (not numpy)
- Expected KS: 0.50–0.70

**Step 1.5: Fix DP-TVAE**
- Apply DP FIRST to raw DataFrame, THEN fit TVAE
- Use SDV TVAE as base if Genuity fails

**Step 1.6: Optimize Copula TSTR**
- Copula already has excellent KS (0.92)
- Issue: TSTR=0.32 is weak — conditional sampling or post-processing

**Script:** `run_all_models_excellence.py` (CREATED — needs to run)

---

### PHASE 2: Evaluate All Datasets [HIGH PRIORITY]
**Goal:** Compute comprehensive metrics for every model × size

**Metrics per dataset:**
- KS pass rate (% features passing KS test at α=0.05)
- Mean KL divergence
- TSTR F1 (macro-avg, Random Forest)
- TRTS F1 (reverse)
- Correlation matrix Frobenius distance
- MMD (Maximum Mean Discrepancy)
- Discriminator AUC (privacy)
- Composite score (weighted)

**Script:** `full_validation_pipeline.py` (EXISTS — update with new datasets)

---

### PHASE 3: Reports [HIGH PRIORITY]
**Goal:** Professional reports leveraging pre-existing gold from `d:\aero\`

**3.1 data_analysis_report.md** — 40-50 page EDA (AGENT RUNNING)
- 12 chapters covering real + synthetic data analysis
- References 202 PNG plots already copied to `reports/plots/`

**3.2 explainability_report.md** — Per-model deep dives (AGENT RUNNING)
- Uses `d:\aero\explainability\20260315_100903\` content (316 files!)
- Per-model strengths/weaknesses
- Statistical significance tests (bootstrap n=10000)
- Edge case robustness

**3.3 hyperparameter_optimization_report.md** — Optuna HPO results (AGENT RUNNING)
- CTGAN (3 trials), TabuDiff (3 trials), Copula (6 trials)
- Finding: smaller architecture wins on small datasets

**3.4 model_comparison_report.md** — Update with new SDV results
- Add SDV CTGAN vs Genuity CTGAN comparison
- Full leaderboard with 27+ configurations

**3.5 winner_declaration.md** — Update with best generative model
- Winner among generative models (not Empirical)
- Best per category: best KS, best TSTR, best balanced

**3.6 genuity_technical_paper.md** — Academic paper (PREV AGENT)
- Extended with premium model results

---

### PHASE 4: Final Datasets [MEDIUM]
**Goal:** 3 deliverable-quality datasets

**4.1** `synthetic_data/synthetic_aerospace_data.csv`
- Best generative model result at size=1000
- Target: composite > 0.75

**4.2** `synthetic_data/balanced_1000.csv` (EXISTS)
- Class-balanced across 4 targets

**4.3** `synthetic_data/best_empirical_5000.csv` (COPIED)
- Gold standard 5000-row dataset (composite=0.9969)

---

### PHASE 5: Ancillary [MEDIUM]
**5.1** Update `experiments/all_experiments.csv` with SDV results
**5.2** Update `README.md` to reflect new structure
**5.3** Create `feature_engineering/feature_engineering.py` standalone script
**5.4** Conditional probability validation (10 domain rules)

---

## EXECUTION ORDER (RIGHT NOW)

1. ✅ **SDV installed** (v1.34.3)
2. ✅ `run_all_models_excellence.py` created — NEEDS TO RUN
3. 🔄 Background agents running: explainability_report, HPO_report, data_analysis_report
4. **NEXT: Run excellence generation** → get good KPIs
5. **THEN: Run full validation** on all new datasets
6. **THEN: Update reports** with new results

---

## KEY FILES REFERENCE

| File | Purpose | Status |
|---|---|---|
| `run_all_models_excellence.py` | Generate all models with correct workflows + SDV fallback | READY |
| `full_validation_pipeline.py` | Tier 1+2 validation on all datasets | EXISTS |
| `reports/explainability_report.md` | Per-model explainability (316 source files) | GENERATING |
| `reports/hyperparameter_optimization_report.md` | Optuna HPO results | GENERATING |
| `reports/data_analysis_report.md` | 40-50 page EDA | GENERATING |
| `experiments/all_metrics_72runs.csv` | 72-run prior experiment baseline | COPIED |
| `synthetic_data/best_synthetic_empirical_seed11_n5000.csv` | 5000-row gold dataset | COPIED |

---

## EXPECTED FINAL KPIs (Targets)

| Model | Size | Target KS | Target TSTR | Target Composite |
|---|---|---|---|---|
| SDV CTGAN | 300/600/1000 | ≥ 0.75 | ≥ 0.65 | ≥ 0.72 |
| SDV TVAE | 300/600/1000 | ≥ 0.75 | ≥ 0.65 | ≥ 0.72 |
| Copula | 300/600/1000 | ≥ 0.85 | ≥ 0.55 | ≥ 0.75 |
| TabuDiff | 300/600/1000 | ≥ 0.60 | ≥ 0.50 | ≥ 0.65 |
| MaskedPredictor | 300/600/1000 | ≥ 0.50 | ≥ 0.45 | ≥ 0.55 |
| DP-TVAE | 1000 | ≥ 0.60 | ≥ 0.45 | ≥ 0.60 |
| Empirical (baseline) | 300/600/1000 | 1.00 | 0.75–0.96 | 0.93–0.99 |

---

## PRE-EXISTING GOLD ASSETS (from `d:\aero\`)

| Asset | Location | How to Use |
|---|---|---|
| 72-run metrics | `experiments/all_metrics_72runs.csv` | Baseline for leaderboard |
| 5000-row gold dataset | `synthetic_data/best_synthetic_empirical_seed11_n5000.csv` | Best deliverable |
| 44 model comparison graphs | `reports/plots/model_comparison/`, `scale_analysis/`, `summary/` | Reference in reports |
| 78 explainability graphs | `reports/plots/explainability/` | Per-model analysis |
| 31 statistical graphs | `reports/plots/statistical/` | Distribution overlays |
| HTML executive report | `reports/executive_report.html` | Client-facing deliverable |
| HTML benchmarking report | `reports/benchmarking_report.html` | Technical benchmark |
| PDF full report | `reports/full_report.pdf` | Print deliverable |
| Jupyter notebook | `notebooks/aerospace_synthesis_analysis.ipynb` | Reproducibility |
| Optuna HPO data | `experiments/optuna/` (51 files) | HPO report source |

---

*Plan created: 2026-03-18 | All execution steps are ordered by dependency*
