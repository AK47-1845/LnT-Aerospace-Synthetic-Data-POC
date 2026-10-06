"""
Build final_LnT/synthetic_data/ folder structure.
- experimentations/  : experimentation_results.csv + all 91 synthetic CSVs
- top_10/           : top_10.csv + 10 best synthetic CSVs
"""

import os, shutil, pandas as pd

# ── Paths ────────────────────────────────────────────────────────────────────
FINAL       = "D:/aero/final"
ART1        = "D:/aero/artifacts/experiments/20260315_094221/synth_datasets"
ART2        = "D:/aero/artifacts/experiments/20260315_100903/synth_datasets"
PER_MODEL   = "D:/aero/final/per_model_datasets"
EXP_CSV     = f"{FINAL}/experiments/experimentation_results.csv"
OUT_BASE    = "D:/aero/final_LnT/synthetic_data"
EXP_OUT     = f"{OUT_BASE}/experimentations"
TOP10_OUT   = f"{OUT_BASE}/top_10"

os.makedirs(EXP_OUT,   exist_ok=True)
os.makedirs(TOP10_OUT, exist_ok=True)

# ── Load experiment results ───────────────────────────────────────────────────
df = pd.read_csv(EXP_CSV)
print(f"Loaded experimentation_results.csv: {len(df)} rows")

# ── Row → source-file mapping ────────────────────────────────────────────────
# Strategy per model:
#   Copula rows 0-11   → ART1  synthetic_Copula_{seed}_{size}_best.csv
#   GMM    rows 12-23  → ART2  synthetic_GMM_{seed}_{size}_best.csv
#   KDE    rows 24-35  → ART1  synthetic_KDE_{seed}_{size}_best.csv
#   MaskedPredictor 36-47 → ART1 synthetic_MaskedPredictor_{seed}_{size}_best.csv
#   TabuDiff 48-59     → ART1  synthetic_TabuDiff_{seed}_{size}_best.csv
#   Copula rows 60-65  → PER_MODEL  copula_s{seed}_n{size}.csv  (or _r01 dup)
#   TabuDiff rows 66-74→ PER_MODEL  tabudiff_s{seed}_n{size}.csv
#   TabuDiffPremium 75-76→PER_MODEL tabudiff_premium_s{seed}_n1000.csv
#   MaskedPredictor 77-81→PER_MODEL masked_s{seed}_n{size}.csv
#   TVAE 82-86         → PER_MODEL  tvae_s{seed}_n{size}.csv
#   TVAEPremium 87     → PER_MODEL  tvae_premium_s11_n1000.csv
#   CTGANPremium 88-90 → PER_MODEL  ctgan_premium_s{seed}_n1000.csv

def resolve_source(idx, model, seed, size):
    seed, size = int(seed), int(size)

    # ── Artifact-backed rows (0-59) ──────────────────────────────────────────
    if idx <= 11:          # Copula original 72-run
        return f"{ART1}/synthetic_Copula_{seed}_{size}_best.csv"
    if 12 <= idx <= 23:    # GMM
        return f"{ART2}/synthetic_GMM_{seed}_{size}_best.csv"
    if 24 <= idx <= 35:    # KDE
        return f"{ART1}/synthetic_KDE_{seed}_{size}_best.csv"
    if 36 <= idx <= 47:    # MaskedPredictor original 72-run
        return f"{ART1}/synthetic_MaskedPredictor_{seed}_{size}_best.csv"
    if 48 <= idx <= 59:    # TabuDiff original 72-run
        return f"{ART1}/synthetic_TabuDiff_{seed}_{size}_best.csv"

    # ── Final-run rows (60+) ─────────────────────────────────────────────────
    if model == "Copula":
        # handle duplicate row 63/64 (both s42 n1000)
        base = f"{PER_MODEL}/copula_s{seed}_n{size}.csv"
        if idx == 64:
            base = f"{PER_MODEL}/copula_s42_n1000_r01.csv"
        return base
    if model == "TabuDiff":
        return f"{PER_MODEL}/tabudiff_s{seed}_n{size}.csv"
    if model == "TabuDiffPremium":
        return f"{PER_MODEL}/tabudiff_premium_s{seed}_n1000.csv"
    if model == "MaskedPredictor":
        return f"{PER_MODEL}/masked_s{seed}_n{size}.csv"
    if model == "TVAE":
        return f"{PER_MODEL}/tvae_s{seed}_n{size}.csv"
    if model == "TVAEPremium":
        return f"{PER_MODEL}/tvae_premium_s11_n1000.csv"
    if model == "CTGANPremium":
        return f"{PER_MODEL}/ctgan_premium_s{seed}_n1000.csv"

    raise ValueError(f"Unknown model at row {idx}: {model}")

# ── Standardised destination filename ────────────────────────────────────────
def dest_name(idx, model, seed, size):
    model_safe = model.replace(" ", "_")
    suffix = f"_r{idx:03d}" if idx == 64 else ""   # disambiguate the duplicate
    return f"{model_safe}_s{int(seed)}_n{int(size)}{suffix}.csv"

# ── Copy all files + track what went where ───────────────────────────────────
df["_src_file"] = None
df["_dest_file"] = None
missing = []

for idx, row in df.iterrows():
    model, seed, size = row["Model"], row["Seed"], row["Size"]
    src  = resolve_source(idx, model, seed, size)
    name = dest_name(idx, model, seed, size)
    dst  = f"{EXP_OUT}/{name}"

    if os.path.exists(src):
        shutil.copy2(src, dst)
        df.at[idx, "_src_file"]  = src
        df.at[idx, "_dest_file"] = name
        print(f"  [{idx:02d}] {name}")
    else:
        missing.append((idx, model, seed, size, src))
        df.at[idx, "_dest_file"] = "MISSING"
        print(f"  [{idx:02d}] MISSING: {src}")

# ── Save experimentation_results.csv (clean copy, no internal cols) ──────────
export_df = df.drop(columns=["_src_file", "_dest_file"])
export_df.to_csv(f"{EXP_OUT}/experimentation_results.csv", index=False)
print(f"\nSaved experimentation_results.csv to {EXP_OUT}/")

# ── Top 10 ───────────────────────────────────────────────────────────────────
top10 = df[df["_dest_file"] != "MISSING"] \
          .nlargest(10, "Composite Score") \
          .copy()

top10_clean = top10.drop(columns=["_src_file", "_dest_file"])
top10_clean.to_csv(f"{TOP10_OUT}/top_10.csv", index=False)
print(f"\nTop 10 by Composite Score:")
print(top10[["Model","Seed","Size","Composite Score","_dest_file"]].to_string())

for _, row in top10.iterrows():
    src_name = row["_dest_file"]
    src_path = f"{EXP_OUT}/{src_name}"
    dst_path = f"{TOP10_OUT}/{src_name}"
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"  → copied {src_name}")
    else:
        print(f"  !! cannot copy {src_name} (not in experimentations/)")

# ── Summary ──────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"Experimentations/ : {len(df) - len(missing)} CSVs + experimentation_results.csv")
print(f"Top10/            : top_10.csv + 10 CSVs")
if missing:
    print(f"\nMISSING ({len(missing)}):")
    for m in missing:
        print(f"  row={m[0]} model={m[1]} seed={m[2]} size={m[3]}")
        print(f"    {m[4]}")
