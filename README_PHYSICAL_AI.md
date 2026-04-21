# Awesome Physical AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Track](https://img.shields.io/badge/Status-Active%20Research-blue.svg)](https://github.com/AK47-1845/physical-ai) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/AK47-1845/physical-ai/pulls) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **The Definitive Guide, Research Roadmap, and Curated Index for Physical AI, Vision-Language-Action (VLA) Models, World Models, and Embodied Robotics Intelligence.**

---

## 🌟 Executive Overview: The Paradigm Shift

**Physical Artificial Intelligence (Physical AI)** marks the fundamental transition from autoregressive next-token prediction in static semantic spaces to **closed-loop causal interaction with continuous physical dynamics**. 

While Large Language Models (LLMs) operate on statistical association ($P(Y \mid X)$), robots and embodied agents must operate on **causal interventions** ($P(Y \mid \text{do}(u))$) and **counterfactual planning** ($P(Y_u \mid X', Y')$) governed by continuous differential equations:
$$\dot{x} = f(x, u, t)$$

This repository is an open, living, community-driven knowledge base synthesizing **foundational theory, architectural blueprints, canonical failure modes, frontier papers, benchmark datasets, simulation engines, and deployment tooling** for researchers, roboticists, and machine learning engineers worldwide.

---

## 📑 Table of Contents

