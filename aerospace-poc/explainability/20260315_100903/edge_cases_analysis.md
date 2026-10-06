# Edge Case Analysis & Implications

Edge case catalogues evaluate model capabilities in sparse, out-of-distribution, or boundary-terminating regions.

Review the `edge_case_catalog.csv` in `/artifacts/experiments/20260315_100903/edge_cases/`.

Models that heavily rely on Gaussian priors (GMM, KDE) often struggle with sharp, non-differentiable physics boundaries (like absolute zero or structural minimums), triggering high repair actions. Deep learning models like TabuDiff adapt better but can mode-collapse.

**Visual Examples**: Check visual folder thumbnails. 

For each feature (Altitude, Pressure, Tensile Strength), edge cases ensure no impossible planes are simulated.
