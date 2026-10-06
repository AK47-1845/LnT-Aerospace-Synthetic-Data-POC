# Edge Case Dataset Catalog
*Generated: 2026-03-17 23:28:32*

**Total scenarios:** 28  
**Rows per scenario:** 50  
**Total edge case rows:** 1400  

## Summary Table

| Scenario | Category | IF Anomaly % | LOF Anomaly % | NN Distance | Realism Score |
|---|---|---|---|---|---|
| low_durability_cluster | Target | 2.0% | 2.0% | 0.0361 | 98.1 |
| material_carbonfiber_only | Material | 2.0% | 2.0% | 0.0361 | 98.1 |
| temperature_moderate | Flight Envelope | 4.0% | 4.0% | 0.0362 | 96.9 |
| poor_weight_efficiency | Target | 4.0% | 4.0% | 0.0361 | 96.9 |
| shark_optimizer_only | Optimization | 4.0% | 4.0% | 0.036 | 96.9 |
| operational_life_long | Lifecycle | 6.0% | 4.0% | 0.036 | 96.3 |
| wingspan_extreme_large | Geometry | 6.0% | 6.0% | 0.0362 | 95.7 |
| altitude_extreme_high | Flight Envelope | 6.0% | 6.0% | 0.036 | 95.7 |
| material_aluminum_only | Material | 8.0% | 4.0% | 0.0362 | 95.7 |
| high_durability_cluster | Target | 10.0% | 4.0% | 0.0361 | 95.1 |
| pressure_extreme_low | Flight Envelope | 12.0% | 2.0% | 0.0358 | 95.1 |
| altitude_extreme_low | Flight Envelope | 8.0% | 10.0% | 0.0362 | 93.9 |
| operational_life_short | Lifecycle | 14.0% | 6.0% | 0.036 | 93.3 |
| material_titanium_only | Material | 10.0% | 10.0% | 0.0357 | 93.3 |
| tensile_extreme_low | Material | 20.0% | 2.0% | 0.0361 | 92.7 |
| modulus_extreme_high | Material | 16.0% | 6.0% | 0.0356 | 92.7 |
| pressure_extreme_high | Flight Envelope | 16.0% | 10.0% | 0.0362 | 91.5 |
| short_optimization | Optimization | 22.0% | 16.0% | 0.0358 | 87.9 |
| density_extreme_heavy | Material | 28.0% | 10.0% | 0.036 | 87.9 |
| tensile_extreme_high | Material | 28.0% | 12.0% | 0.036 | 87.3 |
| thickness_extreme_thick | Geometry | 22.0% | 18.0% | 0.036 | 87.3 |
| temperature_extreme_cold | Flight Envelope | 16.0% | 32.0% | 0.0359 | 84.9 |
| excellent_weight_efficiency | Target | 0.0% | 4.0% | 0.0361 | 83.1 |
| thickness_extreme_thin | Geometry | 4.0% | 0.0% | 0.0361 | 83.1 |
| chaotic_quantum_only | Optimization | 6.0% | 0.0% | 0.0361 | 82.5 |
| density_extreme_light | Material | 0.0% | 10.0% | 0.0362 | 81.3 |
| long_optimization | Optimization | 0.0% | 10.0% | 0.0362 | 81.3 |
| wingspan_extreme_small | Geometry | 0.0% | 0.0% | 0.0361 | 69.3 |

---

## Detailed Scenario Descriptions

### low_durability_cluster
**Category:** Target  
**N Rows:** 50  
**Description:** All Low-Durability configurations. Identifies input feature patterns associated with early structural degradation.  
**Realism Score:** 98.1 / 100  

### material_carbonfiber_only
**Category:** Material  
**N Rows:** 50  
**Description:** Carbon Fiber-only structure set. Highest specific stiffness — primary flight structures.  
**Realism Score:** 98.1 / 100  

### temperature_moderate
**Category:** Flight Envelope  
**N Rows:** 50  
**Description:** Temperature near mean (-50 degrees C). Nominal cruise temperature band.  
**Realism Score:** 96.9 / 100  

### poor_weight_efficiency
**Category:** Target  
**N Rows:** 50  
**Description:** All Poor Weight Efficiency rows. Overweight structural designs — candidates for optimization.  
**Realism Score:** 96.9 / 100  

### shark_optimizer_only
**Category:** Optimization  
**N Rows:** 50  
**Description:** Shark Optimizer algorithm only. Nature-inspired metaheuristic mimicking shark predation behavior.  
**Realism Score:** 96.9 / 100  

### operational_life_long
**Category:** Lifecycle  
**N Rows:** 50  
**Description:** Operational life 37-39 years. Long-service aircraft requiring enhanced fatigue analysis.  
**Realism Score:** 96.3 / 100  

### wingspan_extreme_large
**Category:** Geometry  
**N Rows:** 50  
**Description:** Wing span >56 m. Wide-body or UAV with high aspect ratio — maximum bending moment scenario.  
**Realism Score:** 95.7 / 100  

