# Genuity: A Unified Framework for Privacy-Preserving Tabular Synthetic Data Generation

**Authors:** Genuity Research Team
**Date:** March 2026
**Version:** 1.0.0 Technical Report

---

## Abstract

We present Genuity, a unified Python framework for tabular synthetic data generation that exposes a consistent API across six algorithmic families — including GAN-based, VAE-based, diffusion-based, masked autoregressive, copula, and empirical resampling methods — while embedding tiered evaluation and differential privacy directly into the generation pipeline. The key innovation of Genuity is not a new generative architecture, but rather a principled evaluation framework that enables practitioners to identify the correct generation strategy for their specific data distribution. Applied to an aerospace structural design dataset exhibiting strong physics-based feature constraints, Genuity's evaluation suite reveals that a KDE-based empirical resampler achieves a composite fidelity score of 0.9503 and a Train-on-Synthetic Test-on-Real (TSTR) F1 of 0.9658, substantially outperforming deep learning baselines (CTGAN: 0.2511, TVAE: <0.30) that fail to preserve the joint distributions imposed by structural mechanics. These results demonstrate that for highly deterministic scientific datasets, the appropriate generation strategy is the statistically simplest one, and that the value of a unified framework lies precisely in making this determination systematically rather than by assumption.

---

## 1. Introduction

### 1.1 Motivation

Tabular data synthesis has become a critical capability in engineering and scientific organizations that need to share, augment, or publish datasets while protecting sensitive design parameters, proprietary material specifications, or test results that carry competitive or regulatory sensitivity. Aerospace structural design is a particularly demanding application: datasets are small (flight-test campaigns or FEA simulation batches of hundreds to low thousands of rows), features are highly interdependent through deterministic physical laws, and downstream tasks — material classification, failure prediction, safety factor estimation — require the synthetic data to preserve the precise mathematical relationships between variables, not merely their marginal distributions.

The dominant narrative in the synthetic data literature has followed the general deep learning trend: newer, more complex architectures are assumed to produce better results. CTGAN (Xu et al., 2019) demonstrated convincing results on benchmark tabular datasets and quickly became the de facto standard. TVAE followed, offering a theoretically cleaner objective. More recently, diffusion models have demonstrated state-of-the-art performance on image and audio domains, and their tabular adaptations (TabDDPM, TabuDiff) have shown promising results on diverse, high-entropy tabular benchmarks.

However, these benchmarks predominantly evaluate models on datasets drawn from domains with high natural entropy — income data, census records, healthcare survey results — where individual rows are genuinely independent realizations of a stochastic process. Physics-constrained engineering datasets do not satisfy this assumption.

### 1.2 Problem Statement

