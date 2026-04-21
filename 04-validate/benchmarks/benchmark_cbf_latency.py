"""
Physical AI Atlas — CBF QP Solve-Time Latency Benchmark
========================================================
Measures actual Control Barrier Function QP solve times on this hardware
to determine whether 1 kHz safety-loop operation is feasible.

Methodology:
    1. Generates 10,000 random robot states within workspace bounds
    2. Generates random nominal actions (some intentionally unsafe)
    3. Solves the CBF-QP for each (state, action) pair via SLSQP
    4. Reports p50, p95, p99, max latency in microseconds
    5. Determines 1 kHz feasibility (p99 < 1000 µs)

The CBF-QP being solved:
    u* = argmin_u  ||u - u_nominal||^2
    s.t.  h(x + u) >= 0           (barrier function non-negativity)
    
    where h(x) = min(distance to each workspace boundary - safety_margin)

Usage:
    python benchmark_cbf_latency.py
    python benchmark_cbf_latency.py --iterations 50000 --save results.json

Dependencies:
    numpy, scipy
"""

import argparse
import json
import platform
import sys
import time
from typing import List, Tuple

import numpy as np
from scipy.optimize import minimize

# ─────────────────────────────────────────────────────────────────────
#  Workspace & Safety Parameters
# ─────────────────────────────────────────────────────────────────────

WORKSPACE_BOUNDS = (-0.5, -0.5, 0.0, 0.5, 0.5, 0.6)  # meters
SAFETY_MARGIN = 0.05  # meters
CBF_ALPHA = 1.0
DT = 0.001  # 1 kHz target


def barrier_function(pos: np.ndarray) -> float:
    """h(x) = min distance to workspace boundary (with safety margin)."""
    b = WORKSPACE_BOUNDS
    m = SAFETY_MARGIN
    return float(np.min([
        pos[0] - (b[0] + m),
        (b[3] - m) - pos[0],
        pos[1] - (b[1] + m),
        (b[4] - m) - pos[1],
        pos[2] - (b[2] + m),
        (b[5] - m) - pos[2],
    ]))


def solve_cbf_qp(current_pos: np.ndarray, 
                  nominal_action: np.ndarray) -> Tuple[np.ndarray, float, bool]:
    """
    Solve the CBF-QP and return (safe_action, solve_time_us, was_modified).
    """
    t_start = time.perf_counter()
    
    next_pos = current_pos + nominal_action
    h_next = barrier_function(next_pos)
    h_current = barrier_function(current_pos)
    
    # Check if CBF constraint is already satisfied
    h_dot = (h_next - h_current) / DT
    if h_dot >= -CBF_ALPHA * h_current and h_next >= 0:
        solve_time_us = (time.perf_counter() - t_start) * 1e6
        return nominal_action, solve_time_us, False
    
    # Solve QP
    def objective(u):
        return np.sum((u - nominal_action)**2)
    
    def constraint(u):
        return barrier_function(current_pos + u)
    
    result = minimize(
        objective,
        x0=nominal_action * 0.5,
        method='SLSQP',
        constraints={'type': 'ineq', 'fun': constraint},
        bounds=[
            (nominal_action[0] - 0.1, nominal_action[0] + 0.1),
            (nominal_action[1] - 0.1, nominal_action[1] + 0.1),
            (nominal_action[2] - 0.1, nominal_action[2] + 0.1),
        ],
        options={'maxiter': 50, 'ftol': 1e-8}
    )
    
    solve_time_us = (time.perf_counter() - t_start) * 1e6
    
    if result.success:
        return result.x, solve_time_us, True
    else:
        return np.zeros(3), solve_time_us, True


