import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def analyze_real_dataset(csv_path="aerospace_structural_design_dataset.csv", out_dir="final/graphs/data_understanding"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Load Data
    print(f"Loading {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Shape: {df.shape}")
    
    # Target variables
    targets = ["Vibration Damping", "Computational Time", "Weight Efficiency", "Durability"]
    
    # Separate numeric and categorical
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    features = [c for c in df.columns if c not in targets]
    
    # 2. Extract Feature Importance for each target
    print("\n--- Extracting Baseline Feature Importance ---")
    
    # Encode categoricals for Random Forest
    df_encoded = df.copy()
    le_dict = {}
    for col in cat_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        le_dict[col] = le
        
    X = df_encoded[features]
    
    importance_dict = {}
    
    for t in targets:
        y = df_encoded[t]
        # Train RF to find what drives this target
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        importances = rf.feature_importances_
        
        # Sort and store top 5
        indices = np.argsort(importances)[::-1]
        top_features = [(features[i], importances[i]) for i in indices[:5]]
        importance_dict[t] = top_features
        
        print(f"\nTarget: {t}")
        for i, (feat, imp) in enumerate(top_features):
            print(f"  {i+1}. {feat}: {imp:.4f}")
            
    # Save a heatmap of all feature importances
    plt.figure(figsize=(10, 8))
    full_imp = np.zeros((len(features), len(targets)))
    for j, t in enumerate(targets):
        y = df_encoded[t]
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        full_imp[:, j] = rf.feature_importances_
        
    imp_df = pd.DataFrame(full_imp, index=features, columns=targets)
    sns.heatmap(imp_df, cmap='YlGnBu', annot=True, fmt='.2f')
    plt.title("Real Data: Feature Importance for Targets")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/baseline_feature_importance.png")
    plt.close()
    
    # 3. Analyze Key Physical Correlations
    print("\n--- Analyzing Physical Correlations ---")
    # Group by Material Type to see physical bounds
    mat_stats = df.groupby('Material Type')[['E (GPa)', 'ρ (kg/m³)', 'Tensile Strength (MPa)']].agg(['min', 'max', 'mean']).round(1)
    print("\nMaterial Physical Bounds:")
    print(mat_stats)
    
    # Analyze Altitude vs Temp/Pressure
    alt_corr = df[['Altitude (m)', 'Temperature (°C)', 'Pressure (Pa)']].corr()
    print("\nAltitude Correlations:")
    print(alt_corr)
    
    print(f"\nSaved baselines to {out_dir}/")
    return importance_dict, mat_stats

if __name__ == "__main__":
    analyze_real_dataset()