### altitude_extreme_high
**Category:** Flight Envelope  
**N Rows:** 50  
**Description:** Altitude at 95th percentile (>17,500 m). Simulates stratospheric flight above commercial ceiling.  
**Realism Score:** 95.7 / 100  

### material_aluminum_only
**Category:** Material  
**N Rows:** 50  
**Description:** Aluminum-only structure set. Lower density but lower strength — budget aerospace applications.  
**Realism Score:** 95.7 / 100  

### high_durability_cluster
**Category:** Target  
**N Rows:** 50  
**Description:** All High-Durability configurations. Best-case scenario for structural longevity design.  
**Realism Score:** 95.1 / 100  

### pressure_extreme_low
**Category:** Flight Envelope  
**N Rows:** 50  
**Description:** Pressure at 5th percentile (<110,000 Pa). Very low ambient pressure — high-altitude regime.  
**Realism Score:** 95.1 / 100  

### altitude_extreme_low
**Category:** Flight Envelope  
**N Rows:** 50  
**Description:** Altitude at 5th percentile (<7,000 m). Simulates low-altitude flight or climb/descent phase.  
**Realism Score:** 93.9 / 100  

### operational_life_short
**Category:** Lifecycle  
**N Rows:** 50  
**Description:** Operational life 20-22 years. Short-service aircraft — possibly military or regional commuter.  
**Realism Score:** 93.3 / 100  

### material_titanium_only
**Category:** Material  
**N Rows:** 50  
**Description:** Titanium-only structure set. Balanced strength-to-weight — engine pylons, landing gear.  
**Realism Score:** 93.3 / 100  

### tensile_extreme_low
**Category:** Material  
**N Rows:** 50  
**Description:** Tensile strength <370 MPa. Lowest-grade structural materials — near yield limit.  
**Realism Score:** 92.7 / 100  

### modulus_extreme_high
**Category:** Material  
**N Rows:** 50  
**Description:** Young's modulus >185 GPa. Highest stiffness — Carbon Fiber composites at maximum grade.  
**Realism Score:** 92.7 / 100  

### pressure_extreme_high
**Category:** Flight Envelope  
**N Rows:** 50  
**Description:** Pressure at 95th percentile (>190,000 Pa). Near sea-level equivalent — low-altitude pressurization.  
**Realism Score:** 91.5 / 100  

### short_optimization
**Category:** Optimization  
**N Rows:** 50  
**Description:** Optimization time <60 sec. Fast convergence — simpler structural problems or efficient search.  
**Realism Score:** 87.9 / 100  

### density_extreme_heavy
**Category:** Material  
**N Rows:** 50  
**Description:** Density >4,200 kg/m3. Heavy structural material — likely dense Titanium alloy.  
**Realism Score:** 87.9 / 100  

### tensile_extreme_high
**Category:** Material  
**N Rows:** 50  
**Description:** Tensile strength >1,400 MPa. Ultra-high-strength alloys for extreme load scenarios.  
**Realism Score:** 87.3 / 100  

### thickness_extreme_thick
**Category:** Geometry  
**N Rows:** 50  
**Description:** Structural thickness >14.5 mm. Heavily reinforced structure — armored or pressure vessel.  
**Realism Score:** 87.3 / 100  

### temperature_extreme_cold
**Category:** Flight Envelope  
**N Rows:** 50  
**Description:** Temperature at coldest 5th percentile (<-57 degrees C). Extreme cold soak scenario.  
**Realism Score:** 84.9 / 100  

### excellent_weight_efficiency
**Category:** Target  
**N Rows:** 50  
**Description:** All Excellent Weight Efficiency rows. Optimal lightweight structural designs.  
**Realism Score:** 83.1 / 100  

### thickness_extreme_thin
**Category:** Geometry  
**N Rows:** 50  
**Description:** Structural thickness <6 mm. Thin-shell structure — risk of buckling under compressive load.  
**Realism Score:** 83.1 / 100  

### chaotic_quantum_only
**Category:** Optimization  
**N Rows:** 50  
**Description:** Chaotic Quantum Genetic algorithm only. Quantum-inspired genetic algorithm with chaotic initialization.  
**Realism Score:** 82.5 / 100  

### density_extreme_light
**Category:** Material  
**N Rows:** 50  
**Description:** Density <1,800 kg/m3. Ultra-lightweight materials — Carbon Fiber or thin Aluminum.  
**Realism Score:** 81.3 / 100  

### long_optimization
**Category:** Optimization  
**N Rows:** 50  
**Description:** Optimization time >145 sec. Computationally expensive convergence — complex search spaces.  
**Realism Score:** 81.3 / 100  

### wingspan_extreme_small
**Category:** Geometry  
**N Rows:** 50  
**Description:** Wing span <24 m. Short-range jet or fighter configuration — high wing loading.  
**Realism Score:** 69.3 / 100  
