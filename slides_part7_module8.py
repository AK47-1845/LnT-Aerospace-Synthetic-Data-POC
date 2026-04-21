"""
Slides Part 7: Module 8 — Integrated Recommendations & Bottom-Up Budgets (Slides 38 to 45)
Executive Editorial Light System: Crisp white canvas, 0.8" margins, deep ink typography, Navy conclusion anchor.
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

def slide_38_m8_divider():
    return section_divider_slide(
        8,
        "Strategic Recommendations for LTTS",
        "Strategic Roadmap, Phasing Rationale, and Bottom-Up Cost Breakdown",
        [
            "Sequencing rationale: capital efficiency, client safety dependency, and operational access",
            "Priority 1: Physical AI Verification & Validation (V&V) practice with automated safety dossiers",
            "Priority 2: Strategic alliances with incumbent PLCs (Siemens, Rockwell) & frontier AI labs",
            "Priority 3: Domain-specific synthetic data factories (SD-FaaS) monetizing enterprise CAD",
            "Priority 4: Physical AI Center of Excellence upskilling 250 engineers with lateral PhD hiring",
            "Full execution roadmap and phased budget breakdown ($2.8M + $1.3M + $4.2M + $2.5M/yr)"
        ]
    )


def slide_39_phasing_rationale():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Strategic Phasing Rationale & Investment Sequencing",
               "The sequencing of LTTS's Physical AI initiatives across 2027 is mathematically disciplined.")

    drivers = [
        ("Driver 1: Capital Efficiency", GREEN, BORDER_GREEN,
         "Lowest Capital Entry First",
         "Launching V&V first ($2.8M) requires dramatically less capital than building large compute clusters ($4.2M). It generates immediate revenue from existing automotive and aerospace clients in Q1 2027 to help self-fund subsequent phases."),

        ("Driver 2: Client Safety Dependency", BRAND_NAVY, BORDER_SUBTLE,
         "Solving the Immediate Regulatory Bottleneck",
         "Tier-1 industrial clients are currently paralyzed by safety certification bottlenecks for AI controllers. Establishing formal verification credentials builds the rigorous methodology required before deploying synthetic data models."),

        ("Driver 3: Operational Access Prerequisites", BRAND_BLUE, BORDER_CYAN,
         "Unlocking Client Plant Floors & CAD Repositories",
         "Siemens and Rockwell will only certify integrators possessing verified safety credentials (Priority 1). Once certified (Priority 2), these alliances unlock direct access to client CAD/PLM repositories needed to power the Synthetic Data Factory (Priority 3).")
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, desc) in enumerate(drivers):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 2.45
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, left, top, card_w, 0.025, color)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(card_w - 0.4), Inches(0.65))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = title + "\n"; r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run(); r2.text = sub; r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_d = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.85), Inches(card_w - 0.4), Inches(1.5))
        tf_d = tx_d.text_frame; tf_d.word_wrap = True; tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        pd = tf_d.paragraphs[0]
        rd = pd.add_run(); rd.text = desc; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Phased Timeline Diagram Card Below
    add_card(s, 0.8, 4.45, 11.73, 2.20, bg=BG_CARD_ALT, border=BORDER_SUBTLE, border_width=0.75)
    tx_t = s.shapes.add_textbox(Inches(1.05), Inches(4.55), Inches(11.23), Inches(0.35))
    tf_t = tx_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    pt = tf_t.paragraphs[0]
    rt = pt.add_run()
    rt.text = "SEQUENTIAL INITIATIVE EXECUTION TIMELINE (2027):"
    rt.font.name = FONT_NAME; rt.font.size = Pt(10.5); rt.font.bold = True; rt.font.color.rgb = BRAND_NAVY

    timeline_steps = [
        ("Q1 2027", "PRIORITY 1: V&V PRACTICE", "$2.8M Budget", "Launch HIL testbenches & automated safety compiler; establish TÜV SÜD partnership.", GREEN),
        ("Q2 2027", "PRIORITY 2: PLC ALLIANCES", "$1.3M Budget", "Joint integration labs with Siemens & Rockwell; deploy Orin edge testbeds.", BRAND_BLUE),
        ("Q3 2027", "PRIORITY 3: SYNTHETIC FACTORY", "$4.2M Budget", "Commission 64-GPU Omniverse cluster; automate CAD/PLM digital twin ingestion.", BRAND_NAVY),
        ("ONGOING", "PRIORITY 4: TALENT COE", "$2.5M/yr Budget", "Upskill 250 engineers across ROS2/Isaac; hire 5 PhD specialists; academic links.", PURPLE)
    ]

    t_w = 2.70
    t_gap = 0.24
    for j, (quarter, name, bud, detail, clr) in enumerate(timeline_steps):
        t_left = 1.05 + j * (t_w + t_gap)
        add_card(s, t_left, 4.95, t_w, 1.55, bg=COLOR_WHITE, border=BORDER_SUBTLE, border_width=0.75)
        add_rect(s, t_left, 4.95, t_w, 0.025, clr)

        tx_s = s.shapes.add_textbox(Inches(t_left + 0.12), Inches(5.05), Inches(t_w - 0.24), Inches(1.35))
        tf_s = tx_s.text_frame; tf_s.word_wrap = True; tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0

        p1 = tf_s.paragraphs[0]
        rp1 = p1.add_run(); rp1.text = quarter + "  ·  " + bud + "\n"; rp1.font.name = FONT_NAME; rp1.font.size = Pt(9); rp1.font.bold = True; rp1.font.color.rgb = clr
        rp2 = p1.add_run(); rp2.text = name + "\n"; rp2.font.name = FONT_NAME; rp2.font.size = Pt(9.5); rp2.font.bold = True; rp2.font.color.rgb = INK_PRIMARY
        
        p2 = tf_s.add_paragraph()
        p2.space_before = Pt(3)
        rp3 = p2.add_run(); rp3.text = detail; rp3.font.name = FONT_NAME; rp3.font.size = Pt(8.5); rp3.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "A disciplined three-stage progression: build safety credibility in Q1, secure plant alliances in Q2, scale compute in Q3.")
    set_notes(s, "Explain the Phasing Rationale. Emphasize why V&V must come before Synthetic Data: safety credentials are the key that unlocks client plant access.")
    return s


def slide_40_priority1_vv():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Priority 1: Physical AI Verification & Validation (V&V)",
               "Q1 2027 Launch  ·  Establishing the industry's premier neural safety certification practice.")

    card_w = 5.7
    gap = 0.33

    # Left: Formal Mathematical Deliverable
    add_card(s, 0.8, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, GREEN)
    add_badge(s, 1.05, 2.05, "CORE DELIVERABLE: AUTOMATED SAFETY DOSSIER COMPILER", bg=BORDER_GREEN, fg=GREEN, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run(); r1.text = "Formal Mathematical Specification:\n"; r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
    r2 = p1.add_run(); r2.text = "For any neural policy u = pi_theta(o) controlling continuous dynamics x_dot = f(x, u), the compiler evaluates Control Barrier Functions (CBFs) to formally certify safety against safe set C:"; r2.font.name = FONT_NAME; r2.font.size = Pt(9.2); r2.font.color.rgb = TEXT_LIGHT

    # Math Image 1: CBF Equation (Deep Ink)
    add_card(s, 1.05, 3.25, card_w - 0.5, 0.65, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
    add_math_image(s, r'\dot{h}(x, u) = \nabla h(x) \cdot f(x, \pi_\theta(x)) \geq -\alpha(h(x))', 1.20, 3.35, fontsize=15, color='#0F172A', max_h=0.45)

    tx_l2 = s.shapes.add_textbox(Inches(1.05), Inches(4.05), Inches(card_w - 0.5), Inches(2.4))
    tf_l2 = tx_l2.text_frame; tf_l2.word_wrap = True; tf_l2.margin_left = tf_l2.margin_right = tf_l2.margin_top = tf_l2.margin_bottom = 0
    p2 = tf_l2.paragraphs[0]
    r3 = p2.add_run(); r3.text = "Forward Reachable Set Verification via alpha,beta-CROWN:\n"; r3.font.name = FONT_NAME; r3.font.size = Pt(10.5); r3.font.bold = True; r3.font.color.rgb = INK_PRIMARY
    r4 = p2.add_run(); r4.text = "The software computes bounded forward reachable sets R(T; X0) via interval neural network bound propagation, mathematically guaranteeing that R(T; X0) subset of C for all initial operating conditions X0."; r4.font.name = FONT_NAME; r4.font.size = Pt(9); r4.font.color.rgb = TEXT_LIGHT

    # Math Image 2: Safe Reachable Set (Deep Ink)
    add_card(s, 1.05, 4.95, card_w - 0.5, 0.60, bg=BG_CARD_ALT, border=BORDER_SUBTLE)
    add_math_image(s, r'\mathcal{R}(T; \mathcal{X}_0) \subseteq \mathcal{C} = \{x \in \mathbb{R}^n \mid h(x) \geq 0\}', 1.30, 5.05, fontsize=15, color='#0F172A', max_h=0.40)

    tx_l3 = s.shapes.add_textbox(Inches(1.05), Inches(5.70), Inches(card_w - 0.5), Inches(0.80))
    tf_l3 = tx_l3.text_frame; tf_l3.word_wrap = True; tf_l3.margin_left = tf_l3.margin_right = tf_l3.margin_top = tf_l3.margin_bottom = 0
    p3 = tf_l3.paragraphs[0]
    r5 = p3.add_run()
    r5.text = "Standard Compliance: Generates automated functional safety dossiers satisfying ISO 13849 (Cat 4 / PL e) and IEC 61508 without requiring millions of physical test trials."
    r5.font.name = FONT_NAME; r5.font.size = Pt(9); r5.font.color.rgb = TEXT_LIGHT

    # Right: Bottom-Up Budget Breakdown
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, BRAND_NAVY)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "BOTTOM-UP BUDGET: $2.8M TOTAL", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "Target Range: $2.0M - $3.5M [Estimated]\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = BRAND_NAVY

    items_b = [
        ("HIL Testbenches ($800k):", "Two multi-axis industrial robot test cells equipped with optical motion capture, torque dynamometers, and real-time dSPACE/Speedgoat controllers for physical validation."),
        ("Verification Tooling Licenses ($400k):", "Formal methods software licenses, computational reachability engines, and interval bound propagation toolchains."),
        ("Core Engineering Team ($1.2M/yr):", "6 FTEs at blended $200k/yr loaded cost: 2 Lead TÜV-Certified Functional Safety Engineers, 2 Controls Engineers, and 2 Neural Network Verification Specialists."),
        ("Accredited Lab Certification ($400k):", "ISO/IEC 17025 laboratory accreditation and TÜV SÜD partnership audit fees to legally issue compliance dossiers.")
    ]
    for h, d in items_b:
        p = tf_r.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"✔ {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    p_tot = tf_r.add_paragraph()
    p_tot.space_before = Pt(8)
    rt1 = p_tot.add_run(); rt1.text = "TOTAL PHASE 1 BUDGET: $2.8M "; rt1.font.name = FONT_NAME; rt1.font.size = Pt(11); rt1.font.bold = True; rt1.font.color.rgb = GREEN
    rt2 = p_tot.add_run(); rt2.text = "(Anchored in $2.0M-$3.5M range)"; rt2.font.name = FONT_NAME; rt2.font.size = Pt(9.5); rt2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "Priority 1 transforms safety verification from an expensive physical trial-and-error process into an automated, mathematically certified software compiler.")
    set_notes(s, "Explain Priority 1. Detail the CBF formulation, alpha,beta-CROWN reachability, and the exact $2.8M budget components.")
    return s


def slide_41_priority2_alliances():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Priority 2: Strategic Alliances with Incumbent PLCs & AI Labs",
               "Q2 2027 Launch  ·  Establishing certified bridge partnerships with Siemens, Rockwell & frontier labs.")

    card_w = 5.7
    gap = 0.33

    # Left: Sequencing Rationale
    add_card(s, 0.8, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, BRAND_BLUE)
    add_badge(s, 1.05, 2.05, "SEQUENCING RATIONALE & VALUE CREATION", bg=BORDER_CYAN, fg=BRAND_BLUE, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Why PLC Alliances Follow V&V Launch:\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    points_p2 = [
        ("The Credential Prerequisite:", "Industrial automation giants (Siemens, Rockwell) will not partner with unproven service firms. They require systems integrators to possess verified functional safety credentials before certifying them as authorized AI bridge partners."),
        ("Unlocking Brownfield Access:", "Once certified, these alliances unlock direct access to brownfield client plant floors, proprietary PLC fieldbus protocols, and engineering CAD repositories."),
        ("Bilateral AI Lab Channel:", "Frontier AI labs (Physical Intelligence, Skild AI) lack field systems engineering. LTTS becomes their designated deployment arm for enterprise manufacturing rollouts."),
        ("Target Output:", "Become the preferred global deployment partner for Siemens TIA Portal Industrial Copilot and Rockwell FactoryTalk Physical AI extensions.")
    ]
    for h, d in points_p2:
        p = tf_l.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = BRAND_BLUE
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Right: Bottom-Up Budget
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, BRAND_NAVY)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "BOTTOM-UP BUDGET: $1.3M TOTAL", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "Target Range: $1.0M - $1.5M [Estimated]\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = BRAND_NAVY

    items_b2 = [
        ("Joint Integration Lab Hardware ($350k):", "Siemens S7-1500 and Rockwell ControlLogix racks with high-speed industrial fieldbus interface cards (Profinet IRT / EtherCAT) paired with edge NVIDIA Jetson AGX Orin units for real-time benchmark testing."),
        ("Alliance Solutions Architecture Team ($650k):", "3 dedicated senior FTEs: Siemens-Certified PLC Engineer, Rockwell-Certified Systems Engineer, and Edge AI Systems Architect."),
        ("Partner Enablement & Co-Marketing ($300k):", "Development of joint solution briefs, partner portal technical certifications, and live customer demonstration cells.")
    ]
    for h, d in items_b2:
        p = tf_r.add_paragraph()
        p.space_before = Pt(7)
        rh = p.add_run(); rh.text = f"✔ {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    p_tot2 = tf_r.add_paragraph()
    p_tot2.space_before = Pt(12)
    rt1 = p_tot2.add_run(); rt1.text = "TOTAL PHASE 2 BUDGET: $1.3M "; rt1.font.name = FONT_NAME; rt1.font.size = Pt(11); rt1.font.bold = True; rt1.font.color.rgb = GREEN
    rt2 = p_tot2.add_run(); rt2.text = "(Within $1.0M-$1.5M target range)"; rt2.font.name = FONT_NAME; rt2.font.size = Pt(9.5); rt2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "Priority 2 establishes joint integration testbeds with Siemens and Rockwell, locking in LTTS as the preferred field rollout partner.")
    set_notes(s, "Explain Priority 2. Detail how Siemens S7-1500 and Rockwell ControlLogix racks are paired with NVIDIA Jetson AGX Orin in the joint lab.")
    return s


def slide_42_priority3_synthetic_data():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Priority 3: Domain-Specific Synthetic Data Factories",
               "Q3 2027 Pilot  ·  Industrial CAD/PLM digital twin ingestion & policy pre-training engine.")

    card_w = 5.7
    gap = 0.33

    # Left: Sequencing Rationale
    add_card(s, 0.8, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, BRAND_NAVY)
    add_badge(s, 1.05, 2.05, "SEQUENCING RATIONALE & SD-FAAS", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Why Synthetic Data Launches in Q3:\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    points_p3 = [
        ("Capital & Compute Concentration:", "Synthetic data generation requires substantial GPU infrastructure and specialized simulation engineering investment ($4.2M)."),
        ("Leveraging Prior Phases:", "By scheduling this for Q3 2027, the practice directly leverages the CAD/PLM customer access unlocked by Q2 PLC alliances, and the physical validation frameworks built in Q1."),
        ("Automated CAD Ingestion Pipeline:", "Ingests client 3D assemblies (Siemens NX, Teamcenter, CATIA) and automatically generates contact-calibrated digital twin environments in NVIDIA Isaac Sim."),
        ("Extreme Domain Randomization:", "Trains robust vision-action policies across millions of lighting, texture, and physical friction variations before any physical hardware arrives.")
    ]
    for h, d in points_p3:
        p = tf_l.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = BRAND_NAVY
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Right: Bottom-Up Budget
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, GREEN)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "BOTTOM-UP BUDGET: $4.2M TOTAL", bg=BORDER_GREEN, fg=GREEN, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "Target Range: $3.0M - $5.0M [Estimated]\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = INK_PRIMARY

    items_b3 = [
        ("Simulation Compute Cluster ($2.2M):", "Dedicated on-premise/hybrid GPU simulation cluster (64 high-end GPUs) engineered for high-throughput Isaac Sim / Omniverse physics rendering and parallel policy generation."),
        ("Simulation Software Enterprise Licensing ($500k):", "NVIDIA Omniverse Enterprise, Siemens Tecnomatix CAD ingestion toolchains, and proprietary mesh processing software."),
        ("Simulation Engineering Team ($1.5M/yr):", "8 dedicated engineering FTEs: 3D CAD/Meshing Specialists, Differentiable Physics Engineers, and Domain Randomization ML Engineers.")
    ]
    for h, d in items_b3:
        p = tf_r.add_paragraph()
        p.space_before = Pt(7)
        rh = p.add_run(); rh.text = f"✔ {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    p_tot3 = tf_r.add_paragraph()
    p_tot3.space_before = Pt(12)
    rt1 = p_tot3.add_run(); rt1.text = "TOTAL PHASE 3 BUDGET: $4.2M "; rt1.font.name = FONT_NAME; rt1.font.size = Pt(11); rt1.font.bold = True; rt1.font.color.rgb = GREEN
    rt2 = p_tot3.add_run(); rt2.text = "(Within $3.0M-$5.0M target range)"; rt2.font.name = FONT_NAME; rt2.font.size = Pt(9.5); rt2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "Priority 3 transforms enterprise CAD databases into high-margin Synthetic Data Factory as a Service (SD-FaaS) recurring revenues.")
    set_notes(s, "Explain Priority 3. Emphasize the 64-GPU compute cluster and how automated CAD ingestion turns static drawings into dynamic digital twins.")
    return s


def slide_43_priority4_coe():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Priority 4: Physical AI Engineering Center of Excellence",
               "Ongoing Baseline  ·  Cross-training 250 engineers, lateral PhD hiring, and academic fellowships.")

    card_w = 5.7
    gap = 0.33

    # Left: Sequencing Rationale
    add_card(s, 0.8, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, card_w, 0.025, PURPLE)
    add_badge(s, 1.05, 2.05, "FOUNDATIONAL TALENT STRATEGY", bg=BORDER_PURPLE, fg=PURPLE, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_l = tx_l.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "The Hybrid Mechatronics + AI Talent Bench:\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    points_p4 = [
        ("The Industry Talent Scarcity:", "There are virtually zero engineers who understand both PyTorch reinforcement learning and Siemens S7 ladder logic. Pure ML engineers lack controls knowledge; automation engineers lack neural network training skills."),
        ("Underpinning All Commercial Pillars:", "Continuous talent upskilling underpins Priorities 1, 2, and 3 from day one, systematically cross-training LTTS's mechatronics bench into robotics AI."),
        ("Structured 250-Engineer Cohort:", "Cross-training 250 senior mechatronics and controls engineers into ROS2, Isaac Lab, PyTorch, and edge quantization at $4k per engineer."),
        ("Creating the Long-Term Moat:", "A hybrid workforce that cannot be replicated by software consultancies or traditional IT services firms.")
    ]
    for h, d in points_p4:
        p = tf_l.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run(); rh.text = f"• {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = PURPLE
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Right: Bottom-Up Budget
    add_card(s, 0.8 + card_w + gap, 1.85, card_w, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8 + card_w + gap, 1.85, card_w, 0.025, BRAND_NAVY)
    add_badge(s, 0.8 + card_w + gap + 0.25, 2.05, "ANNUAL COE BUDGET: $2.5M/YR TOTAL", bg=BORDER_SUBTLE, fg=BRAND_NAVY, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(0.8 + card_w + gap + 0.25), Inches(2.40), Inches(card_w - 0.5), Inches(4.0))
    tf_r = tx_r.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "Target Range: $2.0M - $3.0M/yr [Estimated]\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = BRAND_NAVY

    items_b4 = [
        ("Structured Upskilling Curriculum ($1.0M/yr):", "Formal intensive training of 250 senior engineers across PyTorch, ROS2, Isaac Lab, and embedded edge quantization ($4,000 per engineer loaded program cost)."),
        ("Specialized Lateral Hiring ($1.2M/yr):", "Recruiting 5 Principal Research Engineers and Ph.D. technical leads in Embodied AI, Differentiable Physics, and Formal Safety Verification."),
        ("Academic Research Fellowships ($300k/yr):", "Sponsored research partnerships and doctoral fellowships with leading robotics laboratories (IISc Bangalore, IIT Madras/Bombay, and Stanford/CMU affiliates).")
    ]
    for h, d in items_b4:
        p = tf_r.add_paragraph()
        p.space_before = Pt(7)
        rh = p.add_run(); rh.text = f"✔ {h} "; rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = INK_PRIMARY
        rd = p.add_run(); rd.text = d; rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    p_tot4 = tf_r.add_paragraph()
    p_tot4.space_before = Pt(12)
    rt1 = p_tot4.add_run(); rt1.text = "TOTAL ANNUAL COE BUDGET: $2.5M/yr "; rt1.font.name = FONT_NAME; rt1.font.size = Pt(11); rt1.font.bold = True; rt1.font.color.rgb = GREEN
    rt2 = p_tot4.add_run(); rt2.text = "(Within $2.0M-$3.0M target range)"; rt2.font.name = FONT_NAME; rt2.font.size = Pt(9.5); rt2.font.color.rgb = TEXT_MUTED

    add_takeaway(s, "The CoE builds the world's largest certified workforce of hybrid mechatronics-plus-AI engineers, cementing LTTS's long-term competitive moat.")
    set_notes(s, "Explain Priority 4. Highlight the 250 engineer upskilling program ($1.0M), 5 PhD lateral hires ($1.2M), and $300k in university fellowships.")
    return s


def slide_44_roadmap_table():
    s = new_slide()
    add_header(s, "Module 8 · Strategic Roadmap", "Integrated Strategic Roadmap & Phased Budget Allocation (Table 5)",
               "Comprehensive execution timeline, strategic capabilities, target deliverables, and capital deployment.")

    left_m = 0.8
    top_base = 1.80
    total_w = 11.73

    # Column widths summing to 11.73"
    col_w = [2.60, 1.35, 3.48, 2.70, 1.60]
    col_x = [left_m]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    # Header Row (Deep Navy)
    hdr_h = 0.38
    add_rect(s, left_m, top_base, total_w, hdr_h, BRAND_NAVY)

    headers = [
        "STRATEGIC INITIATIVE",
        "TIMELINE",
        "STRATEGIC FOCUS & CAPABILITY",
        "TARGET DELIVERABLE",
        "PHASED BUDGET"
    ]

    for j, (h_text, x_pos, w) in enumerate(zip(headers, col_x, col_w)):
        tx = s.shapes.add_textbox(Inches(x_pos + 0.10), Inches(top_base + 0.05), Inches(w - 0.20), Inches(hdr_h - 0.10))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = h_text; r.font.name = FONT_NAME; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = COLOR_WHITE

    milestones = [
        ("Priority 1: V&V Practice",
         "Q1 2027",
         "Functional safety auditing, CBF evaluation & interval bound reachability certification",
         "Automated Safety Dossier Compiler & certified lab testing under ISO 13849 / IEC 61508",
         "$2.8M Phase 1",
         GREEN),

        ("Priority 2: PLC Alliances",
         "Q2 2027",
         "Joint integration testbeds with Siemens S7-1500 & Rockwell ControlLogix architectures",
         "Certified bridge middleware connecting neural policies to industrial fieldbuses",
         "$1.3M Phase 2",
         BRAND_BLUE),

        ("Priority 3: Synthetic Data Factory",
         "Q3 2027",
         "Digital twin simulation (SD-FaaS) monetizing enterprise CAD/PLM engineering assemblies",
         "Dedicated 64-GPU Omniverse cluster generating contact-calibrated simulation policies",
         "$4.2M Phase 3",
         BRAND_NAVY),

        ("Priority 4: Hybrid Talent CoE",
         "Ongoing",
         "Cross-training mechatronics bench into robotics AI; recruiting 5 lateral Ph.D. specialists",
         "250-engineer hybrid workforce bridging controls engineering with deep learning",
         "$2.5M/yr Annual",
         PURPLE)
    ]

    row_h = 1.00
    for i, (init, time, focus, outcome, budget, color) in enumerate(milestones):
        row_top = top_base + hdr_h + i * row_h
        row_bg = BG_CARD if i % 2 == 0 else COLOR_WHITE

        add_card(s, left_m, row_top, total_w, row_h, bg=row_bg, border=BORDER_SUBTLE, border_width=0.5)

        # Col 0: Initiative
        tx0 = s.shapes.add_textbox(Inches(col_x[0] + 0.12), Inches(row_top + 0.15), Inches(col_w[0] - 0.20), Inches(row_h - 0.30))
        tf0 = tx0.text_frame; tf0.word_wrap = True; tf0.margin_left = tf0.margin_right = tf0.margin_top = tf0.margin_bottom = 0
        p0 = tf0.paragraphs[0]
        r0 = p0.add_run(); r0.text = init; r0.font.name = FONT_NAME; r0.font.size = Pt(10.5); r0.font.bold = True; r0.font.color.rgb = INK_PRIMARY

        # Col 1: Timeline
        tx1 = s.shapes.add_textbox(Inches(col_x[1] + 0.08), Inches(row_top + 0.22), Inches(col_w[1] - 0.16), Inches(row_h - 0.35))
        tf1 = tx1.text_frame; tf1.word_wrap = True; tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
        p1 = tf1.paragraphs[0]
        r1 = p1.add_run(); r1.text = time; r1.font.name = FONT_NAME; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = color

        # Col 2: Strategic Focus
        tx2 = s.shapes.add_textbox(Inches(col_x[2] + 0.10), Inches(row_top + 0.12), Inches(col_w[2] - 0.20), Inches(row_h - 0.24))
        tf2 = tx2.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        r2 = p2.add_run(); r2.text = focus; r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.color.rgb = TEXT_LIGHT

        # Col 3: Target Deliverable
        tx3 = s.shapes.add_textbox(Inches(col_x[3] + 0.10), Inches(row_top + 0.12), Inches(col_w[3] - 0.20), Inches(row_h - 0.24))
        tf3 = tx3.text_frame; tf3.word_wrap = True; tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0
        p3 = tf3.paragraphs[0]
        r3 = p3.add_run(); r3.text = outcome; r3.font.name = FONT_NAME; r3.font.size = Pt(9); r3.font.color.rgb = TEXT_LIGHT

        # Col 4: Phased Budget
        tx4 = s.shapes.add_textbox(Inches(col_x[4] + 0.08), Inches(row_top + 0.22), Inches(col_w[4] - 0.16), Inches(row_h - 0.35))
        tf4 = tx4.text_frame; tf4.word_wrap = True; tf4.margin_left = tf4.margin_right = tf4.margin_top = tf4.margin_bottom = 0
        p4 = tf4.paragraphs[0]
        r4 = p4.add_run(); r4.text = budget; r4.font.name = FONT_NAME; r4.font.size = Pt(10); r4.font.bold = True; r4.font.color.rgb = BRAND_NAVY

    # Program Summary Total Card
    add_card(s, left_m, 6.30, total_w, 0.65, bg=BG_CARD_ALT, border=BORDER_SUBTLE, border_width=0.75)
    tx_sum = s.shapes.add_textbox(Inches(left_m + 0.20), Inches(6.38), Inches(total_w - 0.40), Inches(0.50))
    tf_sum = tx_sum.text_frame; tf_sum.word_wrap = True; tf_sum.margin_left = tf_sum.margin_right = tf_sum.margin_top = tf_sum.margin_bottom = 0
    psum = tf_sum.paragraphs[0]
    rsum1 = psum.add_run(); rsum1.text = "TOTAL 2027 PROGRAM INVESTMENT: "; rsum1.font.name = FONT_NAME; rsum1.font.size = Pt(10); rsum1.font.bold = True; rsum1.font.color.rgb = BRAND_NAVY
    rsum2 = psum.add_run(); rsum2.text = "$8.3M Phased Capex ($2.8M V&V + $1.3M Alliances + $4.2M Data Factory) + $2.5M/yr Ongoing CoE Baseline. Every dollar is directly anchored in customer revenue expansion."; rsum2.font.name = FONT_NAME; rsum2.font.size = Pt(9); rsum2.font.color.rgb = TEXT_LIGHT

    set_notes(s, "Table 5 Strategic Roadmap. Summarize the total $8.3M phased investment and $2.5M/yr CoE budget. Point out the clear milestone gates.")
    return s


def slide_45_strategic_conclusion():
    s = new_slide(bg_color=BRAND_NAVY)
    
    # Left accent gold bar
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()

    # Top badge
    add_badge(s, 0.8, 0.75, "STRATEGIC CONCLUSION  ·  BOARDROOM ACTION CALL", bg=RGBColor(0x00, 0x1E, 0x33), fg=GOLD, font_size=9, bold=True)

    # Big Headline
    tx_t = s.shapes.add_textbox(Inches(0.8), Inches(1.30), Inches(11.5), Inches(1.5))
    tf_t = tx_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p = tf_t.paragraphs[0]
    r = p.add_run()
    r.text = "The future of industrial automation\nis Physical Artificial Intelligence."
    r.font.name = FONT_NAME; r.font.size = Pt(36); r.font.bold = True; r.font.color.rgb = COLOR_WHITE

    div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.05), Inches(8.0), Inches(0.015))
    div.fill.solid(); div.fill.fore_color.rgb = GOLD; div.line.fill.background()

    tx_c = s.shapes.add_textbox(Inches(0.8), Inches(3.30), Inches(11.5), Inches(2.1))
    tf_c = tx_c.text_frame; tf_c.word_wrap = True; tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    pc = tf_c.paragraphs[0]
    rc1 = pc.add_run()
    rc1.text = "The strategic opportunity for L&T Technology Services is not to manufacture commoditizing robot hardware, nor to compete in multi-billion-dollar foundational model training.\n\n"
    rc1.font.name = FONT_NAME; rc1.font.size = Pt(13); rc1.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    rc2 = pc.add_run()
    rc2.text = "The definitive opportunity for LTTS is to become the indispensable, trusted engineering bridge that verifies, integrates, and deploys Physical AI safely at scale."
    rc2.font.name = FONT_NAME; rc2.font.size = Pt(16); rc2.font.bold = True; rc2.font.color.rgb = GOLD

    # 4 Closing Pillars across the bottom
    pillars = [
        ("1. VERIFY (Q1 2027)", "Formal Safety Dossiers & CBF reachability certification under ISO 13849 / IEC 61508.", GREEN),
        ("2. INTEGRATE (Q2 2027)", "Certified PLC bridge middleware with Siemens S7-1500 & Rockwell ControlLogix.", RGBColor(0x38, 0xBD, 0xF8)),
        ("3. SCALE (Q3 2027)", "Domain-Specific Synthetic Data Factories monetizing enterprise CAD/PLM assemblies.", GOLD),
        ("4. EMPOWER (Ongoing)", "Center of Excellence cross-training 250+ hybrid mechatronics-plus-AI engineers.", RGBColor(0xC0, 0x84, 0xFC)),
    ]

    p_w = 2.75
    p_gap = 0.24
    p_top = 5.65
    p_h = 1.35

    for i, (title, desc, color) in enumerate(pillars):
        x = 0.8 + i * (p_w + p_gap)
        add_card(s, x, p_top, p_w, p_h, bg=RGBColor(0x04, 0x33, 0x54), border=RGBColor(0x0C, 0x4A, 0x73))
        add_rect(s, x, p_top, p_w, 0.02, color)

        tx = s.shapes.add_textbox(Inches(x + 0.12), Inches(p_top + 0.12), Inches(p_w - 0.24), Inches(p_h - 0.20))
        tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title + "\n"; r.font.name = FONT_NAME; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = color
        p_desc = tf.add_paragraph()
        p_desc.space_before = Pt(3)
        r = p_desc.add_run(); r.text = desc; r.font.name = FONT_NAME; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0xF1, 0xF5, 0xF9)

    set_notes(s, "Conclusion Slide. Deliver the final punchline: LTTS is the trusted engineering bridge that verifies, integrates, and deploys Physical AI safely at scale.")
    return s
