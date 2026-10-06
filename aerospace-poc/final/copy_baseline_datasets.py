import os
import glob
import shutil

src_dir = r"d:\aero\artifacts\experiments\20260315_100903\synth_datasets"
dest_dir = r"d:\aero\final\per_model_datasets"
os.makedirs(dest_dir, exist_ok=True)

models = ['Empirical', 'KDE', 'GMM', 'Copula', 'TabuDiff']

for size in [300, 600, 1000]:
    for model in models:
        # Best ones were usually seed 11 except varying for TabuDiff occasionally
        pattern = f"{src_dir}/synth_{model}_seed*_n{size}.csv"
        files = glob.glob(pattern)
        if files:
            src = files[0] # Just take the first one found (ideally seed 11)
            dest = os.path.join(dest_dir, f"{model.lower()}_{size}.csv")
            shutil.copy2(src, dest)
            print(f"Copied {os.path.basename(src)} -> {model.lower()}_{size}.csv")
        else:
            print(f"MISSING: {model} {size}")