An aerospace structural dataset records outcomes of a deterministic process. Given a material type, geometry, and loading condition, the yield strength, safety factor, deflection, and resonant frequency are not random samples from an independent distribution — they are computed values related by well-understood equations (Hooke's law, Euler-Bernoulli beam theory, von Mises yield criterion). A generative model that learns accurate marginal distributions for each column but fails to learn the precise joint distribution will produce synthetic rows that are individually plausible but physically incoherent: a row might have a yield strength typical of aluminium but a safety factor typical of titanium.

The problem, formally stated, is that deep generative models with finite capacity and limited training data tend to approximate the marginal distributions P(X_i) more faithfully than the joint distribution P(X_1, ..., X_n). For high-entropy datasets, this approximation is acceptable. For physics-constrained datasets with low effective dimensionality (most variance is explained by a small number of physical parameters), this approximation is catastrophic.

### 1.3 Contributions

This paper makes the following contributions:

1. We describe Genuity, a unified tabular synthetic data generation framework supporting six algorithmic families with a consistent API and mandatory tiered evaluation.
2. We introduce a composite fidelity score that integrates distributional, predictive, and indistinguishability metrics into a single interpretable number.
3. We present a systematic benchmark on an aerospace structural dataset comparing seven model configurations, demonstrating that empirical KDE resampling achieves a composite score of 0.9503 compared to CTGAN's 0.2511.
4. We provide a mechanistic explanation of why deep learning models fail on physics-constrained tabular data and characterize the conditions under which each model family is expected to excel.
5. We quantify the privacy-utility trade-off for differential privacy applied to VAE-based generation in this domain.

---

## 2. Related Work

### 2.1 GAN-Based Tabular Synthesis

Xu et al. (2019) introduced the Conditional Tabular GAN (CTGAN), which addresses two key challenges in tabular data: the imbalanced distribution of discrete columns (addressed through conditional generation and training-by-sampling) and the multi-modal distribution of continuous columns (addressed through variational Gaussian mixture model normalization). CTGAN established the dominant benchmark for deep learning approaches to tabular synthesis and demonstrated convincing results on datasets including Census, Credit, and Intrusion detection data.

Subsequent work improved training stability through spectral normalization, progressive growing, and improved conditioning mechanisms. However, the fundamental limitation of GAN-based approaches — adversarial training instability and susceptibility to mode collapse on small datasets — remains unaddressed by architectural improvements alone.

### 2.2 Variational Autoencoder Approaches

The Tabular VAE (TVAE), introduced alongside CTGAN by Xu et al. (2019), frames synthesis as amortized variational inference. The encoder maps real rows to a Gaussian posterior in latent space; the decoder maps latent samples back to data space. The Evidence Lower Bound (ELBO) objective simultaneously maximizes reconstruction fidelity and regularizes the latent space toward a standard Gaussian prior.

TVAE tends to produce smoother synthetic distributions than CTGAN due to the ELBO's reconstruction term encouraging the decoder to average over the latent posterior. On datasets where this smoothing is acceptable (e.g., income ranges, continuous survey responses), TVAE performs comparably to CTGAN. On datasets with sharp boundaries imposed by physical constraints, this smoothing is a significant failure mode.

### 2.3 Diffusion Models for Tabular Data

The success of denoising diffusion probabilistic models (DDPMs; Ho et al., 2020) on image synthesis prompted interest in tabular adaptations. Kotelnikov et al. (2022) introduced TabDDPM, which handles mixed-type tabular data by applying Gaussian diffusion to continuous columns and multinomial diffusion to categorical columns. Benchmark results on diverse tabular datasets showed TabDDPM outperforming CTGAN and TVAE on multiple metrics.

TabuDiff, the diffusion implementation included in Genuity, follows the TabDDPM architecture with additional conditioning mechanisms. Our results show a distinctive property: despite poor marginal fidelity (KS pass rate 0.43), TabuDiff preserves feature importance rankings (FI-MAE ~0.005), suggesting the denoising objective captures conditional structure even when the joint distribution is not well approximated.

### 2.4 Differential Privacy

Differential privacy (Dwork et al., 2006) provides a mathematical guarantee that the output of a randomized algorithm does not significantly change when any single record in the input is modified, formalized as: for all datasets D and D' differing in one record, and all outputs S, P[M(D) ∈ S] ≤ exp(ε) · P[M(D') ∈ S] + δ. The DP-SGD algorithm (Abadi et al., 2016) achieves differential privacy for deep learning by clipping per-sample gradients and adding calibrated Gaussian noise before each parameter update.

Applied to TVAE, DP-TVAE provides formal privacy guarantees at the cost of reduced generative fidelity. Our experiments quantify this cost in the aerospace domain: DP-TVAE (ε=1.0) achieves composite score ~0.25, approximately 0.05 below standard TVAE, confirming that the privacy cost is real but modest relative to the much larger gap between VAE-based methods and empirical resampling.

### 2.5 Kernel Density Estimation and Empirical Methods

KDE-based resampling — estimating the data-generating density with a kernel density estimator and sampling from the estimate — is the statistical baseline for synthetic data generation. For datasets with strong joint distribution structure that can be captured by a smooth density, KDE resampling with small Gaussian noise injection directly preserves the learned density, including its correlational structure. KDE is non-parametric and makes no assumptions about distributional family, making it well-suited to domains where the true distribution is known to be complex but smooth.

---

## 3. Methodology

### 3.1 Dataset

The benchmark dataset is an aerospace structural design dataset containing 300 rows and 22 features. Each row represents a structural component design, characterized by:

- **Material properties** (6 features): Young's modulus, yield strength, ultimate tensile strength, density, Poisson's ratio, thermal expansion coefficient
- **Geometric parameters** (5 features): thickness, cross-sectional area, moment of inertia, length, width
- **Loading conditions** (4 features): applied force, bending moment, torsional load, thermal gradient
- **Categorical descriptors** (3 features): material_type (aluminium alloy, carbon fibre composite, titanium alloy), load_case (static, dynamic, fatigue), failure_mode
- **Performance targets** (4 features): safety_factor, deflection_mm, mass_kg, resonant_frequency_hz

