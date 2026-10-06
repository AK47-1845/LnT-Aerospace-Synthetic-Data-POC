import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import shutil

def generate_graphs():
    df = pd.read_csv("d:/aero/deliverables/03_data/all_metrics_72runs.csv")
    out_dir = "d:/aero/deliverables/02_graphs"
    
    # 6-color palette
    palette = sns.color_palette("husl", 6)
    
    # A1. Composite Score ranking
    plt.figure(figsize=(10, 6))
    summary = df.groupby('Model')['Composite Score'].agg(['mean', 'std']).sort_values('mean', ascending=False)
    ax = sns.barplot(x=summary.index, y='mean', data=summary.reset_index(), palette=palette, capsize=0.1)
    ax.errorbar(x=range(len(summary)), y=summary['mean'], yerr=summary['std'], fmt='none', c='black')
    for i, v in enumerate(summary['mean']):
        ax.text(i, v + 0.02, f"{v:.3f}", ha='center')
    plt.title("Model Performance Ranking (Mean Composite Score +/- Std Dev)", fontweight='bold', fontsize=14)
    plt.ylabel("Composite Score")
    plt.ylim(0, 1.1)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/A_model_comparison/composite_score_ranking.png", dpi=150)
    plt.close()
    
    # B1. Line chart — Composite Score vs Generation Size
    plt.figure(figsize=(12, 7))
    sns.lineplot(data=df, x='Size', y='Composite Score', hue='Model', marker='o', palette=palette)
    plt.title("Composite Score vs Generation Size", fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/B_scale_analysis/composite_vs_size.png", dpi=150)
    plt.close()

    # B4. Physics vs Stats scatter
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Physics Consistency', y='Statistical Similarity', hue='Model', size='Size', sizes=(20, 200), palette=palette, alpha=0.7)
    plt.title("Physics Consistency vs Statistical Similarity", fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/B_scale_analysis/physics_vs_statistical_scatter.png", dpi=150)
    plt.close()
    
    # C3. Copy existing KDE curves from explainability as "C3" requirements
    exp_dir = "d:/aero/explainability/20260315_100903/visual_examples"
    dest_c_dir = f"{out_dir}/C_statistical"
    if os.path.exists(exp_dir):
        for f in os.listdir(exp_dir):
            if f.endswith(".png"):
                shutil.copy2(os.path.join(exp_dir, f), os.path.join(dest_c_dir, f))
                
    # Copy correlation
    exp_graphs = "d:/aero/explainability/20260315_100903/graphs"
    if os.path.exists(exp_graphs):
        for f in os.listdir(exp_graphs):
            if f.startswith("corr_diff") and f.endswith(".png"):
                shutil.copy2(os.path.join(exp_graphs, f), os.path.join(dest_c_dir, f))
                
    print("Graphs generated and copied to deliverables/02_graphs.")

generate_graphs()
