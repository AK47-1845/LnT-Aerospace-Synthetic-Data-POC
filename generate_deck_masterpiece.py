"""
The Practice of Physical AI — Master Executive Presentation Builder
Synthesizes all 51 slides into The_Practice_of_Physical_AI_Executive_Deck.pptx
"""

import os
import sys
import time

from deck_common import prs, OUTPUT_PPTX

from slides_part1_intro import (
    slide_01_cover, slide_02_taxonomy, slide_03_exec_summary, slide_04_agenda
)
from slides_part2_module1 import (
    slide_05_m1_divider, slide_06_maturity_framework, slide_07_tier1_deepdive,
    slide_08_tier2_tier3_deepdive, slide_09_capital_matrix_p1,
    slide_10_capital_matrix_p2, slide_11_capital_asymmetry
)
from slides_part3_module2 import (
    slide_12_m2_divider, slide_13_frontier_priorities_p1,
    slide_14_frontier_priorities_p2, slide_15_failure_modes_p1,
    slide_16_failure_modes_p2, slide_17_causal_ladder
)
from slides_part4_module3 import (
    slide_18_m3_divider, slide_19_commercial_models_table,
    slide_20_engineering_services_opportunity, slide_21_offerings_1_and_2,
    slide_22_offerings_3_and_4
)
from slides_part5_module4_5 import (
    slide_23_m4_divider, slide_24_verified_deployments, slide_25_hype_analysis,
    slide_26_hybrid_adoption_model, slide_27_m5_divider,
    slide_28_competitive_map_table, slide_29_underserved_gaps
)
from slides_part6_module6_7 import (
    slide_30_m6_divider, slide_31_industrial_vs_physical,
    slide_32_kinematic_moat, slide_33_timing_and_safety_moat,
    slide_34_data_flywheel, slide_35_m7_divider, slide_36_market_evolution,
    slide_37_sources_of_uncertainty
)
from slides_part7_module8 import (
    slide_38_m8_divider, slide_39_phasing_rationale, slide_40_priority1_vv,
    slide_41_priority2_alliances, slide_42_priority3_synthetic_data,
    slide_43_priority4_coe, slide_44_roadmap_table,
    slide_45_strategic_conclusion
)
from slides_part8_appendices import (
    slide_46_app_divider, slide_47_appendix_a_p1, slide_48_appendix_a_p2,
    slide_49_appendix_b_p1, slide_50_appendix_b_p2, slide_51_signoff
)