def run_benchmark(n_iterations: int = 10000, seed: int = 2026,
                  save_path: str = None):
    """Run the full CBF latency benchmark."""
    
    rng = np.random.default_rng(seed)
    
    print("=" * 70)
    print("  Physical AI Atlas — CBF QP Solve-Time Latency Benchmark")
    print("=" * 70)
    print(f"  Hardware:       {platform.processor() or platform.machine()}")
    print(f"  OS:             {platform.system()} {platform.release()}")
    print(f"  Python:         {platform.python_version()}")
    print(f"  Iterations:     {n_iterations:,}")
    print(f"  Seed:           {seed}")
    print(f"  QP Solver:      scipy.optimize.minimize (SLSQP)")
    print(f"  Safety Margin:  {SAFETY_MARGIN*100:.0f} cm")
    print(f"  Target Loop:    1 kHz ({DT*1000:.0f} ms budget)")
    print("-" * 70)
    
    solve_times_safe: List[float] = []      # CBF not triggered
    solve_times_override: List[float] = []  # CBF override needed
    solve_times_all: List[float] = []
    
    n_overrides = 0
    
    for i in range(n_iterations):
        # Generate random state (biased toward boundaries for stress testing)
        b = WORKSPACE_BOUNDS
        if rng.random() < 0.4:
            # 40% of states near boundaries (stress test)
            axis = rng.integers(0, 3)
            pos = rng.uniform(
                [b[0] + 0.05, b[1] + 0.05, b[2] + 0.05],
                [b[3] - 0.05, b[4] - 0.05, b[5] - 0.05]
            )
            if rng.random() < 0.5:
                pos[axis] = b[axis] + SAFETY_MARGIN + rng.uniform(0, 0.05)
            else:
                pos[axis] = b[axis + 3] - SAFETY_MARGIN - rng.uniform(0, 0.05)
        else:
            pos = rng.uniform(
                [b[0] + 0.1, b[1] + 0.1, b[2] + 0.1],
                [b[3] - 0.1, b[4] - 0.1, b[5] - 0.1]
            )
        
        # Generate action (some intentionally toward boundary)
        action = rng.standard_normal(3) * 0.05
        if rng.random() < 0.3:
            # 30% of actions intentionally push toward nearest boundary
            nearest_axis = np.argmin([
                pos[0] - b[0], b[3] - pos[0],
                pos[1] - b[1], b[4] - pos[1],
                pos[2] - b[2], b[5] - pos[2],
            ])
            boundary_axis = nearest_axis // 2
            direction = -1 if nearest_axis % 2 == 0 else 1
            action[boundary_axis] = direction * 0.08
        
        _, solve_time, was_modified = solve_cbf_qp(pos, action)
        solve_times_all.append(solve_time)
        
        if was_modified:
            solve_times_override.append(solve_time)
            n_overrides += 1
        else:
            solve_times_safe.append(solve_time)
        
        # Progress
        if (i + 1) % 2500 == 0:
            print(f"  Progress: {i+1:,}/{n_iterations:,} "
                  f"({100*(i+1)/n_iterations:.0f}%) "
                  f"| Overrides: {n_overrides:,}")
    
    # Compute statistics
    all_arr = np.array(solve_times_all)
    
    stats = {
        "total_iterations": n_iterations,
        "n_overrides": n_overrides,
        "override_rate": n_overrides / n_iterations,
        "p50_us": float(np.percentile(all_arr, 50)),
        "p90_us": float(np.percentile(all_arr, 90)),
        "p95_us": float(np.percentile(all_arr, 95)),
        "p99_us": float(np.percentile(all_arr, 99)),
        "max_us": float(np.max(all_arr)),
        "mean_us": float(np.mean(all_arr)),
        "std_us": float(np.std(all_arr)),
    }
    
    if solve_times_safe:
        safe_arr = np.array(solve_times_safe)
        stats["safe_p50_us"] = float(np.percentile(safe_arr, 50))
        stats["safe_p99_us"] = float(np.percentile(safe_arr, 99))
    
    if solve_times_override:
        override_arr = np.array(solve_times_override)
        stats["override_p50_us"] = float(np.percentile(override_arr, 50))
        stats["override_p99_us"] = float(np.percentile(override_arr, 99))
    
    feasible_1khz = stats["p99_us"] < 1000
    
    # Print results
    print("=" * 70)
    print("  BENCHMARK RESULTS")
    print("-" * 70)
    print(f"  Total Iterations:   {n_iterations:,}")
    print(f"  Override Rate:      {stats['override_rate']*100:.1f}% "
          f"({n_overrides:,}/{n_iterations:,})")
    print()
    print(f"  {'Metric':<22} {'All (µs)':>12} {'Safe (µs)':>12} {'Override (µs)':>14}")
    print(f"  {'-'*22} {'-'*12} {'-'*12} {'-'*14}")
    print(f"  {'p50 (median)':<22} {stats['p50_us']:>12.1f} "
          f"{stats.get('safe_p50_us', 0):>12.1f} "
          f"{stats.get('override_p50_us', 0):>14.1f}")
    print(f"  {'p90':<22} {stats['p90_us']:>12.1f}")
    print(f"  {'p95':<22} {stats['p95_us']:>12.1f}")
    print(f"  {'p99':<22} {stats['p99_us']:>12.1f} "
          f"{stats.get('safe_p99_us', 0):>12.1f} "
          f"{stats.get('override_p99_us', 0):>14.1f}")
    print(f"  {'max':<22} {stats['max_us']:>12.1f}")
    print(f"  {'mean ± std':<22} {stats['mean_us']:>7.1f} ± {stats['std_us']:.1f}")
    print()
    print(f"  1 kHz FEASIBILITY:   {'✓ YES' if feasible_1khz else '✗ NO'} "
          f"(p99 = {stats['p99_us']:.0f} µs {'<' if feasible_1khz else '>='} 1000 µs budget)")
    
    if feasible_1khz:
        headroom = (1000 - stats['p99_us']) / 1000 * 100
        print(f"  Headroom:            {headroom:.0f}% of 1 ms budget remaining at p99")
    
    print("=" * 70)
    
    # Save results
    if save_path:
        full_results = {
            "benchmark": "CBF QP Solve-Time Latency",
            "hardware": platform.processor() or platform.machine(),
            "os": f"{platform.system()} {platform.release()}",
            "python": platform.python_version(),
            "solver": "scipy SLSQP",
            "seed": seed,
            **stats,
            "feasible_1khz": feasible_1khz,
        }
        with open(save_path, 'w') as f:
            json.dump(full_results, f, indent=2)
        print(f"\n  Results saved to: {save_path}")
    
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Physical AI Atlas — CBF QP Latency Benchmark"
    )
    parser.add_argument("--iterations", type=int, default=10000,
                        help="Number of QP solves (default: 10000)")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--save", type=str, default=None,
                        help="Save results to JSON file")
    
    args = parser.parse_args()
    run_benchmark(args.iterations, args.seed, args.save)