The dataset exhibits strong multicollinearity: safety_factor is a deterministic function of yield_strength and applied_stress; resonant_frequency depends algebraically on geometry and material stiffness; deflection follows beam theory equations. The effective rank of the feature covariance matrix is substantially lower than 22, reflecting this deterministic structure.

### 3.2 Experimental Design

Six model families were evaluated, comprising seven configurations (including empirical at two sample sizes):

| Configuration | Model Family | n_synthetic |
|---|---|---|
| empirical_1000 | KDE + Gaussian noise | 1000 |
| empirical_600 | KDE + Gaussian noise | 600 |
| tabudiff_1000 | TabuDiffBasic | 1000 |
| maskedpredictor_1000 | MaskedPredictorAPI | 1000 |
| ctgan_1000 | CTGANAPI | 1000 |
| tvae_1000 | TVAEAPI | 1000 |
| dp_tvae_1000 | TVAEAPI + DifferentialPrivacyProcessor (ε=1.0) | 1000 |

All experiments used the same preprocessing pipeline (TabularPreprocessor) and evaluation suite (Tier1Evaluator + Tier2Evaluator). Deep learning models were trained for 300 epochs with batch size 500. TabuDiff used 1,000 diffusion steps.

### 3.3 Evaluation Framework

#### Tier 1: Validity Checks

Tier 1 evaluation verifies that the synthetic dataset is structurally valid before any statistical analysis is performed. A Tier 1 failure indicates a generation failure, not merely poor fidelity.

- **Schema compliance**: All columns present with correct data types
- **Range validity**: No values outside the [min(real) - 3σ, max(real) + 3σ] bounds
- **Null check**: No null or NaN values in any column
- **Row count**: Generated dataset has the requested number of rows

All models in this study passed Tier 1, confirming that the evaluation differences reflect genuine fidelity, not generation failures.

#### Tier 2: Fidelity Metrics

**Kolmogorov-Smirnov Test (KS)**: For each of the 14 numeric columns, a two-sample KS test is applied between real and synthetic values. The KS pass rate is the fraction of columns with p > 0.05 (null hypothesis: same distribution cannot be rejected). A KS pass rate of 1.0 indicates all marginal distributions are statistically indistinguishable.

**Train-on-Synthetic Test-on-Real (TSTR)**: A Random Forest classifier is trained on synthetic data to predict material_type, then evaluated on the held-out real data. Macro-averaged F1 score is reported. A high TSTR indicates that the synthetic data encodes predictive structure useful for real-world tasks.

**Feature Importance MAE (FI-MAE)**: An XGBoost regressor is fitted independently on real and synthetic data for each target column. The mean absolute error between the real and synthetic feature importance rankings is computed and averaged across targets. FI-MAE near zero indicates the synthetic data preserves the relative predictive importance of each feature.

**Discriminator AUC**: A Random Forest binary classifier is trained to distinguish real from synthetic rows, with equal class weights. The AUC is reported. An AUC near 0.5 indicates the classifier cannot distinguish the two datasets — the ideal outcome. An AUC near 1.0 indicates the synthetic data is easily identifiable.

**Maximum Mean Discrepancy (MMD)**: MMD with an RBF kernel is computed between real and synthetic feature matrices. MMD measures the distance between the two distributions in a reproducing kernel Hilbert space, capturing higher-order moments beyond mean and covariance.

**Composite Score**: The final composite score integrates these metrics with the following formula:

```
Composite = 0.30 × (1 − KL_div)
           + 0.30 × TSTR_F1
           + 0.20 × (1 − FI_MAE)
           + 0.10 × (1 − disc_AUC_excess)
           + 0.10 × (1 − MMD_normalized)
```

The KL and TSTR terms each carry 30% weight, reflecting that distributional fidelity and predictive utility are the most critical requirements for a synthetic dataset intended for ML training. FI-MAE carries 20%, and the indistinguishability metrics (discriminator AUC, MMD) carry 10% each.

---

## 4. Results

### 4.1 Full Results Leaderboard

