"""
Slides Part 3: Module 2 — Frontier Research & Failure Modes (Slides 12 to 17)
Executive Editorial Light System: Crisp white canvas, 0.8" margins, deep ink typography.
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from deck_common import (
    new_slide, add_card, add_rect, add_header, add_takeaway, add_stat_box,
    add_badge, set_notes, add_math_image, section_divider_slide, BG_CANVAS,
    BG_CARD, BG_CARD_ALT, BG_CARD_ACCENT, BORDER_SUBTLE, BORDER_GOLD,
    BORDER_CYAN, BORDER_GREEN, BORDER_AMBER, BORDER_RED, BORDER_PURPLE, GOLD, CYAN, GREEN,
    AMBER, RED, PURPLE, WHITE, COLOR_WHITE, BRAND_NAVY, BRAND_BLUE, INK_PRIMARY,
    TEXT_LIGHT, TEXT_MUTED, FONT_NAME
)

def slide_12_m2_divider():
    return section_divider_slide(
        2,
        "Frontier Research Direction",
        "What the Frontier Is Actually Working On & Canonical Failure Modes",
        [
            "Five active engineering bottlenecks across frontier research labs",
            "Continuous action flow matching vs. discrete tokenization (π0, ManiFlow)",
            "Physics-informed 3D spatial world models and cross-embodiment scaling laws",
            "The five canonical world-model failure modes and engineering mitigations",
            "Pearl's Causal Ladder: why LLMs fundamentally fail at physical robotics control"
        ]
    )

def slide_13_frontier_priorities_p1():
    s = new_slide()
    add_header(s, "Module 2 · Research Frontiers", "Frontier Technical Priorities (1 & 2): Control & World Models",
               "Analyzing technical reports from Physical Intelligence, DeepMind, NVIDIA GEAR, BAIR, and TRI.")

    # Left: Flow Matching vs Tokenization
    add_card(s, 0.8, 1.85, 5.7, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, 5.7, 0.025, CYAN)
    add_badge(s, 1.05, 2.05, "PRIORITY 1: TRAJECTORY GENERATION", bg=BORDER_CYAN, fg=CYAN, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(5.2), Inches(4.0))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Continuous Action Flow Matching vs. Discrete Tokens\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    points_p1 = [
        ("The Legacy Problem (RT-1, RT-2):", "Early Vision-Language-Action (VLA) models quantized continuous joint actions into discrete text tokens (e.g. 256 bins). This caused severe discretization errors, high inference latency, and jerky motion unsuitable for physical contact."),
        ("The Frontier Paradigm Shift:", "Leading frontier models—specifically π0 from Physical Intelligence (Oct 2024) and ManiFlow—abandon discrete tokenization in favor of continuous flow matching."),
        ("Direct High-Frequency Trajectories:", "Flow matching generates high-frequency continuous control trajectories directly at 50Hz (20ms step time), providing smooth, compliant end-effector motion capable of handling high-speed industrial manipulation tasks.")
    ]
    for h, d in points_p1:
        p = tf_l.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run()
        rh.text = f"•  {h} "
        rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = CYAN
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Right: 3D Spatial World Models
    add_card(s, 6.83, 1.85, 5.7, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 6.83, 1.85, 5.7, 0.025, BRAND_NAVY)
    add_badge(s, 7.08, 2.05, "PRIORITY 2: WORLD MODELING", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(7.08), Inches(2.40), Inches(5.2), Inches(4.0))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "Physics-Informed and 3D Spatial World Models\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(12); rr1.font.bold = True; rr1.font.color.rgb = INK_PRIMARY

    points_p2 = [
        ("Abandoning 2D Pixel Hallucination:", "Traditional video prediction models hallucinate pixels without understanding mass, contact geometry, or Newton's laws of motion. Generating visually plausible frames fails in robotics if physical contact violates mechanics."),
        ("Transition to 3D Voxel & Point-Flow:", "Frontier labs are moving aggressively to 3D voxel representations and point-flow dynamics (PointWorld, NVIDIA Cosmos-Predict)."),
        ("Modeling Contact & Bounds:", "These models explicitly simulate collision bounds, surface normals, friction coefficients, and kinematic volume constraints, enabling robots to predict physical contact outcomes before executing motions.")
    ]
    for h, d in points_p2:
        p = tf_r.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run()
        rh.text = f"•  {h} "
        rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = BRAND_NAVY
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Robotics is ditching discrete text tokens for 50Hz continuous flow matching, and replacing 2D pixel prediction with 3D point-flow physics.")
    set_notes(s, "Explain Priority 1 & 2. Explain why discrete tokens failed: you cannot run a robot arm smoothly at 50Hz by generating text tokens. Flow matching is the solution.")
    return s


def slide_14_frontier_priorities_p2():
    s = new_slide()
    add_header(s, "Module 2 · Research Frontiers", "Frontier Technical Priorities (3, 4 & 5): RFT, Scaling & Edge",
               "Reinforced Fine-Tuning, Cross-Embodiment Scaling Laws, and Deterministic Edge Quantization.")

    cards = [
        ("Priority 3: RFT for Dexterous Skills", PURPLE, BORDER_PURPLE,
         "Autonomous Error Recovery & Sub-Goals",
         [
             ("The Imitation Drift Problem:", "Pure behavioral cloning / imitation learning suffers catastrophic distributional drift when tiny tracking errors accumulate over long rollouts."),
             ("Stage-Aware Sub-Goal Rewards:", "Labs apply Reinforced Fine-Tuning (RFT) using STA-PPO (Stage-Aware Proximal Policy Optimization) and residual policy heads."),
             ("Autonomous Error Recovery:", "Enables policies to autonomously recover when an object slips, re-orienting grips without human teleoperation intervention.")
         ]),
        
        ("Priority 4: Cross-Embodiment Scaling", CYAN, BORDER_CYAN,
         "Pre-training on Egocentric Human Video",
         [
             ("NVIDIA EgoScale Study (2026):", "Empirical research proves log-linear capability scaling when pre-training base policies on massive egocentric human video datasets (arXiv:2602.16710)."),
             ("Morphology Transfer:", "Abstract spatial affordances and manipulation primitives learned from human hands transfer efficiently to multi-fingered robot hands and parallel grippers."),
             ("Data Multiplier Effect:", "Solves the chronic scarcity of physical robot telemetry by leveraging uncurated video at internet scale.")
         ]),
        
        ("Priority 5: Edge Model Compression", GREEN, BORDER_GREEN,
         "Real-Time Execution on Embedded GPUs",
         [
             ("The Real-Time Latency Constraint:", "Multi-billion parameter VLAs cannot be deployed across high-latency cloud networks for closed-loop industrial control (<20ms required)."),
             ("Channel-Aware Quantization (AutoQVLA):", "Advanced compression pipelines preserve control sensitivity while reducing weights to INT4/FP8 formats."),
             ("Deterministic Jetson Execution:", "Enables deterministic, low-jitter policy execution directly on embedded industrial GPUs (NVIDIA Jetson AGX Orin).")
         ])
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, items) in enumerate(cards):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.22), Inches(card_w - 0.4), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run()
        r2.text = sub
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_body = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.25), Inches(card_w - 0.4), Inches(3.3))
        tf_b = tx_body.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for j, (hdr, desc) in enumerate(items):
            pj = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            if j > 0: pj.space_before = Pt(7)
            rj1 = pj.add_run()
            rj1.text = f"{hdr}\n"
            rj1.font.name = FONT_NAME; rj1.font.size = Pt(9.5); rj1.font.bold = True; rj1.font.color.rgb = INK_PRIMARY
            rj2 = pj.add_run()
            rj2.text = desc
            rj2.font.name = FONT_NAME; rj2.font.size = Pt(8.8); rj2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "The combination of RFT error recovery, human video scaling, and Jetson edge quantization makes industrial embodied AI technically viable.")
    set_notes(s, "Explain Priorities 3, 4, 5. Mention NVIDIA EgoScale (2026) and edge quantization on Jetson AGX Orin for factory edge determinism.")
    return s


def slide_15_failure_modes_p1():
    s = new_slide()
    add_header(s, "Module 2 · Research Frontiers", "Canonical Failure Modes (FM1 & FM2): Drift & Executability",
               "Every physical AI failure mode has an identified physical mechanism and engineering mitigation.")

    fms = [
        ("FM1: Compounding Autoregressive Drift", RED, BORDER_RED,
         "Physical Mechanism: Error Compounding Across Rollouts",
         "In autoregressive policy execution, minor per-step prediction errors (sub-millimeter positioning drift, slight angular offsets) multiply exponentially over extended time horizons. A 1% per-step error compounds to catastrophic task failure after a 100-step trajectory, causing the robot to completely miss target fixtures or crash into boundaries.",
         "Active Engineering Mitigation:",
         "Hierarchical state space representations, receding-horizon Model Predictive Control (MPC) re-planning, and continuous action flow matching that resynchronizes with sensory state at 50Hz.",
         "Resolution Status: Partially solved on academic benchmarks; active engineering deployment ongoing in production fields.",
         AMBER),

        ("FM2: The Executability Gap", AMBER, BORDER_AMBER,
         "Physical Mechanism: Visual Plausibility vs. Physical Validity",
         "Generative diffusion and video world models produce sequences of future visual frames that look highly plausible to human eyes but violate real contact mechanics—such as objects penetrating rigid surfaces, frictionless sliding, or phantom reaction forces. Robot controllers attempting to track these unphysical trajectories generate unbounded torques or stall.",
         "Active Engineering Mitigation:",
         "Incorporating physics-informed loss constraints (PINN formulations) directly into latent loss functions and embedding differentiable physics engines into the generation loop.",
         "Resolution Status: Gaining rapid traction in commercial simulation tooling (NVIDIA Isaac Sim / Cosmos).",
         GREEN)
    ]

    for i, (title, color, border, mech_h, mech_d, mit_h, mit_d, stat, stat_c) in enumerate(fms):
        left = 0.8 + i * (5.7 + 0.33)
        top = 1.85
        card_w = 5.7
        card_h = 4.75

        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.25, top + 0.22, f"CANONICAL FAILURE MODE {i+1}", bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.60), Inches(card_w - 0.5), Inches(4.0))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = title.split(":")[1].strip() + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(12.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        r2h = p2.add_run()
        r2h.text = f"{mech_h}\n"
        r2h.font.name = FONT_NAME; r2h.font.size = Pt(9.5); r2h.font.bold = True; r2h.font.color.rgb = BRAND_NAVY
        r2d = p2.add_run()
        r2d.text = mech_d
        r2d.font.name = FONT_NAME; r2d.font.size = Pt(9); r2d.font.color.rgb = TEXT_LIGHT

        p3 = tf.add_paragraph()
        p3.space_before = Pt(8)
        r3h = p3.add_run()
        r3h.text = f"{mit_h}\n"
        r3h.font.name = FONT_NAME; r3h.font.size = Pt(9.5); r3h.font.bold = True; r3h.font.color.rgb = BRAND_BLUE
        r3d = p3.add_run()
        r3d.text = mit_d
        r3d.font.name = FONT_NAME; r3d.font.size = Pt(9); r3d.font.color.rgb = TEXT_LIGHT

        p4 = tf.add_paragraph()
        p4.space_before = Pt(8)
        r4 = p4.add_run()
        r4.text = f"Status: {stat}"
        r4.font.name = FONT_NAME; r4.font.size = Pt(9); r4.font.bold = True; r4.font.color.rgb = stat_c

    add_takeaway(s, "FM1 and FM2 prove why raw generative video models cannot drive robots without physics-informed bounds and real-time receding MPC.")
    set_notes(s, "Explain FM1 (compounding error drift) and FM2 (executability gap: visual realism is not physical validity). Emphasize the engineering solutions.")
    return s


def slide_16_failure_modes_p2():
    s = new_slide()
    add_header(s, "Module 2 · Research Frontiers", "Canonical Failure Modes (FM3, FM4, FM5): Residuals & Sim-to-Real",
               "Perceptual Hallucination, Action Marginalization, and the Sim-to-Real Reality Gap.")

    modes = [
        ("FM3: Perceptual Hallucination", RED, BORDER_RED,
         "Out-of-Distribution Inputs Mapped to Known Tokens",
         "Novel industrial lighting conditions, unexpected reflections from metallic sheet surfaces, or occluded parts cause neural encoders to collapse out-of-distribution (OOD) states into incorrect known tokens.",
         r'\mathcal{E}_{\text{recon}} > \tau',
         "Mitigation: Latent reconstruction residual gating. If reconstruction error exceeds threshold tau, the model trips safety interlocks rather than commanding motion.",
         "Critical for formal safety interlocks."),

        ("FM4: Action Marginalization", AMBER, BORDER_AMBER,
         "Predictions Invariant to Real-Time Operator Inputs",
         "When world models are trained on massive video corpora with weak action grounding, predicted future states become invariant to real-time control commands, effectively ignoring teleoperator or safety override signals.",
         r'\mathcal{L}_{\text{contrastive}}(s, a)',
         "Mitigation: Action-conditioned contrastive losses and dedicated inverse dynamics heads that explicitly penalize predictions failing to reflect control inputs.",
         "Active research in foundation labs."),

        ("FM5: Sim-to-Real Reality Gap", PURPLE, BORDER_PURPLE,
         "Discrepancies in Friction & Contact Compliance",
         "Mismatches between rigid-body simulation dynamics and real-world micro-friction, payload inertia, and cable elasticity cause high-performing simulated policies to fail instantly in real plants.",
         r'\text{Real2Sim2Real Loop}',
         "Mitigation: Real2Sim2Real closed loops with automated physics system identification, extreme domain randomization, and hybrid synthetic-plus-real fine-tuning.",
         "Standard industrial engineering practice.")
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, mech, math_eq, mit, stat) in enumerate(modes):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.2, top + 0.22, f"FAILURE MODE {i+3}", bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.60), Inches(card_w - 0.4), Inches(0.65))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title.split(":")[1].strip()
        r.font.name = FONT_NAME; r.font.size = Pt(11.5); r.font.bold = True; r.font.color.rgb = INK_PRIMARY

        tx_b = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.25), Inches(card_w - 0.4), Inches(1.3))
        tf_b = tx_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        pb = tf_b.paragraphs[0]
        rb1 = pb.add_run()
        rb1.text = "Physical Mechanism:\n"
        rb1.font.name = FONT_NAME; rb1.font.size = Pt(9); rb1.font.bold = True; rb1.font.color.rgb = BRAND_NAVY
        rb2 = pb.add_run()
        rb2.text = mech
        rb2.font.name = FONT_NAME; rb2.font.size = Pt(8.8); rb2.font.color.rgb = TEXT_LIGHT

        # Math Formulation Card (Deep Ink)
        add_card(s, left + 0.2, top + 2.65, card_w - 0.4, 0.65, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
        add_math_image(s, math_eq, left + 0.35, top + 2.75, fontsize=16, color='#0F172A', max_h=0.45)

        tx_m = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 3.45), Inches(card_w - 0.4), Inches(1.4))
        tf_m = tx_m.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
        pm = tf_m.paragraphs[0]
        rm1 = pm.add_run()
        rm1.text = "Mitigation & Resolution:\n"
        rm1.font.name = FONT_NAME; rm1.font.size = Pt(9); rm1.font.bold = True; rm1.font.color.rgb = BRAND_BLUE
        rm2 = pm.add_run()
        rm2.text = mit + "\n"
        rm2.font.name = FONT_NAME; rm2.font.size = Pt(8.5); rm2.font.color.rgb = TEXT_LIGHT
        rm3 = pm.add_run()
        rm3.text = f"Status: {stat}"
        rm3.font.name = FONT_NAME; rm3.font.size = Pt(8.5); rm3.font.bold = True; rm3.font.color.rgb = GREEN

    add_takeaway(s, "No known deployment failure mode is beyond engineering control. Every failure has a quantitative mathematical mitigation.")
    set_notes(s, "Detail FM3, FM4, and FM5. Point out the residual gating equation E_recon > tau for tripping safety interlocks.")
    return s


def slide_17_causal_ladder():
    s = new_slide()
    add_header(s, "Module 2 · Research Frontiers", "Pearl's Causal Ladder: Why LLMs Fail at Robotics",
               "Deploying standard language models into robotics fails due to a fundamental representational mismatch.")

    rungs = [
        ("Rung I: Association & Observation", BRAND_BLUE, BORDER_CYAN,
         r'P(Y \mid X)',
         "Where LLMs Operate (Static Semantic Space)",
         "Standard language models operate strictly on observational correlations: P(Y | X). They predict the most probable next token based on statistical co-occurrences in historical training corpora.",
         "Limitation: Passive observation cannot distinguish causal influence from spurious correlation. A language model knows 'smoke follows fire' but has no concept of physical mass, velocity, or friction."),

        ("Rung II: Intervention & Action", BRAND_NAVY, BORDER_SUBTLE,
         r'P(Y \mid \text{do}(u))',
         "The Domain of Physical AI (Dynamic Closed-Loop)",
         "Physical control mandates causal intervention: P(Y | do(u)). A robot controller cannot merely guess tokens; it must predict precisely what physical state Y occurs when it commands a specific 15N torque u to an actuator.",
         "Requirement: Demands dedicated physical world models that map continuous control forces to kinematic motion under Newton's equations."),

        ("Rung III: Counterfactuals & Planning", GREEN, BORDER_GREEN,
         r'P(Y_u \mid X^\prime, Y^\prime)',
         "The Benchmark for Certified Safety & V&V",
         "Safe autonomous execution requires evaluating counterfactual alternatives: P(Yu | X', Y'). The system must compute: 'Given that obstacle X was encountered, would trajectory u have prevented collision?'",
         "Requirement: Essential for formal functional safety dossiers, reachability verification, and insurance compliance in brownfield plants.")
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, math_eq, sub, desc, req) in enumerate(rungs):
        left = 0.8 + i * (card_w + gap)
        top = 1.80
        card_h = 4.80
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.2, top + 0.20, f"RUNG {i+1} OF CAUSALITY", bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.60), Inches(card_w - 0.4), Inches(0.7))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title.split(":")[1].strip() + "\n"
        r.font.name = FONT_NAME; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = INK_PRIMARY
        r_sub = p.add_run()
        r_sub.text = sub
        r_sub.font.name = FONT_NAME; r_sub.font.size = Pt(9); r_sub.font.bold = True; r_sub.font.color.rgb = color

        # Math Equation Display (Crisp Deep Ink)
        add_card(s, left + 0.2, top + 1.45, card_w - 0.4, 0.65, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
        add_math_image(s, math_eq, left + 0.35, top + 1.55, fontsize=18, color='#0F172A', max_h=0.45)

        tx_d = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 2.25), Inches(card_w - 0.4), Inches(2.3))
        tf_d = tx_d.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        
        pd1 = tf_d.paragraphs[0]
        rd1 = pd1.add_run()
        rd1.text = desc
        rd1.font.name = FONT_NAME; rd1.font.size = Pt(9.2); rd1.font.color.rgb = TEXT_LIGHT

        pd2 = tf_d.add_paragraph()
        pd2.space_before = Pt(8)
        rd2 = pd2.add_run()
        rd2.text = req
        rd2.font.name = FONT_NAME; rd2.font.size = Pt(8.8); rd2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "This causal hierarchy proves why industrial robotics requires dedicated physics-grounded verification rather than raw LLM prompt engineering.")
    set_notes(s, "Explain Judea Pearl's Causal Hierarchy. Language models are trapped on Rung 1 (observation). Physical AI requires Rung 2 (intervention) and Rung 3 (counterfactual safety).")
    return s
