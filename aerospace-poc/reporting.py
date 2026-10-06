import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches, Pt
from utils import logger
from config import DIRS

def create_client_slides(output_path, run_metadata, best_model, best_score, significance):
    """ Generates a 5-slide Executive PowerPoint presentation """
    prs = Presentation()
    
    # 1. Title
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Synthetic Data Edge-Case Orchestration Final Report"
    slide.placeholders[1].text = f"Timestamp: {run_metadata.get('timestamp')}\nWinning Model: {best_model}"
    
    # 2. Executive Summary
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Executive Summary"
    tf = slide.placeholders[1].text_frame
    tf.text = f"Best Performing AI Model: {best_model}"
    p = tf.add_paragraph()
    p.text = f"Composite Physics/Utility Score: {best_score:.4f} / 1.0"
    p.level = 1
    p = tf.add_paragraph()
    sig_text = "Statistically Significant difference versus baselines." if significance else "No statistically significant separation from baselines."
    p.text = f"Statistical Note: {sig_text}"
    p.level = 1
    
    # 3. Physics Constraints
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Physics Checks & Auto-Repair Insights"
    tf = slide.placeholders[1].text_frame
    tf.text = "A 6-rule physics engine evaluated all geometries and properties."
    p = tf.add_paragraph()
    p.text = "Hard Checks: Fatigue < Tensile, Yield < Tensile, Densities in bounds."
    p.level = 1
    
    # 4. Edge-Case Coverage
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Edge-Case Coverage & Provenance"
    tf = slide.placeholders[1].text_frame
    tf.text = "Rigorous enumeration of 0.01 / 0.99 quantiles and <0.5% categories."
    p = tf.add_paragraph()
    p.text = "Conditional Fallback Generative Engine ensured all minimum targets were met via perturbation."
    p.level = 1
    
    # 5. Risks & Limitations
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Risks & Assumptions"
    tf = slide.placeholders[1].text_frame
    tf.text = "Residual Risks & Limitations:"
    p = tf.add_paragraph()
    p.text = "1. Edge-case conditional generation relies on real-data neighborhoods."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "2. Composite scores implicitly weight physics and ML utility."
    p.level = 1
    
    prs.save(output_path)
    logger.info(f"Saved client PPTX to {output_path}")

def generate_visuals(real_df, synth_df, model_name, suffix=""):
    """ Core histograms and correlation heatmaps """
    num_cols = real_df.select_dtypes(include=[np.number]).columns[:4]
    
    # Distributions
    for col in num_cols:
        plt.figure(figsize=(10,6))
        sns.histplot(real_df[col], color="blue", label="Real", kde=True, alpha=0.5, stat='density')
        sns.histplot(synth_df[col], color="orange", label="Synthetic", kde=True, alpha=0.5, stat='density')
        plt.title(f"{model_name} | {col} Distribution")
        plt.legend()
        path = os.path.join(DIRS['visuals'], f"dist_{model_name}_{col.replace(' ', '_')}_{suffix}.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()
        
    # Corr Matrix Diff
    if len(num_cols) > 1:
        corr_r = real_df[num_cols].corr()
        corr_s = synth_df[num_cols].corr()
        diff = corr_r - corr_s
        
        plt.figure(figsize=(10,8))
        sns.heatmap(diff, cmap="bwr", center=0, annot=True)
        plt.title(f"{model_name} | Correlation Difference (Real - Synth)")
        path = os.path.join(DIRS['visuals'], f"corr_diff_{model_name}_{suffix}.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()

def build_html_report(best_model, metrics_df, metadata, edge_case_df):
    """ Massive interactive HTML export covering physics, edge cases, and benchmarks """
    html = f"""
    <html>
    <head>
        <title>Synthetic Data Benchmark</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    </head>
    <body class="container mt-4">
        <h1 class="mb-4">Orchestration Exec Memo</h1>
        <div class="alert alert-primary">
            <h4>TL;DR</h4>
            <ul>
                <li><strong>Best Model:</strong> {best_model}</li>
                <li><strong>Composite Score:</strong> {metrics_df.loc[metrics_df['Model'] == best_model, 'composite_score'].values[0]:.4f}</li>
                <li><strong>Physics Enforced:</strong> 6-layer bounds logic.</li>
            </ul>
        </div>
        
        <h2 class="mt-4">Leaderboard</h2>
        {metrics_df.sort_values(by="composite_score", ascending=False).to_html(classes='table table-striped table-hover mt-2')}
        
        <h2 class="mt-4">Edge-Case Coverage</h2>
        <p>Enumerating all >Q99, <Q01, and <0.5% levels.</p>
        {edge_case_df.head(20).to_html(classes='table table-sm')}
        
        <h2 class="mt-4">Metadata / Provenance</h2>
        <pre>{json.dumps(metadata, indent=2)}</pre>
    </body>
    </html>
    """
    path = os.path.join(DIRS['signoff'], "DETAILED_REPORT.html")
    with open(path, "w", encoding='utf-8') as f:
        f.write(html)
    logger.info(f"Saved Executive HTML Report to {path}")
