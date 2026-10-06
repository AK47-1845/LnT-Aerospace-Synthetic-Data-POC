import pandas as pd
import numpy as np
from config import PHYSICS_RANGES, CONSTANTS
from utils import logger

def derive_physics_features(df):
    """
    Computes derived physical features for the aerospace dataset.
    Features: specific_stiffness, specific_strength, buckling_resistance_index,
    elastic_energy_capacity, fatigue_resistance_ratio, stress_safety_factor.
    """
    logger.info("Deriving physics features...")
    df = df.copy()
    
    # Extract constants if needed
    g = CONSTANTS["gravitational_acceleration"]
    
    # 1. specific_stiffness = youngs_modulus / density
    if 'Youngs Modulus' in df.columns and 'Density' in df.columns:
        df['specific_stiffness'] = df['Youngs Modulus'] / df['Density']
        
    # 2. specific_strength = tensile_strength / density
    if 'Tensile Strength' in df.columns and 'Density' in df.columns:
        df['specific_strength'] = df['Tensile Strength'] / df['Density']
        
    # 3. buckling_resistance_index = youngs_modulus * (structural_thickness ** 2)
    if 'Youngs Modulus' in df.columns and 'Structural Thickness' in df.columns:
        df['buckling_resistance_index'] = df['Youngs Modulus'] * (df['Structural Thickness'] ** 2)
        
    # 4. elastic_energy_capacity = (tensile_strength ** 2) / youngs_modulus
    if 'Tensile Strength' in df.columns and 'Youngs Modulus' in df.columns:
        df['elastic_energy_capacity'] = (df['Tensile Strength'] ** 2) / df['Youngs Modulus']
        
    # 5. fatigue_resistance_ratio = fatigue_limit / tensile_strength
    if 'Fatigue Limit' in df.columns and 'Tensile Strength' in df.columns:
        df['fatigue_resistance_ratio'] = df['Fatigue Limit'] / df['Tensile Strength']

    # 6. stress_safety_factor = tensile_strength / applied_stress 
    # (Assuming we have Applied Stress or similar out of the 22 cols. If not, skip safely)
    if 'Tensile Strength' in df.columns and 'Applied Stress' in df.columns:
        df['stress_safety_factor'] = df['Tensile Strength'] / df['Applied Stress']
        
    # 7. optimization_convergence_rate = objective_improvement / number_of_iterations
    # We will compute if columns exist
    
    logger.info("Feature engineering complete.")
    return df

def apply_physics_repair(df):
    """
    Applies hard automated repair rules to violating synthetic data rows.
    Returns: repaired dataframe and the count of repairs made.
    """
    df_rep = df.copy()
    repair_count = 0
    
    # Rule A: fatigue_limit <= tensile_strength
    if 'Fatigue Limit' in df_rep.columns and 'Tensile Strength' in df_rep.columns:
        mask_a = df_rep['Fatigue Limit'] > df_rep['Tensile Strength']
        repairs_a = mask_a.sum()
        if repairs_a > 0:
            df_rep.loc[mask_a, 'Fatigue Limit'] = 0.85 * df_rep.loc[mask_a, 'Tensile Strength']
            repair_count += repairs_a
            
    # Rule B: yield_strength <= tensile_strength
    if 'Yield Strength' in df_rep.columns and 'Tensile Strength' in df_rep.columns:
        mask_b = df_rep['Yield Strength'] > df_rep['Tensile Strength']
        repairs_b = mask_b.sum()
        if repairs_b > 0:
            df_rep.loc[mask_b, 'Yield Strength'] = np.minimum(
                df_rep.loc[mask_b, 'Yield Strength'], 
                0.9 * df_rep.loc[mask_b, 'Tensile Strength']
            )
            repair_count += repairs_b

    # Rule C is soft (correlation) - no repair
    
    # Rule D: no negative densities, moduli, strengths
    cols_to_clip = ['Density', 'Youngs Modulus', 'Tensile Strength', 'Yield Strength', 'Fatigue Limit']
    for col in cols_to_clip:
        if col in df_rep.columns:
            mask_neg = df_rep[col] < 0
            repairs_neg = mask_neg.sum()
            if repairs_neg > 0:
                df_rep.loc[mask_neg, col] = 1e-6 # small positive
                repair_count += repairs_neg
                
    # Rule D (part 2): Known material range clipping
    if 'Density' in df_rep.columns and 'Material Type' in df_rep.columns:
        for mat, (d_min, d_max) in PHYSICS_RANGES.items():
            mask_mat = df_rep['Material Type'] == mat
            
            # Less than min
            mask_low = mask_mat & (df_rep['Density'] < d_min)
            rep_low = mask_low.sum()
            if rep_low > 0:
                df_rep.loc[mask_low, 'Density'] = d_min
                repair_count += rep_low
                
            # Greater than max
            mask_high = mask_mat & (df_rep['Density'] > d_max)
            rep_high = mask_high.sum()
            if rep_high > 0:
                df_rep.loc[mask_high, 'Density'] = d_max
                repair_count += rep_high

    # Rule F: categorical must be from original levels
    # Handled prior during generation clipping, but we can enforce 'OTHER' mapping here if needed.
    
    return df_rep, repair_count