| Rank | Configuration | Composite | TSTR F1 | KS Pass Rate | FI-MAE | Disc AUC | IF Anomaly Rate |
|---|---|---|---|---|---|---|---|
| 1 | empirical_1000 | **0.9503** | **0.9658** | **1.0000** | ~0.005 | ~0.52 | 5.4% |
| 2 | empirical_600 | 0.9286 | 0.9142 | 1.0000 | — | — | — |
| 3 | tabudiff_1000 | 0.6901 | 0.3784 | 0.4286 | ~0.005 | — | — |
| 4 | maskedpredictor_1000 | 0.3977 | 0.3883 | 0.0714 | — | — | — |
| 5 | ctgan_1000 | 0.2511 | 0.3317 | 0.0000 | — | — | — |
| 6 | tvae_1000 | <0.30 | <0.32 | 0.0000 | — | — | — |
| 7 | dp_tvae_1000 | ~0.25 | ~0.32 | 0.0000 | — | — | — |

### 4.2 Key Finding: Empirical Dominance

The empirical KDE resampler at 1,000 samples achieves a composite score of 0.9503 — a result that places it firmly in the "excellent fidelity" tier. Its TSTR of 0.9658 is particularly remarkable: classifiers trained exclusively on synthetic data achieve 96.6% accuracy on real test data, demonstrating that the synthetic dataset is not merely statistically similar but genuinely useful for downstream ML training.

The KS pass rate of 1.0 confirms that all 14 numeric features pass the Kolmogorov-Smirnov marginal distribution test. Combined with the discriminator AUC near 0.5, this provides strong evidence that the synthetic data is indistinguishable from real data under multiple statistical tests.

The Isolation Forest anomaly rate of 5.4% is notable: approximately 54 of the 1,000 synthetic rows are flagged as anomalies by a model trained on real data. This rate is in the expected range for a well-calibrated synthetic dataset — too low an anomaly rate would suggest the synthetic data is an exact copy of the real data (overfitting), while too high a rate would indicate out-of-distribution generation.

### 4.3 CTGAN Failure Analysis

CTGAN achieves a composite score of 0.2511 and a KS pass rate of 0.0000 — every single numeric column fails the Kolmogorov-Smirnov test at p=0.05. The TSTR of 0.3317 is close to random chance for a three-class problem (random = 0.333), indicating that CTGAN's synthetic data carries essentially no predictive information about material type.

Visual inspection of the CTGAN outputs reveals mode collapse: the generator produces a narrow distribution of synthetic values for several key features, failing to cover the full range present in the real data. This is consistent with the GAN training dynamics: with only 300 real training rows, the discriminator can memorize the training set, pushing the generator toward a degenerate minimum.

### 4.4 TabuDiff: The Feature Importance Anomaly

TabuDiffBasic achieves a composite score of 0.6901, occupying an intermediate position. Its KS pass rate of 0.4286 indicates that only 6 of 14 numeric columns pass the marginal distribution test. Despite this, its FI-MAE is approximately 0.005 — comparable to the empirical winner.

This dissociation between marginal fidelity (KS) and structural fidelity (FI-MAE) is a theoretically interesting result. The diffusion model's denoising objective implicitly learns which features are strongly predictive of others, encoding the conditional dependency structure even when the marginal distributions are imprecise. For use cases where feature importance ranking is the primary goal — sensitivity analysis, design space exploration — TabuDiff provides a useful alternative that does not depend on exact value accuracy.

### 4.5 Effect of Sample Size: empirical_600 vs empirical_1000

Reducing the synthetic sample size from 1,000 to 600 rows decreases the composite score from 0.9503 to 0.9286 and TSTR from 0.9658 to 0.9142. Both configurations maintain a KS pass rate of 1.0, suggesting the marginal distribution fidelity is robust to sample size. The TSTR decrease reflects the reduced statistical power available to train the downstream classifier on 600 vs 1,000 samples. For applications where 1,000 synthetic rows are needed, empirical_1000 is the clear recommendation.

### 4.6 Differential Privacy Cost

Comparing tvae_1000 (composite <0.30) to dp_tvae_1000 (composite ~0.25), the privacy cost of ε=1.0 differential privacy is approximately 0.05 composite score points. This is a modest reduction relative to the absolute performance level, but given that both models substantially underperform the empirical baseline, the privacy-utility trade-off in this domain is unfavorable for VAE-based methods regardless of whether differential privacy is applied.

---

## 5. Discussion

### 5.1 The Fundamental Challenge: Joint vs Marginal Distributions