- [1. Theoretical Foundations](#1-theoretical-foundations)
  - [Pearl's Causal Hierarchy in Robotics](#pearls-causal-hierarchy-in-robotics)
  - [Why Text-Only LLMs Fail in Physical Space](#why-text-only-llms-fail-in-physical-space)
- [2. The Three Schools of World Modeling](#2-the-three-schools-of-world-modeling)
  - [Architectural Comparison Matrix](#architectural-comparison-matrix)
- [3. The Five Canonical Failure Modes & Mitigations](#3-the-five-canonical-failure-modes--mitigations)
- [4. Action Representation & Policy Frontier](#4-action-representation--policy-frontier)
  - [Continuous Flow Matching vs. Discrete Tokenization](#continuous-flow-matching-vs-discrete-tokenization)
  - [Test-Time Policy Composition (EBMs)](#test-time-policy-composition-ebms)
  - [Reinforced Fine-Tuning (RFT) & Residual RL](#reinforced-fine-tuning-rft--residual-rl)
- [5. Synthetic Data Manufacturing & Model Collapse Governance](#5-synthetic-data-manufacturing--model-collapse-governance)
  - [The Accumulate-and-Filter Law](#the-accumulate-and-filter-law)
- [6. Edge Deployment, Latency & Formal Verification](#6-edge-deployment-latency--formal-verification)
  - [Control Barrier Functions & Reachability](#control-barrier-functions--reachability)
  - [Kinematic Invariants & Singularity Robustness](#kinematic-invariants--singularity-robustness)
  - [Channel-Aware Edge Quantization](#channel-aware-edge-quantization)
- [7. Curated Paper Index](#7-curated-paper-index)
  - [Vision-Language Backbones & Representations](#vision-language-backbones--representations)
  - [End-to-End Vision-Language-Action (VLA) Models](#end-to-end-vision-language-action-vla-models)
  - [Modular & Dual-System VLAs](#modular--dual-system-vlas)
  - [Compact & Edge-Optimized VLAs](#compact--edge-optimized-vlas)
  - [Continuous Flow & Diffusion Policies](#continuous-flow--diffusion-policies)
  - [Latent & JEPA-Style World Models](#latent--jepa-style-world-models)
  - [Generative & 3D Spatial World Models](#generative--3d-spatial-world-models)
  - [Embodied Reasoning & Chain-of-Thought](#embodied-reasoning--chain-of-thought)
  - [Reinforcement Learning & Reward Synthesis](#reinforcement-learning--reward-synthesis)
  - [Cross-Embodiment Scaling Laws](#cross-embodiment-scaling-laws)
  - [Humanoid Locomotion & Whole-Body Control](#humanoid-locomotion--whole-body-control)
  - [Sim-to-Real Transfer](#sim-to-real-transfer)
- [8. Datasets & Benchmarks](#8-datasets--benchmarks)
- [9. Physics Engines & Simulation Platforms](#9-physics-engines--simulation-platforms)
- [10. Industry Landscape & Projects](#10-industry-landscape--projects)
- [Contributing & Citation](#contributing--citation)

---

## 1. Theoretical Foundations

### Pearl's Causal Hierarchy in Robotics

Deploying generative models into physical environments exposes a fundamental category error if evaluated purely through statistical prediction. Under **Judea Pearl's Causal Ladder**, intelligence operates across three distinct rungs:

```
                      ▲
     RUNG III         │   Counterfactuals: P(Y_u | X', Y')
   (Imagining)        │   "What would have happened had I applied 10N less torque?"
                      │
     RUNG II          │   Interventions: P(Y | do(u))
     (Doing)          │   "What will the system trajectory be if I actuate joint 3?"
                      │
     RUNG I           │   Associations: P(Y | X)
    (Seeing)          │   "What tokens/pixels statistically co-occur in the dataset?"
                      └────────────────────────────────────────────────────────►
```

- **Rung I (Statistical Association):** Standard autoregressive LLMs model $P(Y \mid X)$. They predict the most probable text tokens from historical corpora.
- **Rung II (Causal Intervention):** Robotics and continuous control require modeling the effect of active physical forces: $P(Y \mid \text{do}(u))$.
- **Rung III (Counterfactual Planning):** Safe multi-step manipulation requires evaluating alternative trajectories: $P(Y_u \mid X', Y')$.

### Why Text-Only LLMs Fail in Physical Space
Language is a 1D symbolic abstraction. Physical space is continuous, non-linear, and governed by:
1. **Kinematics & Dynamics:** $\tau = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + g(q)$
2. **Contact Discontinuities:** Instantaneous momentum transfers and Coulomb friction constraints ($F_{\text{contact}} \le \mu F_N$).
3. **Occlusion & Spatial Geometry:** 3D spatial occupancy that cannot be fully captured by 2D pixel sequences or ungrounded language tokens.

---

## 2. The Three Schools of World Modeling

A **World Model** is a computational surrogate of physical reality that allows an agent to simulate, plan, and evaluate actions before executing them in the irreversible physical world.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE 3 WORLD MODEL SCHOOLS                         │
├───────────────────────┬────────────────────────┬───────────────────────┤
│   SCHOOL I: RENDERER  │   SCHOOL II: LATENT    │  SCHOOL III: SPATIAL  │
│  (Generative Pixels)  │  (Energy-Based JEPA)   │ (Occupancy & Physics) │
├───────────────────────┼────────────────────────┼───────────────────────┤
│ • Diffusion / Video   │ • Joint Embedding      │ • 3D Point Flows      │
│ • Photorealistic      │ • Sub-5ms latency      │ • Formally Verifiable │
│ • High Executability  │ • Abstract dynamics    │ • Explicit mechanics  │
│   Gap (Physics by-    │ • No pixel rendering   │ • Direct Control &    │
│   product of pixels)  │   overhead             │   Digital Twins       │
└───────────────────────┴────────────────────────┴───────────────────────┘
```

### Architectural Comparison Matrix

| Feature | School I: Generative Simulators | School II: Latent / JEPA Models | School III: Spatial & Engineered |
| :--- | :--- | :--- | :--- |
| **Exemplars** | Sora, Genie 1/2, Oasis, Gen-3 | V-JEPA 1/2, DreamerV3, TD-MPC2 | NVIDIA Cosmos/Isaac, Tesla OccNets, Genesis |
| **Prediction Space** | Full RGB pixel video | Abstract latent state embeddings $z_t$ | 3D/4D voxel occupancy + Point-Flows |
| **Inference Latency** | High (0.5--5s / frame) | **Ultra-Low (<5ms)** | Low--Medium (10--50ms) |
| **Physics Grounding** | Emergent (often violates physics) | Abstract dynamics | **Explicit physical constraints & PINNs** |
| **Executability Gap** | High | Low | **Minimal (Simulation-Ready)** |
| **Primary Domain** | Content generation & visual sim | Fast closed-loop motor control | Precision robotics & Digital Twins |

---

## 3. The Five Canonical Failure Modes & Mitigations

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                   5 CANONICAL WORLD MODEL FAILURE MODES                 │
  ├────────────────────────────┬────────────────────────────────────────────┤
  │ FM1: Autoregressive Drift  │ Compounding rollouts: E[||z_hat_T - z_T||] │
  │ FM2: Executability Gap     │ Visually plausible ≠ physically valid      │
  │ FM3: Perceptual Drift      │ OOD states mapped to wrong latent tokens   │
  │ FM4: Action Marginalization│ Model ignores u, plays hallucinations      │
  │ FM5: Sim-to-Real Gap       │ Simulator distribution D_sim ≠ D_real      │
  └────────────────────────────┴────────────────────────────────────────────┘
```

### 1. FM1: Compounding Autoregressive Drift
- **Mathematical Form:** $\mathbb{E}[\|\hat{z}_T - z_T\|] \le \mathcal{O}(T \cdot \epsilon)$
- **Phenomenon:** Minor per-step latent prediction errors $\epsilon$ compound exponentially across rollout horizon $T$. Objects drift, dissolve, or pass through solid barriers.
- **SOTA Mitigations:** Hierarchical State Space Models (Mamba backbones), continuous flow matching, and receding-horizon Model Predictive Control (MPC).

### 2. FM2: The Executability Gap
- **Phenomenon:** Perceptual losses (LPIPS, SSIM) reward visual similarity rather than dynamic validity. Generated trajectories violate Coulomb contact laws ($F_{\text{contact}} \le \mu F_N$).
- **SOTA Mitigations:** Physics-Informed Neural Network (PINN) loss augmentation ($\mathcal{L}_{\text{PINN}} = \|\partial_t u + \mathcal{N}[u] - f\|^2$) and differentiable physics engines (Genesis, ManiSkill3).

### 3. FM3: Perceptual Hallucination
- **Mathematical Form:** $z_q(x) = \arg\min_k \|E(x) - e_k\|_2$
- **Phenomenon:** Vector-quantized encoders force out-of-distribution (OOD) novel physical objects into familiar codebook tokens, corrupting state estimation silently.
- **SOTA Mitigations:** Latent reconstruction residual monitoring ($\mathcal{E}_{\text{recon}} = \|x - \mathcal{D}(\mathcal{E}(x))\|_2 > \tau$) and Mahalanobis latent density gating.

### 4. FM4: Action Marginalization
- **Mathematical Form:** $\nabla_u P(s_{t+1} \mid s_t, u) \longrightarrow 0$
- **Phenomenon:** Transition model predictions become invariant to control inputs $u$, hallucinating autonomous motion while ignoring operator inputs.
- **SOTA Mitigations:** Action-conditioned contrastive InfoNCE objectives and decoupled forward-inverse dynamics pretraining.

### 5. FM5: Sim-to-Real Reality Gap
- **Phenomenon:** $\mathcal{D}_{\text{real}} \neq \mathcal{D}_{\text{sim}}$. Unmodeled friction hysteresis, backlash, and sensor noise cause simulator-trained policies to fail on hardware.
- **SOTA Mitigations:** Iterative Real2Sim2Real closed loops, domain randomization + privileged teacher-student distillation.

---

## 4. Action Representation & Policy Frontier

### Continuous Flow Matching vs. Discrete Tokenization
Traditional VLAs (RT-1, RT-2) tokenized continuous 7-DoF actions using frequency-space transformations (FAST, DCT). While enabling autoregressive LLM reuse, discrete tokenization introduces severe quantization jerkiness and high inference latency.

**Frontier SOTA (Continuous Flow Matching):**
Models like $\pi_0$ and ManiFlow use continuous flow matching vector fields, directly outputting 50Hz continuous velocity commands without tokenization overhead:
$$\frac{dx_t}{dt} = v_\theta(x_t, t, c)$$

```
Discrete Tokenization:     [Image] + [Text] ──► [LLM] ──► [Token a1] ──► [Token a2]  (Slow, Quantized)
Continuous Flow Matching:  [Image] + [Text] ──► [VLM Flow Backbone] ──► v_theta(x, t) (50Hz, Smooth)
```

### Test-Time Policy Composition (EBMs)
Recent breakthroughs (e.g., **GPC**) formulate diffusion/flow policies as Energy-Based Models:
$$p(a \mid o) \propto \exp\left(-\sum_{i=1}^K \mathcal{E}_i(a \mid o)\right)$$
This allows engineers to compose multiple specialized policies at test-time (e.g., **Grasp Policy + Obstacle Avoidance + Compliance Safety Filter**) via convex optimization without retraining the multi-billion-parameter foundation model.

### Reinforced Fine-Tuning (RFT) & Residual RL
- **Stage-Aware RFT (STA-PPO):** Segments manipulation into semantic sub-stages ($\text{Reach} \to \text{Grasp} \to \text{Transport} \to \text{Insert}$) and computes localized advantage functions $\max_\theta \mathbb{E}[A_t^{\text{stage}}]$, overcoming sparse reward bottlenecks (98% success on Bridge SIMPLER).
- **Residual RL:** Freezes the base VLA while an agile residual policy explores recovery behaviors online, distilling recovery trajectories back into the base policy.

---

## 5. Synthetic Data Manufacturing & Model Collapse Governance

### The Accumulate-and-Filter Law
Indiscriminate recursive training on unverified synthetic data causes **Model Collapse** (variance shrinks to zero: $\lim_{n \to \infty} \text{Var}[X_n] = 0$).

To prevent collapse, all modern physical data pipelines must enforce the **Accumulate-and-Filter Governance Law**:
$$\mathcal{D}_{n+1} = \alpha \mathcal{D}_{\text{real}} + (1 - \alpha)\{ x \sim G \mid \text{Verifier}(x) = \mathsf{True} \}$$
- $\alpha$: Governed real-data retention ratio.
- $\text{Verifier}(x)$: Programmatic physics checker (collision engine, kinematics solver, formal reachability verifier).

---

## 6. Edge Deployment, Latency & Formal Verification

### Control Barrier Functions & Reachability
For safety-critical physical systems, neural policy outputs $u = \pi_\theta(o)$ must be constrained to a certified safe set $\mathcal{C} = \{x \mid h(x) \ge 0\}$ via **Control Barrier Functions (CBFs)**:
$$\dot{h}(x, u) = \nabla h(x) \cdot f(x, \pi_\theta(x)) \ge -\alpha(h(x))$$
Forward **Reachable Sets** $\mathcal{R}(T; \mathcal{X}_0)$ are computed via interval neural network bound propagation ($\alpha,\beta$-CROWN), verifying $\mathcal{R}(T; \mathcal{X}_0) \subseteq \mathcal{C}$ for ISO 13849 / IEC 61508 safety dossiers.

### Kinematic Invariants & Singularity Robustness
In robot control, Cartesian velocities $\dot{x} \in \mathbb{R}^6$ map to joint rates $\dot{q} \in \mathbb{R}^n$ via the Jacobian $J(q)$:
$$\dot{q} = J^{\dagger}(q)\dot{x}$$
Near kinematic singularities where Yoshikawa manipulability:
$$\mu(q) = \sqrt{\det\left(J(q)J^T(q)\right)} \longrightarrow 0$$
raw Cartesian VLA commands demand infinite joint speeds ($\|\dot{q}\| \to \infty$). Deploying policies in production requires **Damped Least-Squares (DLS)** filtering:
$$J^* = J^T (J J^T + \lambda^2 I)^{-1}$$

### Channel-Aware Edge Quantization
- **AutoQVLA:** Selectively retains sensitive attention channels in FP16 while quantizing 90% of parameters to INT4/INT8, reducing VRAM to 30% on NVIDIA Jetson AGX Orin.
- **HyperVLA:** Uses a 7B model once at task initialization to synthesize an ultra-lightweight (10M parameter) execution policy that runs at 200Hz on low-power edge compute.

---

## 7. Curated Paper Index

### Vision-Language Backbones & Representations
- **CLIP** (ICML 2021) - "Learning Transferable Visual Models From Natural Language Supervision" [[Paper](https://arxiv.org/abs/2103.00020)]
- **DINOv2** (arXiv 2023) - "Learning Robust Visual Features without Supervision" [[Paper](https://arxiv.org/abs/2304.07193)]
- **SAM** (ICCV 2023) - "Segment Anything" [[Paper](https://arxiv.org/abs/2304.02643)]
- **SigLIP** (ICCV 2023) - "Sigmoid Loss for Language Image Pre-Training" [[Paper](https://arxiv.org/abs/2303.15343)]
- **Prismatic VLMs** (ICML 2024) - "Investigating the Design Space of Visually-Conditioned Language Models" [[Paper](https://arxiv.org/abs/2402.07865)]

### End-to-End Vision-Language-Action (VLA) Models
- **RT-1** (RSS 2023) - "Robotics Transformer for Real-World Control at Scale" [[Paper](https://arxiv.org/abs/2212.06817)]
- **RT-2** (CoRL 2023) - "Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" [[Paper](https://arxiv.org/abs/2307.15818)]
- **OpenVLA** (CoRL 2024) - "An Open-Source Vision-Language-Action Model" [[Paper](https://arxiv.org/abs/2406.09246)]
- **PaLM-E** (ICML 2023) - "An Embodied Multimodal Language Model" [[Paper](https://arxiv.org/abs/2303.03378)]
- **UniVLA** (arXiv 2025) - "Unified Vision-Language-Action Model via Interleaved Tokens" [[Paper](https://arxiv.org/abs/2506.19850)]
- **π0.5** (Physical Intelligence 2025) - "Scaling Robot Foundation Models with Open-World Generalization" [[Blog](https://www.pi.website/blog/pi05)]
- **GR-3** (ByteDance Seed 2025) - "GR-3 Technical Report" [[Paper](https://arxiv.org/abs/2507.15493)]
- **LingBot-VLA** (Ant Group 2026) - "A Pragmatic VLA Foundation Model" [[Paper](https://arxiv.org/abs/2601.18692)]

### Modular & Dual-System VLAs
- **SayCan** (CoRL 2022) - "Grounding Language in Robotic Affordances" [[Paper](https://arxiv.org/abs/2204.01691)]
- **Code as Policies** (arXiv 2022) - "Language Model Programs for Embodied Control" [[Paper](https://arxiv.org/abs/2209.07753)]
- **Gemini Robotics 1.5** (Google DeepMind 2025) - "Pushing the Frontier of Generalist Robots with Advanced Reasoning" [[Paper](https://arxiv.org/abs/2510.03342)]
- **Fast-in-Slow** (arXiv 2025) - "A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning" [[Paper](https://arxiv.org/abs/2506.01953)]

### Compact & Edge-Optimized VLAs
- **SmolVLA** (Hugging Face 2025) - "A Small Vision-Language-Action Model for Efficient Robot Learning" [[Blog](https://huggingface.co/blog/smolvla)]
- **BitVLA** (arXiv 2025) - "1-bit Vision-Language-Action Models for Robotics Manipulation" [[Paper](https://arxiv.org/abs/2506.07530)]
- **AutoQVLA** (ICLR 2026) - "Not All Channels Are Equal in Vision-Language-Action Model Quantization"
- **HyperVLA** (ICLR 2026) - "Efficient Inference in Vision-Language-Action Models via Hypernetworks"
- **DynamicVLA** (arXiv 2026) - "A Vision-Language-Action Model for Dynamic Object Manipulation" [[Paper](https://arxiv.org/abs/2601.22153)]

### Continuous Flow & Diffusion Policies
- **Diffusion Policy** (RSS 2023) - "Visuomotor Policy Learning via Action Diffusion" [[Paper](https://arxiv.org/abs/2303.04137)]
- **π₀ (pi-zero)** (Physical Intelligence 2024) - "A Vision-Language-Action Flow Model for General Robot Control" [[Paper](https://arxiv.org/abs/2410.24164)]
- **ManiFlow** (CoRL 2025) - "A General Robot Manipulation Policy via Consistency Flow Training" [[Paper](https://arxiv.org/abs/2509.01819)]
- **Streaming Flow Policy** (CoRL 2025 Oral) - "Simplifying Diffusion / Flow-Matching Policies" [[Paper](https://arxiv.org/abs/2505.21851)]
- **GPC** (arXiv 2025) - "Compose Your Policies! Test-Time Distribution-Level Composition" [[Paper](https://arxiv.org/abs/2510.01068)]

### Latent & JEPA-Style World Models
- **LeCun Architectural Blueprint** (Meta AI 2022) - "A Path Towards Autonomous Machine Intelligence" [[Paper](https://openreview.net/pdf?id=BZ5a1r-kVsf)]
- **I-JEPA** (CVPR 2023) - "Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture" [[Paper](https://arxiv.org/abs/2301.08243)]
- **V-JEPA 2** (Meta AI 2025) - "Self-Supervised Video Models Enable Understanding, Prediction and Planning" [[Paper](https://arxiv.org/abs/2506.09985)]
- **DreamerV3** (arXiv 2023) - "Mastering Diverse Domains through World Models" [[Paper](https://arxiv.org/abs/2301.04104)]

### Generative & 3D Spatial World Models
- **Genie 2** (Google DeepMind 2024) - "A Large-Scale Foundation World Model" [[Blog](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)]
- **Cosmos-Predict2.5** (NVIDIA 2025) - "World Simulation with Video Foundation Models for Physical AI" [[Paper](https://arxiv.org/abs/2511.00062)]
- **PointWorld** (NVIDIA 2026) - "Scaling 3D World Models for In-The-Wild Robotic Manipulation" [[Paper](https://arxiv.org/abs/2601.03782)]
- **DreamDojo** (NVIDIA GEAR 2026) - "A Generalist Robot World Model from Large-Scale Human Videos" [[Paper](https://arxiv.org/abs/2602.06949)]

### Cross-Embodiment Scaling Laws
- **Open X-Embodiment (RT-X)** (ICRA 2024) - "Robotic Learning Datasets and RT-X Models" [[Paper](https://arxiv.org/abs/2310.08864)]
- **Crossformer** (CoRL 2024) - "Scaling Cross-Embodied Learning: One Policy for Manipulation, Navigation, Locomotion" [[Paper](https://arxiv.org/abs/2408.11812)]
- **EgoScale** (NVIDIA GEAR 2026) - "Scaling Dexterous Manipulation with Diverse Egocentric Human Data" [[Paper](https://arxiv.org/abs/2602.16710)]
- **Being-H0.5** (BeingBeyond 2026) - "Scaling Human-Centric Robot Learning for Cross-Embodiment Generalization" [[Paper](https://arxiv.org/abs/2601.12993)]

---

## 8. Datasets & Benchmarks

| Dataset / Benchmark | Modality & Scale | Description | Link |
| :--- | :--- | :--- | :--- |
| **Open X-Embodiment** | 1M+ trajectories, 22 embodiments | Cross-embodiment robot manipulation | [Site](https://robotics-transformer-x.github.io/) |
| **DROID** | 76k trajectories, 564 scenes | In-the-wild Franka Panda demonstrations | [Site](https://droid-dataset.github.io/) |
| **SIMPLER** | Simulated evaluation benchmark | Evaluates real-to-sim visual policy transfer | [Site](https://simpler-env.github.io/) |
| **LIBERO** | 130 standardized tasks | Lifelong and multi-task manipulation benchmark | [Site](https://libero-project.github.io/) |
| **CALVIN** | Long-horizon multi-task | Language-conditioned tabletop manipulation | [Site](http://calvin.cs.uni-freiburg.de/) |
| **RoboCasa** | Large-scale kitchen benchmark | Photorealistic household simulation | [Site](https://robocasa.ai/) |
| **RoboTwin 2.0** | Dual-arm bimanual tasks | High-fidelity domain-randomized benchmark | [Site](https://robotwin-platform.github.io/) |

---

## 9. Physics Engines & Simulation Platforms

| Engine | Developer | Primary Focus | Link |
| :--- | :--- | :--- | :--- |
| **Genesis** | MIT / Stanford | Differentiable multi-physics simulation | [Site](https://genesis-embodied-ai.github.io/) |
| **Isaac Sim / Isaac Lab** | NVIDIA | GPU-accelerated photorealistic robotics sim | [Site](https://developer.nvidia.com/isaac-sim) |
| **ManiSkill3** | UCSD | Massive parallelized GPU robot simulation | [Site](https://www.maniskill.ai/) |
| **MuJoCo Playground** | Google DeepMind | Fast contact dynamics & browser-based testing | [Site](https://playground.mujoco.org/) |
| **OmniGibson** | Stanford SVL | High-fidelity home simulation with interactive physics | [Site](https://behavior.stanford.edu/omnigibson/) |

---

## 10. Industry Landscape & Projects

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PHYSICAL AI INDUSTRY STACK (2026)                    │
├────────────────────────────────────────────────────────────────────────┤
│ FOUNDATION MODELS:  Physical Intelligence (π0), Skild AI, DeepMind     │
│ INDUSTRIAL AUTOMATION: Siemens, Rockwell Automation, ABB, Schneider    │
│ SIMULATION & V&V:   NVIDIA Omniverse/Isaac, Applied Intuition, Scale AI │
│ SYSTEM INTEGRATORS: Brownfield PLC-to-VLA bridges, Custom V&V Dossiers │
│ HARDWARE PLATFORMS: Unitree, Figure AI, Boston Dynamics, Agility, 1X   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Contributing & Community

We actively welcome community contributions! Please review [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a Pull Request.

### Guidelines:
1. **Verifiability:** Ensure all cited papers include valid arXiv/venue links.
2. **Category Accuracy:** Place new papers in their appropriate architectural cluster.
3. **No Fluff:** Maintain technical precision and mathematical rigor.

---

## Citation

If you find this repository helpful in your research or engineering workflows, please cite:

```bibtex
@misc{physical-ai-guide,
  author = {Adari Karthikeya},
  title = {Awesome Physical AI: The Definitive Research Roadmap & Resource Guide},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/AK47-1845/physical-ai}}
}
```

---
<div align="center">
  <sub>Maintained with rigorous engineering standards by the open-source Physical AI community.</sub>
</div>
