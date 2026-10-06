import pandas as pd
import numpy as np

def generate_synthetic_data(real_path, n_samples=300, noise_factor=0.01):
    """
    Generates synthetic target data by empirical resampling the real data
    and adding slight noise while maintaining strict physical categorical bounds.
    """
    df_real = pd.read_csv(real_path)
    
    # 1. Resample rows 
    df_syn = df_real.sample(n=n_samples, replace=True).reset_index(drop=True)
    
    # 2. Add continuous noise
    num_cols = df_real.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        std = df_real[col].std()
        noise = np.random.normal(0, std * noise_factor, size=n_samples)
        df_syn[col] = df_syn[col] + noise
        
    # 3. Clip back to real data bounds to prevent physical impossibilities
    for col in num_cols:
        r_min, r_max = df_real[col].min(), df_real[col].max()
        df_syn[col] = df_syn[col].clip(r_min, r_max)
        
    return df_syn

if __name__ == "__main__":
    print("Generating best 300-row synthetic aerospace dataset...")
    df = generate_synthetic_data('aerospace_structural_design_dataset.csv', n_samples=300)
    df.to_csv('synthetic_aerospace_data.csv', index=False)
    print("Saved as synthetic_aerospace_data.csv")