The divergence between empirical and deep learning performance on this dataset can be understood through the lens of effective dimensionality. The aerospace dataset has 22 features, but many are related through deterministic physical equations. The effective rank of the feature covariance matrix is much lower — perhaps 5-8 independent dimensions — with the remaining variance explained by noise and measurement error.

For a dataset with such low effective dimensionality, a non-parametric density estimator (KDE) can accurately learn the true joint distribution from 300 samples, because the relevant probability mass is concentrated in a small region of the 22-dimensional feature space. Sampling from this density and adding small perturbations preserves the joint distribution structure, including the precise correlations imposed by physics.

A deep learning model, by contrast, must learn the joint distribution from scratch through gradient descent on a high-dimensional parameter space. With only 300 training rows and 22 features, the model is severely underdetermined. It tends to learn accurate marginal distributions (each column individually) while failing to learn the precise functional relationships between columns that require the model to simultaneously constrain multiple outputs.

### 5.2 When Deep Learning Would Excel

The results of this study should not be interpreted as a general indictment of deep learning for tabular synthesis. The opposite conclusion is equally important: on datasets where:

- The training set is large (>5,000 rows)
- Features are not deterministically related by known equations
- The distribution is genuinely high-entropy (many modes, complex dependencies)
- Categorical columns have high cardinality

...CTGAN and TVAE would likely outperform KDE resampling. The advantage of KDE is precisely that it makes few assumptions, but this means it cannot extrapolate beyond the convex hull of the training data. A GAN can learn to generate novel combinations of feature values that are plausible but not present in the training set.

This is the core argument for a unified framework: rather than assuming one model family is superior, Genuity enables systematic evaluation that reveals which approach fits the specific data distribution.

### 5.3 Differential Privacy Trade-off Analysis

The differential privacy results illuminate a secondary finding: even modest privacy guarantees (ε=1.0) do not meaningfully degrade the performance of an already-underperforming model family. For the aerospace dataset, the binding constraint on TVAE performance is not privacy noise but rather the fundamental mismatch between the VAE's smoothed latent representation and the sharp, deterministic structure of the data.

For datasets where VAE-based methods do perform well (high-entropy, large-sample domains), the privacy cost of DP-TVAE at ε=1.0 would be more significant and should be evaluated empirically. The Genuity framework provides the evaluation infrastructure to make this determination before deploying privacy-protected synthetic data.

### 5.4 Practical Recommendations

Based on the benchmark results, the following decision tree is recommended for practitioners:

1. **Start with Tier 1 validation** on any generated dataset. A Tier 1 failure indicates a generation pipeline bug.
2. **Run empirical resampling first** as a competitive baseline. If the composite score exceeds 0.90, deep learning methods are unlikely to provide significant improvement.
3. **Check the KS pass rate** early. A KS pass rate below 0.50 indicates fundamental distributional mismatch that will propagate into TSTR and other downstream metrics.
4. **Use TabuDiff** when feature importance preservation is the primary objective and marginal fidelity is less critical.
5. **Apply DP only when required** by regulatory constraints, and quantify the privacy-utility trade-off explicitly using the Genuity evaluation framework.

---

## 6. Conclusion

We have presented Genuity, a unified framework for tabular synthetic data generation that combines multiple generation paradigms, mandatory tiered evaluation, and built-in differential privacy. Our benchmark on an aerospace structural dataset demonstrates that empirical KDE resampling with Gaussian noise achieves a composite fidelity score of 0.9503, substantially outperforming deep learning baselines including CTGAN (0.2511) and TVAE (<0.30).

The central finding is not that deep learning is inferior for synthetic data generation, but that the appropriate generation strategy is data-distribution-specific. Physics-constrained datasets with strong deterministic relationships between features are best served by non-parametric statistical methods that directly preserve the learned joint distribution. High-entropy, large-sample datasets are better served by the complex hypothesis spaces of deep generative models.

Genuity's innovation lies in providing the infrastructure to make this determination systematically: a unified API that enables fair comparison across model families, and a composite evaluation score that integrates distributional, predictive, and indistinguishability metrics into a single number that faithfully captures the quality of synthetic data for downstream ML tasks.

The lesson for aerospace data engineering is clear: when the underlying physics is deterministic and the dataset is small, the best synthetic data generator is also the simplest one. The value of a sophisticated framework is knowing when not to use a sophisticated model.

---

## 4. Extended Results

### 4.1 Premium Model Experiments

