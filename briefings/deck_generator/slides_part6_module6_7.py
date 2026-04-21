"""
Slides Part 6: Modules 6 & 7 — Industrial Bridge, Kinematics & 3-5 Yr Forecast (Slides 30 to 37)
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

def slide_30_m6_divider():
    return section_divider_slide(
        6,
        "The Industrial-AI Bridge",
        "Evolution vs. Category Split, Formal Kinematics Moat & The Data Flywheel",
        [
            "Industrial AI vs. Physical AI: architectural distinctions and coexistence",
            "Where Physical AI replaces traditional models vs. where time-series dominates",
            "The domain engineering moat: formal kinematics, Jacobian singularities, and DLS filtering",
            "Deterministic RTOS timing (<1ms jitter) and ISO 13849 Cat 4 / PL e safety circuits",
            "LTTS's 5-stage closed-loop operational data flywheel"
        ]
    )

def slide_31_industrial_vs_physical():
    s = new_slide()
    add_header(s, "Module 6 · The Bridge", "Evolution vs. Separate Category & Replacement Dynamics",
               "Physical AI is a fundamentally distinct technical discipline requiring robotics controls DNA.")

    card_w = 5.7
    gap = 0.33

    # Top Left: Industrial AI
    add_card(s, 0.8, 1.85, card_w, 2.35, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, CYAN)
    add_badge(s, 1.05, 2.05, "TRADITIONAL INDUSTRIAL AI", bg=BORDER_CYAN, fg=CYAN, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.38), Inches(card_w - 0.5), Inches(1.7))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run(); r1.text = "Association & Open-Loop Monitoring\n"; r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    pts_ind = [
        ("Data Space:", "Operates on 1D scalar time-series (vibration, temp, motor current)."),
        ("Control Loop:", "Open-loop. Generates human alerts on minute or hour timescales."),
        ("Organizational DNA:", "Built by software data scientists. Zero kinematics or real-time RTOS requirements.")
    ]
    for h, d in pts_ind:
        p = tf_l.add_paragraph()
        p.space_before = Pt(3)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9); rh.font.bold = True; rh.font.color.rgb = CYAN
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(8.8); rd.font.color.rgb = TEXT_LIGHT

    # Top Right: Physical AI
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 2.35, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, BRAND_NAVY)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "EMBODIED PHYSICAL AI", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.38), Inches(card_w - 0.5), Inches(1.7))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run(); rr1.text = "Causal & Closed-Loop Actuator Control\n"; rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = INK_PRIMARY

    pts_phy = [
        ("Data Space:", "Operates on 3D spatial representations, depth point clouds, force-torque vectors."),
        ("Control Loop:", "Closed-loop. Directly commands joint actuators at >= 50Hz (delta-t <= 20ms)."),
        ("Organizational DNA:", "Requires deep mechatronics, multi-body dynamics, and formal safety engineering.")
    ]
    for h, d in pts_phy:
        p = tf_r.add_paragraph()
        p.space_before = Pt(3)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9); rh.font.bold = True; rh.font.color.rgb = BRAND_NAVY
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(8.8); rd.font.color.rgb = TEXT_LIGHT

    # Bottom Left: Where Physical AI Replaces Industrial AI
    add_card(s, 0.8, 4.40, card_w, 2.20, bg=BG_CARD_ALT, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 4.40, card_w, 0.025, GREEN)
    tx_rep = s.shapes.add_textbox(Inches(1.05), Inches(4.55), Inches(card_w - 0.5), Inches(1.95))
    tf_rep = tx_rep.text_frame; tf_rep.word_wrap = True; tf_rep.margin_left = tf_rep.margin_right = tf_rep.margin_top = tf_rep.margin_bottom = 0
    prep = tf_rep.paragraphs[0]
    r_rep_h = prep.add_run(); r_rep_h.text = "WHERE PHYSICAL AI REPLACES INDUSTRIAL AI:\n"; r_rep_h.font.name = FONT_NAME; r_rep_h.font.size = Pt(10); r_rep_h.font.bold = True; r_rep_h.font.color.rgb = GREEN
    r_rep_d = prep.add_run()
    r_rep_d.text = "In dynamic, high-speed closed-loop manufacturing tasks where microsecond feedback alters tool behavior:\n" \
                   "• Real-time CNC spindle modulation to suppress chatter vibration.\n" \
                   "• Real-time adaptive seam tracking and wire-feed modulation in robotic welding."
    r_rep_d.font.name = FONT_NAME; r_rep_d.font.size = Pt(9); r_rep_d.font.color.rgb = TEXT_LIGHT

    # Bottom Right: Where Industrial AI Remains Dominant
    add_card(s, 0.8 + card_w + gap, 4.40, card_w, 2.20, bg=BG_CARD_ALT, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 4.40, card_w, 0.025, BRAND_BLUE)
    tx_coex = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(4.55), Inches(card_w - 0.5), Inches(1.95))
    tf_coex = tx_coex.text_frame; tf_coex.word_wrap = True; tf_coex.margin_left = tf_coex.margin_right = tf_coex.margin_top = tf_coex.margin_bottom = 0
    pcoex = tf_coex.paragraphs[0]
    r_coex_h = pcoex.add_run(); r_coex_h.text = "WHERE INDUSTRIAL AI REMAINS DOMINANT:\n"; r_coex_h.font.name = FONT_NAME; r_coex_h.font.size = Pt(10); r_coex_h.font.bold = True; r_coex_h.font.color.rgb = BRAND_BLUE
    r_coex_d = pcoex.add_run()
    r_coex_d.text = "In macro enterprise optimization where physical interaction is decoupled from high-frequency execution:\n" \
                    "• Plant-wide predictive asset maintenance across hundreds of pumps and motors.\n" \
                    "• Macro supply-chain scheduling and enterprise power consumption forecasting."
    r_coex_d.font.name = FONT_NAME; r_coex_d.font.size = Pt(9); r_coex_d.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Predictive maintenance vendors cannot easily pivot into robotics control; Physical AI demands deep mechatronics and controls engineering.")
    set_notes(s, "Industrial AI vs Physical AI. Detail why scalar time-series models cannot command robots at 50Hz. Physical AI requires spatial 3D reasoning.")
    return s


def slide_32_kinematic_moat():
    s = new_slide()
    add_header(s, "Module 6 · The Bridge", "The Domain Engineering Moat: Kinematics & Singularities",
               "Why software-only AI labs cannot deploy neural policies on real industrial servo hardware.")

    card_w = 5.7
    gap = 0.33

    # Left: Mathematical Formalism Card
    add_card(s, 0.8, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, BRAND_NAVY)
    add_badge(s, 1.05, 2.05, "KINEMATIC INVARIANTS & SINGULARITY", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run(); r1.text = "Manipulator Jacobian & Inverse Kinematics:\n"; r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
    r2 = p1.add_run(); r2.text = "The mapping from end-effector velocities to joint velocities is governed by the Jacobian matrix J(q):"; r2.font.name = FONT_NAME; r2.font.size = Pt(9.2); r2.font.color.rgb = TEXT_LIGHT

    # Math Image 1: Jacobian Inversion (Deep Ink Black)
    add_card(s, 1.05, 3.25, card_w - 0.5, 0.65, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
    add_math_image(s, r'\dot{x} = J(q)\dot{q} \quad \Longrightarrow \quad \dot{q} = J^{\dagger}(q)\dot{x}', 1.25, 3.35, fontsize=16, color='#0F172A', max_h=0.45)

    tx_l2 = s.shapes.add_textbox(Inches(1.05), Inches(4.05), Inches(card_w - 0.5), Inches(2.4))
    tf_l2 = tx_l2.text_frame; tf_l2.word_wrap = True; tf_l2.margin_left = tf_l2.margin_right = tf_l2.margin_top = tf_l2.margin_bottom = 0
    p2 = tf_l2.paragraphs[0]
    r3 = p2.add_run(); r3.text = "Yoshikawa Manipulability Measure:\n"; r3.font.name = FONT_NAME; r3.font.size = Pt(11); r3.font.bold = True; r3.font.color.rgb = INK_PRIMARY
    r4 = p2.add_run(); r4.text = "Near kinematic singularities, manipulability collapses to zero:"; r4.font.name = FONT_NAME; r4.font.size = Pt(9.2); r4.font.color.rgb = TEXT_LIGHT

    # Math Image 2: Yoshikawa Collapse (Deep Ink Black)
    add_card(s, 1.05, 4.85, card_w - 0.5, 0.65, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
    add_math_image(s, r'\mu(q) = \sqrt{\det\left(J(q)J^T(q)\right)} \longrightarrow 0 \quad \Longrightarrow \quad \|\dot{q}\| \longrightarrow \infty', 1.20, 4.95, fontsize=15, color='#0F172A', max_h=0.45)

    tx_l3 = s.shapes.add_textbox(Inches(1.05), Inches(5.65), Inches(card_w - 0.5), Inches(0.85))
    tf_l3 = tx_l3.text_frame; tf_l3.word_wrap = True; tf_l3.margin_left = tf_l3.margin_right = tf_l3.margin_top = tf_l3.margin_bottom = 0
    p3 = tf_l3.paragraphs[0]
    r5 = p3.add_run()
    r5.text = "Even a small, bounded Cartesian command outputs unbounded joint speeds, triggering emergency trips or destroying gearboxes."
    r5.font.name = FONT_NAME; r5.font.size = Pt(9); r5.font.color.rgb = RED

    # Right: The Controls Engineering Solution
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, BRAND_BLUE)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "WHY PURE ML FAILS ON REAL HARDWARE", bg=BORDER_CYAN, fg=BRAND_BLUE, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "The Indispensable Mechatronics Filtering Layer\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(12); rr1.font.bold = True; rr1.font.color.rgb = INK_PRIMARY

    points_moat = [
        ("The AI Startup Blind Spot:", "Pure machine learning engineers treat robot arms as abstract point masses. When a VLA model plans a path passing near a wrist or elbow singularity, it demands infinite joint velocity."),
        ("Real Factory Consequences:", "In real production cells, this causes instant drive over-current trips, emergency brake engagements, or stripped harmonic gears."),
        ("Damped Least-Squares (DLS) Filtering:", "LTTS controls engineers insert singularity-robust inverse kinematics, singularity avoidance gradient projection, and DLS damping layers between neural outputs and motor servo drives."),
        ("The Durable Moat:", "This mechatronics filtering layer is mandatory for production deployment. Foundation model providers cannot build or certify this without industrial controls engineering.")
    ]
    for h, d in points_moat:
        p = tf_r.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = BRAND_BLUE
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "AI labs build the neural planners; LTTS builds the singularity-robust kinematics and safety filters that keep physical robots from destroying themselves.")
    set_notes(s, "Explain the Kinematics Moat. Point out the Yoshikawa manipulability formula: when mu(q) -> 0, joint velocity q-dot blows up. Explain why DLS filtering is mandatory.")
    return s


def slide_33_timing_and_safety_moat():
    s = new_slide()
    add_header(s, "Module 6 · The Bridge", "The Domain Engineering Moat: Deterministic Timing & Safety",
               "Real-time industrial fieldbus synchronization and statutory functional safety architecture.")

    card_w = 5.7
    gap = 0.33

    # Left: Deterministic Timing Boundaries
    add_card(s, 0.8, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, CYAN)
    add_badge(s, 1.05, 2.05, "REAL-TIME DETERMINISTIC BOUNDARIES", bg=BORDER_CYAN, fg=CYAN, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Sub-Millisecond Fieldbus Synchronization\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    points_time = [
        ("The Fieldbus Cycle Clock:", "Industrial fieldbuses—specifically Profinet IRT and EtherCAT—operate on deterministic cyclic synchronous positioning (CSP) clocks at 1ms to 2ms intervals."),
        ("The Jitter Constraint (< 1ms):", "If neural policy inference suffers from memory bus contention, garbage collection, or OS jitter exceeding 1ms, fieldbus communication watchdogs trip, throwing the entire production cell into an emergency halt."),
        ("The RTOS Hardware Interface:", "Deploying Physical AI requires architecting real-time operating system (RTOS / Xenomai / PREEMPT_RT) bridge layers running on industrial edge PCs paired with NVIDIA Jetson units."),
        ("Asynchronous Policy Buffering:", "Decoupling 50Hz neural inference from 1000Hz low-level servo interpolators through deterministic ring buffers.")
    ]
    for h, d in points_time:
        p = tf_l.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = CYAN
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Right: Functional Safety Architecture
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, GREEN)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "STATUTORY FUNCTIONAL SAFETY (PL e / SIL 3)", bg=BORDER_GREEN, fg=GREEN, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "Dual-Channel Safety & Hardware Interlocks\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(12); rr1.font.bold = True; rr1.font.color.rgb = INK_PRIMARY

    points_safe = [
        ("ISO 13849 & IEC 61508 Compliance:", "Global manufacturing safety regulations mandate Performance Level e (PL e) / Category 4 architecture for collaborative robotic cells."),
        ("Hardware-Gated Safety Envelopes:", "Neural policy outputs are never permitted direct, unmediated control of servo drives. They are wrapped in deterministic mathematical safety envelopes evaluated by certified safety controllers."),
        ("Dual-Channel Cross-Monitoring:", "Redundant safety channels independently monitor Cartesian joint speeds and payload force limits. If the AI policy breaches dynamic limits, hardware safety contacts de-energize the motor coils in < 15ms."),
        ("The Factory Insurance Gate:", "No automotive Tier-1 will sign off on an AI robot without an audited functional safety dossier approved by TÜV or UL.")
    ]
    for h, d in points_safe:
        p = tf_r.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = GREEN
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Sub-millisecond fieldbus timing and Cat 4 / PL e safety interlocks represent non-negotiable legal requirements that protect plant workers and equipment.")
    set_notes(s, "Detail Deterministic Timing and Safety Architecture. Explain EtherCAT jitter (<1ms) and ISO 13849 Cat 4 / PL e safety circuits.")
    return s


def slide_34_data_flywheel():
    s = new_slide()
    add_header(s, "Module 6 · The Bridge", "The Closed-Loop Operational Data Flywheel",
               "LTTS's 5-stage deployment architecture converting factory operations into continuously refined models.")

    stages = [
        ("STAGE 1", "Telemetry Ingestion", CYAN, BORDER_CYAN,
         "Logging high-frequency motor torques, currents, joint velocities, and visual streams directly from industrial fieldbuses in live production."),
        
        ("STAGE 2", "Physics Calibration", BRAND_NAVY, BORDER_SUBTLE,
         "Refining simulation physics parameters (friction coefficients, link backlash, payload inertia) by fitting sim models against real-world telemetry."),
        
        ("STAGE 3", "Synthetic Generation", GREEN, BORDER_GREEN,
         "Generating millions of extreme edge-case permutations, lighting shifts, and obstacle scenarios in NVIDIA Isaac Sim to train robust policies."),
        
        ("STAGE 4", "Edge Deployment", PURPLE, BORDER_PURPLE,
         "Deploying compressed INT4/FP8 quantized policies onto industrial edge hardware (NVIDIA Jetson) wrapped in deterministic safety envelopes."),
        
        ("STAGE 5", "OOD Feedback Loop", RED, BORDER_RED,
         "Detecting out-of-distribution (OOD) states in production; automatically routing failure telemetry back to Stage 2 for instant re-simulation.")
    ]

    card_w = 2.15
    gap = 0.245
    for i, (stg, title, color, border, desc) in enumerate(stages):
        left = 0.8 + i * (card_w + gap)
        top = 2.00
        card_h = 4.45

        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.15, top + 0.22, stg, bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.60), Inches(card_w - 0.3), Inches(0.85))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title; r.font.name = FONT_NAME; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = INK_PRIMARY

        tx_d = s.shapes.add_textbox(Inches(left + 0.15), Inches(top + 1.50), Inches(card_w - 0.3), Inches(2.7))
        tf_d = tx_d.text_frame; tf_d.word_wrap = True; tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        pd = tf_d.paragraphs[0]
        rd = pd.add_run(); rd.text = desc; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "The Flywheel creates permanent compounding advantage: every hour of plant operation makes LTTS's synthetic simulation models more accurate.")
    set_notes(s, "Explain the 5-stage Data Flywheel. This is the ultimate competitive advantage: Telemetry -> Physics Calibration -> Synthetic Data -> Edge Deploy -> OOD Monitoring.")
    return s


def slide_35_m7_divider():
    return section_divider_slide(
        7,
        "3–5 Year Structural Forecast",
        "Market Evolution Dynamics (2026–2030) & Critical Strategic Uncertainties",
        [
            "Four structural market forces reshaping robotics: commoditization to data exhaustion",
            "Hardware commoditization: value shifts irreversibly to software & systems integration",
            "Robotics foundation models consolidate into 2 to 3 hyperscale ecosystems",
            "Key sources of uncertainty: regulatory caging mandates, geopolitical decoupling, and sim-to-real progress"
        ]
    )


def slide_36_market_evolution():
    s = new_slide()
    add_header(s, "Module 7 · Structural Forecast", "Market Evolution Dynamics (2026–2030): Four Shifts",
               "Structural forces shifting economic value across the global Physical AI technology stack.")

    shifts = [
        ("1. Rapid Hardware Commoditization", CYAN, BORDER_CYAN,
         "Value Migrates from Metal to Software & Integration",
         "Standard 6-DOF robotic arms, parallel grippers, and mobile AMR bases will commoditize rapidly due to aggressive Asian manufacturing scale.",
         "As hardware margins compress toward 15%-20%, the vast majority of economic profit pools will shift irreversibly to upstream software intelligence, simulation, and brownfield systems integration."),

        ("2. Model Layer Consolidation", BRAND_NAVY, BORDER_SUBTLE,
         "Consolidation into 2 to 3 Hyperscale Ecosystems",
         "The robotics foundation model layer will follow the path of LLMs, consolidating into 2 to 3 dominant ecosystems (NVIDIA, Google DeepMind, and 1-2 venture leaders).",
         "Proprietary model training from scratch will become economically unviable for engineering service providers. LTTS should partner with dominant foundation builders rather than training 50B models."),

        ("3. Integration Layer Fragmentation", GREEN, BORDER_GREEN,
         "A Fragmented, High-Margin Bastion for ER&D",
         "Unlike consumer software, factory floors cannot be standardized with a single universal API.",
         "Heterogeneous factory layouts, bespoke mechanical tooling, legacy PLCs, and unique plant safety rules ensure systems integration remains an intensely fragmented, high-margin domain favoring specialized engineering firms."),

        ("4. The Data Exhaustion Pivot", PURPLE, BORDER_PURPLE,
         "Proprietary Telemetry & Synthetic Simulation Win",
         "As public internet text corpora are fully exhausted by frontier LLMs, the AI capability frontier pivots entirely to physical world interaction.",
         "Proprietary physical telemetry and high-fidelity synthetic simulation data become the primary determinants of competitive advantage. Whoever owns calibrated industrial CAD digital twins holds the training data moat.")
    ]

    card_w = 5.7
    gap = 0.33
    for i, (title, color, border, sub, p1, p2) in enumerate(shifts):
        col = i % 2
        row = i // 2
        left = 0.8 + col * (card_w + gap)
        top = 1.85 + row * 2.45
        card_h = 2.30

        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(card_w - 0.4), Inches(0.65))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = title + "\n"; r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run(); r2.text = sub; r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_b = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.85), Inches(card_w - 0.4), Inches(1.35))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        pb1 = tf_b.paragraphs[0]
        rb1 = pb1.add_run(); rb1.text = p1 + " "; rb1.font.name = FONT_NAME; rb1.font.size = Pt(9); rb1.font.color.rgb = TEXT_LIGHT
        pb2 = tf_b.add_paragraph()
        pb2.space_before = Pt(3)
        rb2 = pb2.add_run(); rb2.text = p2; rb2.font.name = FONT_NAME; rb2.font.size = Pt(8.8); rb2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "Hardware commoditizes; models consolidate; but integration remains permanently fragmented and highly profitable.")
    set_notes(s, "Explain the 4 Market Evolution dynamics. Crucial takeaway: Hardware becomes cheap; foundation models consolidate; the integration moat grows wider.")
    return s


def slide_37_sources_of_uncertainty():
    s = new_slide()
    add_header(s, "Module 7 · Structural Forecast", "Key Sources of Uncertainty: Three Strategic Wildcards",
               "External regulatory, geopolitical, and technical vectors that could disrupt deployment timelines.")

    wildcards = [
        ("1. Regulatory Caging Mandates", RED, BORDER_RED,
         "The Collaborative Safety Precedent",
         "If occupational safety regulators (OSHA in the US, EU Machinery Directive) mandate that autonomous AI-driven mobile humanoids must operate inside physical caging or interlocked optical light curtains, adoption timelines for unconstrained collaborative workers will extend by 3 to 5 years.",
         "Strategic Impact: Validates LTTS's focus on structured manufacturing cells and functional safety V&V."),

        ("2. Geopolitical & Compute Decoupling", AMBER, BORDER_AMBER,
         "Export Restrictions & Dual Ecosystems",
         "Expanding semiconductor export controls on advanced training GPUs (NVIDIA B200/H100) and edge accelerators (Jetson AGX) could bifurcate Western and Asian Physical AI ecosystems.",
         "Strategic Impact: LTTS must maintain multi-vendor integration capability across both Western (NVIDIA, Intel) and sovereign/regional compute architectures to insulate global operations."),

        ("3. Sim-to-Real Progress in Contact Physics", CYAN, BORDER_CYAN,
         "The Differentiable Physics Trajectory",
         "The rate at which differentiable physics engines solve complex contact-rich mechanical assembly (sub-millimeter snap fits, deformable routing) will dictate how rapidly synthetic training replaces manual robot programming.",
         "Strategic Impact: If progress is rapid, SD-FaaS scales aggressively in Q3 2027; if slow, manual integration engineering remains dominant even longer.")
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, desc, imp) in enumerate(wildcards):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.2, top + 0.22, f"STRATEGIC WILDCARD {i+1}", bg=border, fg=color, font_size=8.5, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.60), Inches(card_w - 0.4), Inches(0.85))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = title + "\n"; r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run(); r2.text = sub; r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_b = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.55), Inches(card_w - 0.4), Inches(3.0))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True; tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        pb1 = tf_b.paragraphs[0]
        rb1 = pb1.add_run(); rb1.text = desc + "\n\n"; rb1.font.name = FONT_NAME; rb1.font.size = Pt(9.2); rb1.font.color.rgb = TEXT_LIGHT
        pb2 = tf_b.add_paragraph()
        rb2 = pb2.add_run(); rb2.text = imp; rb2.font.name = FONT_NAME; rb2.font.size = Pt(9); rb2.font.bold = True; rb2.font.color.rgb = BRAND_NAVY

    add_takeaway(s, "All three uncertainties reinforce LTTS's core value: safety certification, multi-architecture integration, and synthetic simulation.")
    set_notes(s, "Explain the 3 Sources of Uncertainty. Note that even in downside scenarios (e.g. strict caging mandates), LTTS's safety verification business benefits.")
    return s
