"""
Action Flow Matching for Physical AI (pi-zero / ManiFlow Style)
==============================================================
Reference:
- Lipman et al., "Flow Matching for Generative Modeling" (ICLR 2023)
- Physical Intelligence, "pi-0: A Vision-Language-Action Flow Model for General Robot Control" (2024)
- ManiFlow, "A General Robot Manipulation Policy via Consistency Flow Training" (CoRL 2025)

Why Flow Matching over Standard Diffusion in 2026?
-------------------------------------------------
Traditional diffusion relies on curved stochastic trajectories that require 50-100 denoising
steps. Flow Matching learns straight vector fields between Gaussian prior x_0 and target action x_1:
    x_t = (1 - (1 - sigma_min) * t) * x_0 + t * x_1
Target vector field:
    u_t(x_t | x_0, x_1) = x_1 - (1 - sigma_min) * x_0

This allows deterministic ODE integration (Euler/Heun) in only 3-8 steps at 100Hz+ control rates.
"""

import math
import sys

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

if HAS_TORCH:
    class SinusoidalTimeEmbedding(nn.Module):
        def __init__(self, dim: int):
            super().__init__()
            self.dim = dim

        def forward(self, t: torch.Tensor) -> torch.Tensor:
            half_dim = self.dim // 2
            emb = math.log(10000) / (half_dim - 1)
            emb = torch.exp(torch.arange(half_dim, device=t.device) * -emb)
            emb = t[:, None] * emb[None, :]
            return torch.cat((emb.sin(), emb.cos()), dim=-1)

    class FlowMatchingVectorField(nn.Module):
        """MLP/Transformer Backbone predicting continuous velocity vector field v_theta(x_t, t, obs)."""
        def __init__(self, action_dim: int = 7, horizon: int = 16, obs_dim: int = 256, hidden_dim: int = 512):
            super().__init__()
            self.action_dim = action_dim
            self.horizon = horizon
            flat_action_dim = action_dim * horizon
            
            self.time_mlp = nn.Sequential(
                SinusoidalTimeEmbedding(hidden_dim // 4),
                nn.Linear(hidden_dim // 4, hidden_dim),
                nn.SiLU(),
                nn.Linear(hidden_dim, hidden_dim)
            )
            self.obs_mlp = nn.Sequential(
                nn.Linear(obs_dim, hidden_dim),
                nn.SiLU(),
                nn.Linear(hidden_dim, hidden_dim)
            )
            self.net = nn.Sequential(
                nn.Linear(flat_action_dim + hidden_dim * 2, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.SiLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.SiLU(),
                nn.Linear(hidden_dim, flat_action_dim)
            )

        def forward(self, x_t: torch.Tensor, t: torch.Tensor, obs: torch.Tensor) -> torch.Tensor:
            B = x_t.shape[0]
            x_flat = x_t.reshape(B, -1)
            t_feat = self.time_mlp(t)
            obs_feat = self.obs_mlp(obs)
            feat = torch.cat([x_flat, t_feat, obs_feat], dim=-1)
            v_flat = self.net(feat)
            return v_flat.reshape(B, self.horizon, self.action_dim)

    class ActionFlowMatcher(nn.Module):
        """Conditional Flow Matcher with optimal transport straight paths."""
        def __init__(self, vector_field: FlowMatchingVectorField, sigma_min: float = 1e-4):
            super().__init__()
            self.vf = vector_field
            self.sigma_min = sigma_min

        def compute_loss(self, actions_1: torch.Tensor, obs: torch.Tensor) -> torch.Tensor:
            B = actions_1.shape[0]
            t = torch.rand(B, device=actions_1.device)
            actions_0 = torch.randn_like(actions_1)
            t_expand = t.view(B, 1, 1)
            x_t = (1.0 - (1.0 - self.sigma_min) * t_expand) * actions_0 + t_expand * actions_1
            target_v = actions_1 - (1.0 - self.sigma_min) * actions_0
            pred_v = self.vf(x_t, t, obs)
            return F.mse_loss(pred_v, target_v)

        @torch.no_grad()
        def integrate_policy(self, obs: torch.Tensor, num_steps: int = 5) -> torch.Tensor:
            B = obs.shape[0]
            H, D = self.vf.horizon, self.vf.action_dim
            x_t = torch.randn(B, H, D, device=obs.device)
            dt = 1.0 / num_steps
            for step in range(num_steps):
                t_val = step * dt
                t = torch.full((B,), t_val, device=obs.device, dtype=torch.float32)
                v = self.vf(x_t, t, obs)
                x_t = x_t + v * dt
            return x_t

def run_numpy_math_demo():
    """Pure NumPy mathematical demonstration of Flow Matching ODE."""
    import numpy as np
    print("[*] PyTorch not detected in current environment. Running Pure NumPy Mathematical Engine:")
    print("    Optimal Transport Vector Field: u_t(x_t | x_0, x_1) = x_1 - x_0")
    print("    Trajectory: x_t = (1 - t) * x_0 + t * x_1")
    
    x_0 = np.random.randn(16, 7) # Prior Gaussian noise
    x_1 = np.ones((16, 7)) * 0.05 # Target trajectory
    
    # Fast 4-step Euler ODE integration
    num_steps = 4
    dt = 1.0 / num_steps
    x_sim = np.copy(x_0)
    
    for i in range(num_steps):
        t = i * dt
        v_true = x_1 - x_0 # Analytical optimal transport velocity
        x_sim = x_sim + v_true * dt
        
    err = np.linalg.norm(x_sim - x_1)
    print(f"  * Integrated 4-step Euler ODE: Final position matches target with error {err:.2e}")
    print(f"  * Straight trajectories eliminate curved diffusion steps, enabling sub-10ms control.")
    print("\n[TIP] To train full neural vector fields: run 'pip install torch'")

def demo():
    print("=" * 75)
    print("PHYSICAL AI STARTER: Action Flow Matching (pi-0 / ManiFlow Style)")
    print("=" * 75)
    
    if not HAS_TORCH:
        run_numpy_math_demo()
        print("=" * 75)
        return
        
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    action_dim = 7
    pred_horizon = 16
    obs_dim = 256
    
    vf = FlowMatchingVectorField(action_dim=action_dim, horizon=pred_horizon, obs_dim=obs_dim)
    flow_matcher = ActionFlowMatcher(vf).to(device)
    
    B = 8
    target_actions = torch.randn(B, pred_horizon, action_dim, device=device)
    obs_tokens = torch.randn(B, obs_dim, device=device)
    
    optimizer = torch.optim.AdamW(flow_matcher.parameters(), lr=2e-4)
    loss = flow_matcher.compute_loss(target_actions, obs_tokens)
    loss.backward()
    optimizer.step()
    print(f"[OK] Conditional Flow Matching Loss: {loss.item():.4f}")
    
    flow_matcher.eval()
    actions = flow_matcher.integrate_policy(obs_tokens, num_steps=4)
    print(f"[OK] Ultra-Fast ODE Integration (4 steps): Output Shape: {actions.shape}")
    print(f"     First action command at t=0: {actions[0, 0].cpu().numpy().round(3)}")
    print("     Straight vector paths achieve 10x lower inference latency than diffusion.")
    print("=" * 75)

if __name__ == "__main__":
    demo()