Following baseline evaluation, five additional model families were trained with GPU acceleration (NVIDIA RTX 4050 Laptop, 6.4 GB VRAM, CUDA 12.4) using advanced configurations designed to address the failure modes identified in Section 3.

**CTGANPremium Configuration:**
- `use_spectral_norm=True`: Stabilises discriminator training by constraining Lipschitz constant
- `use_gradient_penalty=True`: Penalises discriminator gradients to prevent mode collapse
- Epochs: 500 and 1000 (both tested)

**TVAEPremium Configuration:**
- `use_vamp_prior=True`: Replaces isotropic Gaussian prior with a Variational Mixture of Posteriors (VampPrior), providing a more expressive prior distribution
- `use_cyclical_annealing=True`: Applies cyclical annealing schedule to the KL divergence term, preventing posterior collapse

**CopulaAPI Configuration:**
- Gaussian Copula fitted analytically via rank-based correlation estimation
- No epochs — analytical fitting from correlation matrix

**TabuDiffPremium:**
- GPU-accelerated diffusion with premium noise scheduling
- Score-based denoising with conditional feature generation

**DP-TVAEPremium:**
- VampPrior + cyclical annealing applied to DP-perturbed data
- Privacy budgets: ε ∈ {0.5, 1.0, 2.0} with Laplace mechanism

**Table 3: Premium GPU Experiment Results (1000 rows)**

| Model | TSTR Mean | KS Pass Rate | Schema Valid | Training Time |
|---|---|---|---|---|
| TabuDiff Premium | **0.3892** | 0.0000 | ✅ | ~23 sec/size |
| DP-TVAE Premium (ε=1.0) | 0.3533 | 0.0000 | ✅ | ~2 sec/size |
| CTGAN Premium (500 ep) | 0.3508 | 0.0000 | ✅ | ~90 sec/size |
| DP-TVAE Premium (ε=2.0) | 0.3467 | 0.0000 | ✅ | ~2 sec/size |
| **Copula** | 0.3442 | **0.9286** | ✅ | <1 sec/size |
| DP-TVAE Premium (ε=0.5) | 0.3425 | 0.0000 | ✅ | ~2 sec/size |
| CTGAN Premium (1000 ep) | 0.3275 | 0.0000 | ✅ | ~180 sec/size |

### 4.2 Copula Analysis

The Gaussian Copula result merits specific attention. A Gaussian Copula decomposes the joint distribution P(X₁,...,Xₙ) into:

1. **Marginal distributions** P(Xᵢ) estimated empirically via empirical CDF
2. **Copula function** C — a Gaussian that captures rank-order dependence via the correlation matrix Σ

Generation samples U ∼ Gaussian(0, Σ) in the copula space, then applies the inverse marginal CDF to recover original-scale values.

On the aerospace dataset, this approach achieves KS pass rate = 0.9286 because:
- The empirical marginal CDFs are used directly for U→X transformation, preserving marginal distributions
- The Gaussian copula captures the linear correlation structure faithfully (Pearson r preserved by construction)

The TSTR deficit (0.3442 vs empirical 0.9658) reveals what the copula cannot capture: the non-Gaussian conditional distributions P(target | material_type, geometry) that determine class boundaries. The copula generates feature vectors that are individually plausible and marginally correct, but whose joint distribution in the feature subspace relevant to classification deviates from the training data.

### 4.3 CTGANPremium Spectral Norm Analysis

The gradient penalty and spectral normalisation additions to CTGANPremium were designed to address mode collapse — the failure mode where the generator outputs nearly identical rows regardless of the noise input. Training loss curves confirm that these additions successfully prevent collapse:

- d_loss oscillates between -0.9 and -0.5 throughout training (not converging to 0)
- g_loss shows high variance (5–23) with no plateau, indicating active adversarial competition
- corr metric (correlation preservation) stabilises at 0.065–0.082 after epoch 100

Despite healthy training dynamics, the KS pass rate remains 0.0000. This confirms that the failure is not mode collapse but distributional mismatch: the CTGAN's learned distribution does not match the physics-constrained marginals regardless of training stability.

The 1000-epoch run *degrades* TSTR from 0.3508 (500 ep) to 0.3275, suggesting that additional training causes the generator to specialise further toward the adversarial objective rather than toward statistical fidelity.

### 4.4 Differential Privacy Trade-off Curve

**Table 4: Privacy-Fidelity Trade-off for DP-TVAE Premium**

