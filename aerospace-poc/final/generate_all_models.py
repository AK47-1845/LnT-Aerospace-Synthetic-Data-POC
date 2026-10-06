import os
import sys
import pandas as pd
import numpy as np

# Add parent directory to path to import main/models_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import prepare_data
from models_engine import UnifiedModelWrapper

def main():
    print("Preparing dataset info...")
    dataset_info = prepare_data()
    out_dir = r"d:\aero\final\per_model_datasets"
    os.makedirs(out_dir, exist_ok=True)
    
    # Run TVAE and CTGAN with reasonable epochs
    models_to_run = {
        "TVAE": {"latent_dim": 128, "epochs": 500},
        "CTGAN": {"epochs": 600, "batch_size": 64, "embedding_dim": 128}
    }
    
    sizes = [300, 600, 1000]
    
    for model_name, params in models_to_run.items():
        print(f"\n--- Initializing {model_name} ---")
        wrapper = UnifiedModelWrapper(model_name, params, dataset_info)
        
        print(f"Fitting {model_name}...")
        wrapper.fit()
        
        for size in sizes:
            out_path = os.path.join(out_dir, f"{model_name.lower()}_{size}.csv")
            if os.path.exists(out_path):
                print(f"Skipping {model_name} size {size}, already derived.")
                continue
                
            print(f"Generating {size} rows for {model_name}...")
            # generate() expects an integer
            syn_df = wrapper.generate(n_samples=size)
            
            # Post-process bounds since genuity doesn't always clip perfectly
            numeric_cols = syn_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col in dataset_info['df_raw']:
                    real_min = dataset_info['df_raw'][col].min()
                    real_max = dataset_info['df_raw'][col].max()
                    syn_df[col] = syn_df[col].clip(real_min, real_max)
                    
            syn_df.to_csv(out_path, index=False)
            print(f"Saved {out_path}")

    print("\nGeneration complete.")

if __name__ == "__main__":
    main()
