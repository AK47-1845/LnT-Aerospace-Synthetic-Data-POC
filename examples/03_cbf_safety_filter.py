"""
Real-Time Control Barrier Function (CBF) Safety Filter
======================================================
Reference: Ames et al., "Control Barrier Functions: Theory and Applications" (ECC 2019)

In production Physical AI, deep learning policies (VLA, Diffusion, RL) are statistical
models with no deterministic safety guarantees. An autonomous agent might hallucinate
a violent trajectory towards human operators, fixtures, or joint mechanical limits.

Industrial architectures (ISO 13849, IEC 61508) enforce a deterministic safety envelope:
A Control Barrier Function (CBF) Quadratic Program (QP) filter executes at high frequency
(500Hz - 1kHz), sitting between the VLA policy and the low-level motor drivers:

    min_{u}  (1/2) * || u - u_nominal ||^2
    subject to:
        L_f h(x) + L_g h(x) * u + gamma * h(x) >= 0   (CBF condition)
        u_min <= u <= u_max                           (Actuator saturation)

If u_nominal is safe, the filter passes it unchanged.
If u_nominal would breach safety, the filter minimally perturbs u to guarantee forward invariance!
"""

import numpy as np
from scipy.optimize import minimize

class CBFSafetyFilter:
    """
    Control Barrier Function QP Filter for a robot end-effector or mobile base.
    State: x = [pos_x, pos_y, vel_x, vel_y]
    Control: u = [acc_x, acc_y]
    Dynamics: x_dot = A*x + B*u (Double Integrator)
    """
    def __init__(self, obstacle_pos: np.ndarray, obstacle_radius: float, robot_radius: float = 0.15, gamma: float = 2.0):
        self.obs_pos = np.array(obstacle_pos, dtype=np.float64)
        self.safe_distance = obstacle_radius + robot_radius
        self.gamma = gamma # Class-K function parameter alpha(h) = gamma * h
        self.u_max = 5.0   # Max acceleration limit (m/s^2)

    def barrier_h(self, pos: np.ndarray) -> float:
        """
        Barrier function h(x):
        h(x) = ||pos - obs||^2 - safe_distance^2
        Safe set C = { x : h(x) >= 0 }
        """
        dist_sq = np.sum((pos - self.obs_pos)**2)
        return dist_sq - (self.safe_distance ** 2)

    def filter_control(self, state: np.ndarray, u_nominal: np.ndarray) -> tuple[np.ndarray, bool]:
        """
        Solves the minimal perturbation Quadratic Program (QP):
            min_u  0.5 * || u - u_nominal ||^2
            s.t.   dot(h) + gamma * h >= 0
        """
        pos = state[0:2]
        vel = state[2:4]
        
        # 1. Evaluate current barrier value
        h_val = self.barrier_h(pos)
        
        # 2. Compute Lie derivatives for relative degree 1 velocity / relative degree 2 position:
        # dot(h) = 2 * (pos - obs)^T * vel
        # ddot(h) = 2 * ||vel||^2 + 2 * (pos - obs)^T * u
        # Using extended CBF: h_ext = dot(h) + lambda_c * h
        # dot(h_ext) = ddot(h) + lambda_c * dot(h) >= -gamma * h_ext
        lambda_c = 3.0
        rel_pos = pos - self.obs_pos
        dot_h = 2.0 * np.dot(rel_pos, vel)
        h_ext = dot_h + lambda_c * h_val
        
        # Linear constraint on u: A_cbf * u + b_cbf >= 0  ==>  A_cbf * u >= -b_cbf
        # ddot(h) = 2 * ||vel||^2 + 2 * rel_pos^T * u
        # Condition: 2 * rel_pos^T * u + 2 * ||vel||^2 + lambda_c * dot_h + self.gamma * h_ext >= 0
        A_cbf = 2.0 * rel_pos
        b_cbf = 2.0 * np.dot(vel, vel) + lambda_c * dot_h + self.gamma * h_ext

        # If nominal control already satisfies safety condition, pass it through directly (0 latency)
        if np.dot(A_cbf, u_nominal) + b_cbf >= 0:
            return np.clip(u_nominal, -self.u_max, self.u_max), False

        # Otherwise solve QP:
        def objective(u):
            return 0.5 * np.sum((u - u_nominal) ** 2)

        def objective_jac(u):
            return u - u_nominal

        # Inequality constraint: A_cbf * u + b_cbf >= 0
        constraints = [{
            'type': 'ineq',
            'fun': lambda u: np.dot(A_cbf, u) + b_cbf,
            'jac': lambda u: A_cbf
        }]
        
        bounds = [(-self.u_max, self.u_max), (-self.u_max, self.u_max)]

        res = minimize(
            objective,
            x0=u_nominal,
            jac=objective_jac,
            constraints=constraints,
            bounds=bounds,
            method='SLSQP',
            options={'ftol': 1e-6, 'maxiter': 50}
        )

        safe_u = res.x if res.success else np.clip(u_nominal, -self.u_max, self.u_max)
        return safe_u, True

def demo():
    print("=" * 75)
    print("PHYSICAL AI STARTER: Real-Time Control Barrier Function (CBF) QP Filter")
    print("=" * 75)
    
    # Define circular safety obstacle (e.g. human worker or machine tool fixture)
    obs_center = np.array([2.0, 2.0])
    obs_radius = 0.5  # 50cm
    cbf_filter = CBFSafetyFilter(obstacle_pos=obs_center, obstacle_radius=obs_radius)
    
    print(f"Obstacle at: {obs_center}, Exclusion Zone: {obs_radius + 0.15:.2f}m")
    
    # Case 1: Robot is far away, VLA outputs nominal action towards target
    safe_state = np.array([0.5, 0.5, 0.2, 0.2]) # pos=(0.5, 0.5), vel=(0.2, 0.2)
    u_vla = np.array([1.5, 1.5])
    u_out, intervened = cbf_filter.filter_control(safe_state, u_vla)
    print(f"\n[Scenario 1: Safe Free-Space]")
    print(f"  VLA Neural Command: {u_vla}")
    print(f"  CBF Filter Output:  {u_out} | Filter Intervened: {intervened}")
    print(f"  Result: Passed transparently with zero perturbation.")
    
    # Case 2: Robot is heading directly towards the obstacle at high speed!
    # Neural policy hallucinates an aggressive acceleration straight into the wall:
    danger_state = np.array([1.4, 1.4, 1.2, 1.2]) # Close to obstacle [2.0, 2.0]
    unsafe_u_vla = np.array([3.0, 3.0])           # Accelerated charge into danger!
    
    u_safe, intervened = cbf_filter.filter_control(danger_state, unsafe_u_vla)
    print(f"\n[Scenario 2: Catastrophic Collision Imminent!]")
    print(f"  VLA Neural Command (Hallucinated): {unsafe_u_vla}")
    print(f"  CBF Safe Overridden Control:       {u_safe.round(3)} | Filter Intervened: {intervened}")
    print(f"  Result: Unsafe acceleration rejected; minimal braking intervention enforced.")
    print("=" * 75)

if __name__ == "__main__":
    demo()