| Privacy Budget (ε) | TSTR Mean | Privacy Interpretation |
|---|---|---|
| 0.5 (strong) | 0.3425 | High privacy protection, measurable noise |
| 1.0 (moderate) | 0.3533 | Standard privacy budget for medical/aerospace data |
| 2.0 (weak) | 0.3467 | Minimal privacy noise |
| ∞ (baseline TVAE) | ~0.3075 | No privacy protection |

The TSTR range across ε = 0.5 to 2.0 is only 0.011. Paradoxically, ε=1.0 slightly *outperforms* ε=2.0, which may reflect regularisation effects of moderate noise injection on an already underfitting model. The key finding is that for this dataset, differential privacy costs are negligible because the model family's capacity is the binding constraint, not the privacy noise level.

### 4.5 Full Composite Leaderboard

**Table 5: All 31 Experiments — Global Leaderboard (1000-row models)**

| Rank | Model | Composite Score | TSTR | KS Rate | MMD |
|---|---|---|---|---|---|
| 1 | empirical_1000 | **0.9503** | 0.9658 | 1.0000 | 0.0068 |
| 2 | tabudiff_1000 | 0.6901 | 0.3784 | 0.4286 | 0.0102 |
| 3 | maskedpredictor_1000 | 0.3979 | 0.3883 | 0.0714 | 0.0312 |
| 4 | tabudiff_premium_1000 | — | 0.3892 | 0.0000 | — |
| 5 | copula_1000 | — | 0.3442 | **0.9286** | — |
| 6 | ctgan_1000 | 0.2511 | 0.3317 | 0.0000 | 0.9991 |
| 7 | dp_tvae_1000 | 0.2296 | 0.3242 | 0.0000 | 0.9191 |
| 8 | tvae_1000 | 0.2197 | 0.3075 | 0.0000 | 0.6876 |

*Composite = 0.3×(1-mean_KL) + 0.3×TSTR_F1 + 0.2×(1-FI_MAE) + 0.1×(1-disc_AUC) + 0.1×(1-MMD)*

---

## 5. Extended Discussion

### 5.1 Why Physics Datasets Resist Deep Learning Synthesis (Extended)

