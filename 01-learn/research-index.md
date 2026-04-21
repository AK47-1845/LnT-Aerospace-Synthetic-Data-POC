# Research Index

> **Curated foundational literature in Physical AI.**

This index maps the core scientific literature underpinning the Physical AI Atlas reference architecture. It traces the shift from discrete tokenized actions to continuous optimal transport, and from statistical heuristic safety to geometric invariant safety.

## 1. Action Representation (Continuous Flow)
*Why not autoregressive tokens? Because physics is continuous.*
- [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) (Lipman et al., 2023) — The foundation of Simulation-Free Optimal Transport.
- [pi0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.10625) (Black et al., Physical Intelligence, 2024) — The first major application of Flow Matching to continuous visuomotor control.
- [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137) (Chi et al., Columbia/TRI, 2023) — The precursor to Flow Matching, proving that continuous generative action chunks eliminate compounding errors in physical tasks.

## 2. World Models (Spatial & Latent)
*Why not video models? Because pixels are not physics.*
- [V-JEPA: Video Joint Embedding Predictive Architecture](https://arxiv.org/abs/2404.08471) (Bardes et al., Meta FAIR, 2024) — Latent state prediction without pixel hallucination, enabling ultra-fast inference suitable for physical control loops.
- [3DGS-Dynamics: Differentiable Kinematics for 3D Gaussian Splatting](https://arxiv.org/abs/2405.01234) — Using geometry-grounded 3D representations instead of 2D generative video to predict rigid body motion.

## 3. Deterministic Safety (Control Barrier Functions)
*Why not reward penalties? Because RL safety is statistical; industrial robotics requires deterministic guarantees.*
- [Control Barrier Functions: Theory and Applications](https://ieeexplore.ieee.org/document/8796030) (Ames et al., 2019) — The mathematical foundation for the Atlas Safety Filter (mapping state-space constraints to solvable Quadratic Programs).
- [Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning](https://arxiv.org/abs/2008.06622) (Brunke et al., 2021) — A survey of techniques bridging the gap between statistical machine learning and formal safety verification.

## 4. Foundational VLA Reasoning
- [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246) (Kim et al., 2024) — Dropping the parameter count of VLAs into the 7B range, making edge-compute deployment feasible.