def score_dataset_physics(df_real, df_synth):
    """
    Calculates the physics score 0-1 for the dataset.
    dataset_physics_score = 0.5 * per_row_physics_ok + 0.3 * correlation_consistency + 0.2 * range_validity
    """
    total_rows = len(df_synth)
    
    # 1. Per Row Physics OK (fraction of rows with FATIGUE <= TENSILE and YIELD <= TENSILE and DENSITY in bounds)
    ok_mask = np.ones(total_rows, dtype=bool)
    if 'Fatigue Limit' in df_synth.columns and 'Tensile Strength' in df_synth.columns:
        ok_mask &= (df_synth['Fatigue Limit'] <= df_synth['Tensile Strength'])
    if 'Yield Strength' in df_synth.columns and 'Tensile Strength' in df_synth.columns:
        ok_mask &= (df_synth['Yield Strength'] <= df_synth['Tensile Strength'])
    if 'Density' in df_synth.columns and 'Material Type' in df_synth.columns:
        for mat, (d_min, d_max) in PHYSICS_RANGES.items():
            mat_mask = df_synth['Material Type'] == mat
            bad_density = mat_mask & ((df_synth['Density'] < d_min) | (df_synth['Density'] > d_max))
            ok_mask &= ~bad_density
            
    per_row_ok = ok_mask.sum() / max(1, total_rows)
    
    # 2. Correlation Consistency (numeric only)
    num_cols = df_real.select_dtypes(include=[np.number]).columns.intersection(df_synth.select_dtypes(include=[np.number]).columns)
    if len(num_cols) > 1:
        corr_real = df_real[num_cols].corr().fillna(0).values
        corr_synth = df_synth[num_cols].corr().fillna(0).values
        # Mean absolute difference of correlation matrices
        mad_corr = np.mean(np.abs(corr_real - corr_synth))
        corr_consistency = max(0, 1 - mad_corr)
    else:
        corr_consistency = 1.0
        
    # 3. Range Validity (fraction of numeric cells within realistic bounds defined by real data)
    cells_valid = 0
    total_cells = 0
    for col in num_cols:
        cmin, cmax = df_real[col].min(), df_real[col].max()
        # allow 5% margin
        margin = (cmax - cmin) * 0.05
        lower, upper = cmin - margin, cmax + margin
        valid_mask = (df_synth[col] >= lower) & (df_synth[col] <= upper)
        cells_valid += valid_mask.sum()
        total_cells += total_rows
        
    range_validity = cells_valid / max(1, total_cells)
    
    dataset_physics_score = 0.5 * per_row_ok + 0.3 * corr_consistency + 0.2 * range_validity
    
    return dataset_physics_score, per_row_ok, corr_consistency, range_validity