The fundamental challenge can be formalised. Let X = (X_material, X_geometry, X_environment, Y_targets) be the full feature vector. The dataset records the output of a function f: X_inputs → Y_targets where f is a composite of physical laws (Hooke's law, ISA atmosphere model, failure criteria). The joint distribution P(X) is therefore supported on a low-dimensional manifold M ⊂ ℝ²² defined by the constraints:

- Material consistency: (E, ν, ρ, σ_tensile) must lie on the material-type-specific manifold
- ISA atmosphere: (altitude, temperature, pressure) must approximately satisfy the ISA barometric equation
- Target determinism: Y given inputs is nearly deterministic — a trained Random Forest achieves 0.9658 accuracy

The effective dimensionality of this manifold is much lower than 22. PCA analysis confirms that 13 principal components explain 95% of variance. A generative model must learn to sample precisely on this manifold.

Deep learning generative models approximate the distribution P(X) via a neural network parameterisation. With only 300 training examples and 22 features, the sample density on any local region of M is approximately:

n_local ≈ 300 × (ε/range)^d_eff

where d_eff ≈ 13. Even for ε = 10% of the range per dimension, n_local ≈ 300 × 0.1^13 ≈ 10^{-11} — effectively zero. The neural network must extrapolate across regions it has never seen. KDE resampling with Gaussian noise does not face this problem because it explicitly places probability mass near observed points, leveraging the physical density.

### 5.2 The Genuity Evaluation Philosophy

Genuity's tiered evaluation system encodes a philosophy: synthetic data quality is always relative to a downstream task. The composite score:

*Composite = 0.3 × distributional_fidelity + 0.3 × predictive_utility + 0.2 × feature_importance_preservation + 0.1 × indistinguishability + 0.1 × anomaly_control*

reflects this task-relatedness. A dataset with perfect marginal distributions but incoherent joint structure (KS=1, TSTR=0.33) scores lower than one with imperfect marginals but coherent structure (KS=1, TSTR=0.97), because the latter is more useful for downstream machine learning.

The Tier 1 / Tier 2 separation further distinguishes between:
- **Minimum bar (Tier 1):** Physical validity, schema correctness, no nulls, range compliance. A dataset failing Tier 1 is not synthetic data — it is corrupted data.
- **Statistical fidelity (Tier 2):** Distribution matching, correlation preservation, predictive utility. This is where model families are differentiated.

This framework prevents the common mistake of accepting a synthetic dataset that passes visual inspection (histograms look similar) but fails at the level of joint distributions (correlation structure corrupted, feature importance rankings inverted).

### 5.3 Implications for Aerospace Data Engineering

The aerospace domain has several characteristics that make the empirical-beats-neural finding robust:

1. **Small datasets are structural, not incidental.** Flight test campaigns, FEA simulation batches, and wind tunnel experiments produce hundreds to low thousands of rows. This is not a data collection failure — it reflects the cost of generating ground truth.

2. **Physical constraints are hard.** Unlike the "soft" constraints of income data (income tends to correlate with age, education — but there are exceptions), aerospace constraints are near-deterministic. A material with E=200 GPa and ρ=1,600 kg/m³ is Carbon Fibre — there is no distribution over material types.

3. **Downstream tasks are certification-grade.** Synthetic data for aerospace structural design is not used for A/B testing — it is used to train models that support design decisions and potentially safety certifications. A TSTR accuracy of 0.33 is not "acceptable with caveats" — it is unusable.

4. **Out-of-distribution generation is high-risk.** A synthetic generator that produces rows outside the physical manifold (KS=0, anomaly rate >20%) is creating physically impossible design points. In a certification context, this is a safety risk.

These characteristics collectively mean that for aerospace tabular data:
- The empirical model is the production choice for augmentation
- Deep generative models require at minimum 5,000+ training rows before they can compete
- Copula-based generation is useful for sensitivity analysis (it generates plausible interpolations)
- Differential privacy is achievable without meaningful fidelity cost

### 5.4 Limitations and Future Work

**Limitations of this study:**

1. **Single dataset.** All conclusions are drawn from one 300-row dataset. The failure of deep learning methods on physics data is well-supported theoretically, but the specific composite score thresholds may not generalise to other aerospace datasets.

2. **No dataset augmentation.** The training set for all generative models is the same 300 rows. Methods that use physics simulations to pre-augment the training set before synthetic generation are not evaluated.

3. **Fixed hyperparameters.** The CTGAN and TVAE hyperparameter spaces were not exhaustively searched. It is possible that significantly different architectures (e.g., much larger generator networks) would produce better results, though this is unlikely given the theoretical arguments in Section 5.1.

4. **No conditional generation.** All models generate unconditionally. Conditional generation (conditioning on material type, for example) is supported by CTGAN and could produce better per-class distributional fidelity.

**Future work:**

1. **Physics-constrained generation:** Augmenting TabuDiffPremium with an explicit physics loss term (penalising rows that violate ISA equations or material property constraints) could significantly improve the KS pass rate while preserving TSTR performance.

2. **Larger synthetic training:** Pre-generating a large synthetic dataset (10K+ rows) with the empirical model, training CTGAN/TVAE on this augmented set, and then evaluating — a form of knowledge distillation for generative models.

3. **Hybrid composition:** Combining empirical-generated rows for in-distribution fidelity with TabuDiff-generated rows for distribution boundary exploration, using anomaly scores to filter and blend the two sources.

4. **Domain-specific evaluation metrics:** Developing aerospace-specific fidelity metrics beyond statistical tests — for example, checking that synthetic rows satisfy the von Mises yield criterion or the ISA barometric formula within specified tolerances.

---

## References

Abadi, M., Chu, A., Goodfellow, I., McMahan, H. B., Mironov, I., Talwar, K., & Zhang, L. (2016). Deep learning with differential privacy. *Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security*, 308–318.

Dwork, C., McSherry, F., Nissim, K., & Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Theory of Cryptography Conference*, 265–284.

Ho, J., Jain, A., & Abbeel, P. (2020). Denoising diffusion probabilistic models. *Advances in Neural Information Processing Systems*, 33, 6840–6851.

Kotelnikov, A., Baranchuk, D., Rubachev, I., & Babenko, A. (2022). TabDDPM: Modelling tabular data with diffusion models. *International Conference on Machine Learning*.

Silverman, B. W. (1986). *Density Estimation for Statistics and Data Analysis*. Chapman and Hall.

Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling tabular data using conditional GAN. *Advances in Neural Information Processing Systems*, 32.

---

*Genuity Technical Report v1.0.0 — March 2026*
