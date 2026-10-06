import os

base_dir = "d:/aero/deliverables"

folders = [
    os.path.join(base_dir, "01_reports"),
    os.path.join(base_dir, "02_graphs/A_model_comparison"),
    os.path.join(base_dir, "02_graphs/B_scale_analysis"),
    os.path.join(base_dir, "02_graphs/C_statistical"),
    os.path.join(base_dir, "02_graphs/D_summary"),
    os.path.join(base_dir, "03_data"),
    os.path.join(base_dir, "04_benchmarks"),
    os.path.join(base_dir, "05_notebooks"),
]

for f in folders:
    os.makedirs(f, exist_ok=True)

print("Created deliverables folder structure.")
