"""Step 1: Clip all synthetic datasets to original data min/max ranges."""
import pandas as pd
import numpy as np
import glob
import os

# Load original dataset to get exact min/max
real = pd.read_csv("D:/aero/aerospace_structural_design_dataset.csv")

# Build exact bounds from real data
NUMERIC_COLS = [
    "E (GPa)", "ν", "ρ (kg/m³)", "Tensile Strength (MPa)", "Young's Modulus",
    "Altitude (m)", "Temperature (°C)", "Pressure (Pa)", "Operational Life (years)",
    "Wing Span (m)", "Fuselage Length (m)", "Structural Thickness (mm)",
    "Number of Iterations", "Optimization Time (sec)"
]
INT_COLS = ["Operational Life (years)", "Number of Iterations"]

bounds = {}
for col in NUMERIC_COLS:
    if col in real.columns:
        bounds[col] = (real[col].min(), real[col].max())
        print(f"  {col}: [{bounds[col][0]:.6f}, {bounds[col][1]:.6f}]")

# Collect all CSVs to process
targets = []
base = "D:/aero/final_LnT"
for pattern in [
    "synthetic_data/best_per_model/*.csv",
    "synthetic_data/top_10/*.csv",
    "synthetic_data/experimentations/*.csv",
    "edge_cases/*.csv",
    "class_balanced/**/*.csv",
]:
    targets.extend(glob.glob(os.path.join(base, pattern), recursive=True))

# Exclude non-data CSVs (index files, metrics files)
EXCLUDE = [
    "top_10.csv", "experimentation_results.csv", "edge_case_metrics.csv",
    "balancing_evaluation.csv", "graph_catalog.csv", "anomaly_summary.csv",
    "discriminator_metrics.csv", "mmd_scores_all.csv", "mmd_pivot.csv",
]
targets = [t for t in targets if os.path.basename(t) not in EXCLUDE]

total_clipped = 0
files_modified = 0

for fpath in sorted(targets):
    try:
        df = pd.read_csv(fpath)
    except Exception as e:
        print(f"  SKIP (read error): {fpath} — {e}")
        continue
    
    file_clips = 0
    for col, (cmin, cmax) in bounds.items():
        if col not in df.columns:
            continue
        before = df[col].copy()
        df[col] = df[col].clip(lower=cmin, upper=cmax)
        n_clipped = (before != df[col]).sum()
        if n_clipped > 0:
            file_clips += n_clipped
    
    # Fix integer columns
    for col in INT_COLS:
        if col in df.columns:
            df[col] = df[col].round().astype(int)
    
    if file_clips > 0:
        df.to_csv(fpath, index=False)
        files_modified += 1
        total_clipped += file_clips
        print(f"  CLIPPED {file_clips:>5} values in {os.path.relpath(fpath, base)}")

print(f"\n=== DONE: {total_clipped} values clipped across {files_modified} files (out of {len(targets)} total) ===")