def build_presentation():
    start_time = time.time()
    print("=" * 70)
    print("  BUILDING: The Practice of Physical Artificial Intelligence")
    print("  51-Slide Master Executive Presentation Deck for LTTS Leadership")
    print("=" * 70)

    slides = [
        # Part 1: Executive Foundation
        (slide_01_cover,                      "01. Title & Executive Cover"),
        (slide_02_taxonomy,                   "02. Four-Tier Verification Taxonomy"),
        (slide_03_exec_summary,                "03. Executive Summary & Core Strategic Thesis"),
        (slide_04_agenda,                     "04. Presentation Architecture / Agenda"),

        # Part 2: Module 1 — Commercial State Mapping
        (slide_05_m1_divider,                 "05. Section Divider: Commercial State"),
        (slide_06_maturity_framework,         "06. Commercial Maturity Tiers Framework"),
        (slide_07_tier1_deepdive,             "07. Tier 1: Commercial Production at Scale"),
        (slide_08_tier2_tier3_deepdive,       "08. Tier 2 & Tier 3: Pilots vs. Lab Claims"),
        (slide_09_capital_matrix_p1,          "09. Capital Matrix: Foundation Models & Humanoids"),
        (slide_10_capital_matrix_p2,          "10. Capital Matrix: Automation, Simulation, Safety"),
        (slide_11_capital_asymmetry,          "11. Capital vs. Maturity Asymmetry & Hardware Trap"),

        # Part 3: Module 2 — Frontier Research & Failure Modes
        (slide_12_m2_divider,                 "12. Section Divider: Frontier Research"),
        (slide_13_frontier_priorities_p1,     "13. Frontier Priorities: Flow Matching & 3D Models"),
        (slide_14_frontier_priorities_p2,     "14. Frontier Priorities: RFT, Scaling & Edge"),
        (slide_15_failure_modes_p1,           "15. Canonical Failure Modes: FM1 & FM2"),
        (slide_16_failure_modes_p2,           "16. Canonical Failure Modes: FM3, FM4 & FM5"),
        (slide_17_causal_ladder,              "17. Pearl's Causal Ladder: Why LLMs Fail at Robotics"),

        # Part 4: Module 3 — Commercialization & LTTS Playbook
        (slide_18_m3_divider,                 "18. Section Divider: Commercialization"),
        (slide_19_commercial_models_table,    "19. Commercial Models & Deal Economics (Table 3)"),
        (slide_20_engineering_services_opportunity, "20. The Engineering Services Opportunity"),
        (slide_21_offerings_1_and_2,          "21. LTTS Commercial Offerings 1 & 2 (SD-FaaS, PLC)"),
        (slide_22_offerings_3_and_4,          "22. LTTS Commercial Offerings 3 & 4 (V&V, MLOps)"),

        # Part 5: Module 4 & 5 — Use Cases & Competitive Map
        (slide_23_m4_divider,                 "23. Section Divider: Use Cases & Adoption"),
        (slide_24_verified_deployments,       "24. Verified Deployments Across 5 Core Sectors"),
        (slide_25_hype_analysis,              "25. Hype-Ahead-of-Deployment Analysis"),
        (slide_26_hybrid_adoption_model,      "26. Dominance of the Hybrid Incumbent Model"),
        (slide_27_m5_divider,                 "27. Section Divider: Competitive Landscape"),
        (slide_28_competitive_map_table,      "28. Layered Competitive Map (Table 4)"),
        (slide_29_underserved_gaps,           "29. High-Value Underserved Market Gaps"),

        # Part 6: Module 6 & 7 — Industrial Bridge & Forecast
        (slide_30_m6_divider,                 "30. Section Divider: The Industrial-AI Bridge"),
        (slide_31_industrial_vs_physical,     "31. Industrial AI vs. Physical AI & Replacement"),
        (slide_32_kinematic_moat,             "32. Kinematics Moat: Jacobian & Singularities"),
        (slide_33_timing_and_safety_moat,     "33. Deterministic RTOS Timing & Safety Interlocks"),
        (slide_34_data_flywheel,              "34. The Closed-Loop Operational Data Flywheel"),
        (slide_35_m7_divider,                 "35. Section Divider: 3-5 Year Forecast"),
        (slide_36_market_evolution,           "36. Market Evolution Dynamics (2026-2030)"),
        (slide_37_sources_of_uncertainty,     "37. Key Sources of Uncertainty & Wildcards"),

        # Part 7: Module 8 — Strategic Recommendations for LTTS
        (slide_38_m8_divider,                 "38. Section Divider: Strategic Recommendations"),
        (slide_39_phasing_rationale,          "39. Strategic Phasing Rationale & Sequencing"),
        (slide_40_priority1_vv,               "40. Priority 1: Physical AI V&V Practice ($2.8M)"),
        (slide_41_priority2_alliances,        "41. Priority 2: Strategic PLC Alliances ($1.3M)"),
        (slide_42_priority3_synthetic_data,   "42. Priority 3: Synthetic Data Factories ($4.2M)"),
        (slide_43_priority4_coe,              "43. Priority 4: Hybrid Talent CoE ($2.5M/yr)"),
        (slide_44_roadmap_table,              "44. LTTS Strategic Roadmap & Milestones (Table 5)"),
        (slide_45_strategic_conclusion,       "45. Strategic Conclusion: The Bridge to Physical AI"),

        # Part 8: Appendices & Governance
        (slide_46_app_divider,                "46. Section Divider: Appendices & Governance"),
        (slide_47_appendix_a_p1,              "47. Appendix A: Sources Index (Commercial & Capital)"),
        (slide_48_appendix_a_p2,              "48. Appendix A: Sources Index (Research & Field)"),
        (slide_49_appendix_b_p1,              "49. Appendix B: Adversarial Self-Critique (Items 1-5)"),
        (slide_50_appendix_b_p2,              "50. Appendix B: Adversarial Self-Critique (Items 6-11)"),
        (slide_51_signoff,                    "51. Executive Document Sign-Off & Distribution")
    ]

    for idx, (func, label) in enumerate(slides):
        func()
        print(f"  [{idx+1:02d}/51] Rendered: {label}")

    prs.save(OUTPUT_PPTX)
    elapsed = time.time() - start_time
    print("=" * 70)
    print(f"  SUCCESSFULLY GENERATED: {OUTPUT_PPTX}")
    print(f"  Total Slides: {len(slides)}")
    print(f"  Execution Time: {elapsed:.2f} seconds")
    print("=" * 70)

if __name__ == "__main__":
    build_presentation()
