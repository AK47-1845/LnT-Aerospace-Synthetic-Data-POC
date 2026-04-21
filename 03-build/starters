"""
Minimal Diffusion Policy for Continuous Action Chunking in Physical AI
=======================================================================
Reference: Chi et al., "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion" (RSS 2023)

In Physical AI, policies cannot simply output single discrete tokens without inducing
chatter and compounding errors. Instead, policies generate continuous multi-step
trajectories ("action chunks") via conditional reverse diffusion:
    p(A | O) where A = [a_t, a_{t+1}, ..., a_{t+H-1}] in R^{H x D}

This script provides a clean, standalone reference implementation:
1. Sinusoidal Positional Embeddings for diffusion timesteps
2. 1D Temporal Convolutional Denoising Backbone with FiLM conditioning on observations
3. Denoising Diffusion Probabilistic Model (DDPM) training and inference loops
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
    class SinusoidalPosEmb(nn.Module):
        """Sinusoidal positional embedding for diffusion timestep k."""
        def __init__(self, dim: int):
            super().__init__()
            self.dim = dim

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            device = x.device
            half_dim = self.dim // 2
            emb = math.log(10000) / (half_dim - 1)
            emb = torch.exp(torch.arange(half_dim, device=device) * -emb)
            emb = x[:, None] * emb[None, :]
            emb = torch.cat((emb.sin(), emb.cos()), dim=-1)
            return emb

    class FiLMBlock(nn.Module):
        """Feature-wise Linear Modulation (FiLM) conditioned residual 1D conv block."""
        def __init__(self, in_channels: int, out_channels: int, cond_dim: int):
            super().__init__()
            self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size=5, padding=2)
            self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size=5, padding=2)
            self.cond_proj = nn.Linear(cond_dim, out_channels * 2)
            self.residual = nn.Conv1d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()

        def forward(self, x: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
            res = self.residual(x)
            h = F.mish(self.conv1(x))
            scale_shift = self.cond_proj(cond).unsqueeze(-1)
            scale, shift = scale_shift.chunk(2, dim=1)
            h = h * (1.0 + scale) + shift
            h = F.mish(self.conv2(h))
            return h + res

    class DiffusionPolicy1D(nn.Module):
        """1D Temporal CNN Denoising Backbone for action trajectories."""
        def __init__(self, action_dim: int = 7, pred_horizon: int = 16, obs_dim: int = 128, hidden_dim: int = 256):
            super().__init__()
            self.action_dim = action_dim
            self.pred_horizon = pred_horizon
            
            self.time_emb = nn.Sequential(
                SinusoidalPosEmb(hidden_dim),
                nn.Linear(hidden_dim, hidden_dim * 2),
                nn.Mish(),
                nn.Linear(hidden_dim * 2, hidden_dim)
            )
            self.obs_proj = nn.Linear(obs_dim, hidden_dim)
            cond_dim = hidden_dim * 2

            self.in_proj = nn.Conv1d(action_dim, hidden_dim, kernel_size=1)
            self.block1 = FiLMBlock(hidden_dim, hidden_dim, cond_dim)
            self.block2 = FiLMBlock(hidden_dim, hidden_dim, cond_dim)
            self.block3 = FiLMBlock(hidden_dim, hidden_dim, cond_dim)
            self.out_proj = nn.Conv1d(hidden_dim, action_dim, kernel_size=1)

        def forward(self, noisy_actions: torch.Tensor, timesteps: torch.Tensor, obs: torch.Tensor) -> torch.Tensor:
            x = noisy_actions.transpose(1, 2)
            t_emb = self.time_emb(timesteps)
            o_emb = F.mish(self.obs_proj(obs))
            cond = torch.cat([t_emb, o_emb], dim=-1)
            
            h = self.in_proj(x)
            h = self.block1(h, cond)
            h = self.block2(h, cond)
            h = self.block3(h, cond)
            out = self.out_proj(h)
            return out.transpose(1, 2)

    class DiffusionModel(nn.Module):
        """DDPM wrapper for action chunk diffusion."""
        def __init__(self, policy_net: DiffusionPolicy1D, num_diffusion_steps: int = 50):
            super().__init__()
            self.net = policy_net
            self.num_steps = num_diffusion_steps
            
            beta = torch.linspace(1e-4, 0.02, num_diffusion_steps)
            alpha = 1.0 - beta
            alpha_bar = torch.cumprod(alpha, dim=0)
            self.register_buffer('beta', beta)
            self.register_buffer('alpha', alpha)
            self.register_buffer('alpha_bar', alpha_bar)

        def compute_loss(self, actions: torch.Tensor, obs: torch.Tensor) -> torch.Tensor:
            B, H, D = actions.shape
            t = torch.randint(0, self.num_steps, (B,), device=actions.device).long()
            noise = torch.randn_like(actions)
            alpha_bar_t = self.alpha_bar[t].view(B, 1, 1)
            noisy_actions = torch.sqrt(alpha_bar_t) * actions + torch.sqrt(1.0 - alpha_bar_t) * noise
            pred_noise = self.net(noisy_actions, t, obs)
            return F.mse_loss(pred_noise, noise)

        @torch.no_grad()
        def sample_actions(self, obs: torch.Tensor, horizon: int = 16) -> torch.Tensor:
            B = obs.shape[0]
            D = self.net.action_dim
            actions = torch.randn((B, horizon, D), device=obs.device)
            for i in reversed(range(self.num_steps)):
                t = torch.full((B,), i, device=obs.device, dtype=torch.long)
                pred_noise = self.net(actions, t, obs)
                beta_t = self.beta[i]
                alpha_t = self.alpha[i]
                alpha_bar_t = self.alpha_bar[i]
                actions = (1.0 / torch.sqrt(alpha_t)) * (actions - (beta_t / torch.sqrt(1.0 - alpha_bar_t)) * pred_noise)
                if i > 0:
                    actions = actions + torch.sqrt(beta_t) * torch.randn_like(actions)
            return actions

def run_numpy_math_demo():
    """Deterministic mathematical demonstration when PyTorch is not yet installed."""
    import numpy as np
    print("[*] PyTorch not detected in current environment. Running Pure NumPy Mathematical Engine:")
    print("    Formula: x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * epsilon")
    
    num_steps = 20
    beta = np.linspace(1e-4, 0.02, num_steps)
    alpha = 1.0 - beta
    alpha_bar = np.cumprod(alpha)
    
    # Simulate a 16-step action trajectory for 7 DoF robot
    x_0 = np.ones((16, 7)) * 0.1  # nominal target trajectory
    noise = np.random.randn(16, 7)
    
    t = 10  # Midpoint diffusion step
    x_t = np.sqrt(alpha_bar[t]) * x_0 + np.sqrt(1.0 - alpha_bar[t]) * noise
    
    print(f"  * Diffusion Steps: {num_steps} | Schedule: Linear [1e-4 -> 0.02]")
    print(f"  * Action Chunk Shape: (16 timesteps, 7 DoF: dx, dy, dz, droll, dpitch, dyaw, gripper)")
    print(f"  * Alpha_bar at step 10: {alpha_bar[t]:.4f}")
    print(f"  * Noisy action chunk sampled successfully (Frobenius norm: {np.linalg.norm(x_t):.3f})")
    print("\n[TIP] To train full 1D Conv nets on GPU: run 'pip install torch'")

def demo():
    print("=" * 75)
    print("PHYSICAL AI STARTER: Diffusion Policy Action Chunking (DDPM)")
    print("=" * 75)
    
    if not HAS_TORCH:
        run_numpy_math_demo()
        print("=" * 75)
        return
        
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    action_dim = 7
    pred_horizon = 16
    obs_dim = 128
    
    backbone = DiffusionPolicy1D(action_dim=action_dim, pred_horizon=pred_horizon, obs_dim=obs_dim)
    model = DiffusionModel(backbone, num_diffusion_steps=20).to(device)
    
    B = 8
    dummy_obs = torch.randn(B, obs_dim, device=device)
    dummy_actions = torch.randn(B, pred_horizon, action_dim, device=device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    loss = model.compute_loss(dummy_actions, dummy_obs)
    loss.backward()
    optimizer.step()
    print(f"[OK] Training Forward Loss computed: {loss.item():.4f}")
    
    model.eval()
    generated_actions = model.sample_actions(dummy_obs, horizon=pred_horizon)
    print(f"[OK] Inference Success: Generated Action Chunk shape: {generated_actions.shape}")
    print(f"     Batch size: {generated_actions.shape[0]}, Horizon: {generated_actions.shape[1]} steps, Action DoF: {generated_actions.shape[2]}")
    print(f"     First predicted action: {generated_actions[0, 0].cpu().numpy().round(3)}")
    print("=" * 75)

if __name__ == "__main__":
    demo()
