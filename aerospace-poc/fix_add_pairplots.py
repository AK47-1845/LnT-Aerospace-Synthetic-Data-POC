"""Step 2: Generate real-vs-synthetic side-by-side pairplots."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid", font_scale=0.9)

real = pd.read_csv("D:/aero/aerospace_structural_design_dataset.csv")

# Select all numeric columns dynamically
NUMERIC_COLS = real.select_dtypes(include=[np.number]).columns.tolist()
# Top 5 by variance
top5 = real[NUMERIC_COLS].var().sort_values(ascending=False).head(5).index.tolist()
print(f"Top 5 features by variance: {top5}")

models = {
    "KDE": "D:/aero/final_LnT/synthetic_data/best_per_model/KDE_s123_n5000_r035.csv",
    "GMM": "D:/aero/final_LnT/synthetic_data/best_per_model/GMM_s42_n5000_r019.csv",
    "Copula": "D:/aero/final_LnT/synthetic_data/best_per_model/Copula_s11_n5000_r003.csv",
}

out_dir = "D:/aero/final_LnT/explainable_graphs/03_synthetic_vs_real"

for model_name, syn_path in models.items():
    print(f"Generating pairplot for {model_name}...")
    syn = pd.read_csv(syn_path)

    # Sample synthetic to match real size for fair visual
    syn_sample = syn.sample(n=min(len(real), len(syn)), random_state=42)

    real_sub = real[top5].copy()
    real_sub['Source'] = 'Real (300)'
    syn_sub = syn_sample[top5].copy()
    syn_sub['Source'] = f'Synthetic ({model_name})'

    combined = pd.concat([real_sub, syn_sub], ignore_index=True)

    palette = {'Real (300)': '#1B2A4A', f'Synthetic ({model_name})': '#ef4444'}

    g = sns.pairplot(
        combined, hue='Source', palette=palette,
        plot_kws={'alpha': 0.35, 's': 12, 'edgecolor': 'none'},
        diag_kind='kde', height=2.0,
        diag_kws={'linewidth': 1.5, 'fill': True, 'alpha': 0.3}
    )
    g.fig.suptitle(f'Joint Pair Plot \u2014 Real vs {model_name} Synthetic (Top 5 Features)',
                   y=1.02, fontsize=14, fontweight='bold')

    out_path = f"{out_dir}/pairplot_real_vs_{model_name.lower()}.png"
    g.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close('all')
    print(f"  Saved: {out_path}")

print("\n=== DONE: 3 pairplots generated ===")
