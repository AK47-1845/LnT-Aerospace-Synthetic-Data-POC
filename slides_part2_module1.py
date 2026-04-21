"""
Slides Part 2: Module 1 — Commercial State Mapping (Slides 5 to 11)
Executive Editorial Light System: Crisp white canvas, 0.8" margins, deep ink typography.
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from deck_common import (
    new_slide, add_card, add_rect, add_header, add_takeaway, add_stat_box,
    add_badge, set_notes, section_divider_slide, BG_CANVAS, BG_CARD, BG_CARD_ALT,
    BG_CARD_ACCENT, BORDER_SUBTLE, BORDER_GOLD, BORDER_CYAN, BORDER_GREEN,
    BORDER_AMBER, BORDER_RED, GOLD, CYAN, GREEN, AMBER, RED, PURPLE, WHITE,
    COLOR_WHITE, BRAND_NAVY, BRAND_BLUE, INK_PRIMARY, TEXT_LIGHT, TEXT_MUTED, FONT_NAME
)

def slide_05_m1_divider():
    return section_divider_slide(
        1,
        "Current State of Physical AI",
        "Commercial State Mapping, Disclosed Capital, and Maturity Asymmetry",
        [
            "Segmenting commercial reality into three strict operational tiers",
            "Disclosed capital deployment matrix across foundational models and simulation",
            "The capital vs. maturity asymmetry: the humanoid capital trap vs. infrastructure software",
            "Strategic implications for LTTS's upstream positioning"
        ]
    )

def slide_06_maturity_framework():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Operational Segmentation: Three Maturity Tiers",
               "Separating verifiable production reality from vendor marketing claims.")

    tiers = [
        ("Tier 1: Commercial Production at Scale", GREEN, BORDER_GREEN,
         "Continuous Revenue & Core Enterprise Workflows",
         "Deployments that operate continuously in production environments, driving core commercial revenue, integrated into live customer operations, and subject to formal commercial SLAs.",
         ["Autonomous Driving Motion Planning (Waymo, Tesla, Wayve)",
          "Industrial Quality & Surface Inspection (TSMC, semiconductor)",
          "Virtual Simulation & ADAS/ISO Validation (Applied Intuition, NVIDIA)"]),
        
        ("Tier 2: Active Customer Pilots", AMBER, BORDER_AMBER,
         "Pre-Production in Strictly Bounded Environments",
         "Field evaluations under controlled conditions with human supervision nearby. High media visibility but zero unconstrained production SLA commitments.",
         ["Humanoid sheet-metal insertion (Figure AI @ BMW Spartanburg)",
          "Humanoid parts assembly delivery (Apptronik @ Mercedes-Benz)",
          "Bipedal tote handling (Agility Digit @ Amazon BFI1 & GXO)",
          "Floor-loaded container unloading (Boston Dynamics Stretch @ DHL)"]),
        
        ("Tier 3: Lab Demonstrations & Claims", RED, BORDER_RED,
         "No Scale Deployment (Unconstrained Research Claims)",
         "Controlled laboratory proofs-of-concept. Frequently rely on curated videos, hand-tuned fixtures, or teleoperation assist. No production economic viability.",
         ["Zero-shot precision mechanical assembly (< 0.1mm clearance)",
          "Unstructured domestic tasks (autonomous laundry, cooking, tidying)",
          "General-purpose humanoid dexterity in dynamic unmapped environments"])
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, desc, bullets) in enumerate(tiers):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        # Refined hairline top rule
        add_rect(s, left, top, card_w, 0.025, color)

        add_badge(s, left + 0.2, top + 0.22, f"TIER {i+1}", bg=border, fg=color, font_size=9, bold=True)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.60), Inches(card_w - 0.4), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title.split(":")[1].strip() + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(12.5); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run()
        r2.text = sub
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_d = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.55), Inches(card_w - 0.4), Inches(1.1))
        tf_d = tx_d.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        pd = tf_d.paragraphs[0]
        rd = pd.add_run()
        rd.text = desc
        rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

        # Sub-bullets
        tx_b = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 2.75), Inches(card_w - 0.4), Inches(1.85))
        tf_b = tx_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        
        p_hdr = tf_b.paragraphs[0]
        r_hdr = p_hdr.add_run()
        r_hdr.text = "NOTABLE EXAMPLES IN 2026:"
        r_hdr.font.name = FONT_NAME; r_hdr.font.size = Pt(8.5); r_hdr.font.bold = True; r_hdr.font.color.rgb = TEXT_MUTED
        
        for b in bullets:
            pb = tf_b.add_paragraph()
            pb.space_before = Pt(4)
            rb1 = pb.add_run()
            rb1.text = "• "
            rb1.font.name = FONT_NAME; rb1.font.size = Pt(9); rb1.font.bold = True; rb1.font.color.rgb = color
            rb2 = pb.add_run()
            rb2.text = b
            rb2.font.name = FONT_NAME; rb2.font.size = Pt(9); rb2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Industrial enterprise buyers only pay for Tier 1 reliability. Pilot novelties (Tier 2) cannot be booked as scalable production revenue.")
    set_notes(s, "Explain the 3 tiers. Crucial distinction: Tier 1 makes real recurring revenue today; Tier 2 is funded by OEM R&D grants; Tier 3 is venture storytelling.")
    return s


def slide_07_tier1_deepdive():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Tier 1 Deep Dive: Commercial Production at Scale",
               "Three sectors where Physical AI actively generates recurring commercial revenue.")

    sectors = [
        ("Autonomous Driving Neural Motion Planning", GREEN, BORDER_GREEN,
         "Continuous Revenue Across Commercial Fleets",
         [
             ("Waymo Commercial Operations:", "Delivering over 150,000 paid commercial robotaxi trips per week across Phoenix, San Francisco, and Los Angeles with >1M autonomous miles weekly. Confirmed in Alphabet Q3 2024 Earnings Call by CEO Sundar Pichai [Verified]."),
             ("Tesla End-to-End Neural Driving:", "Deploying full neural network driving across consumer vehicle fleets, replacing rule-based planners with visual policy networks trained on billions of real-world video frames. Confirmed in Tesla Q2 2024 Shareholder Update [Verified]."),
             ("Wayve Commercial Delivery:", "Executing commercial grocery delivery trials with Ocado and Asda in the UK, operating end-to-end embodied foundation models in complex urban environments [Reported].")
         ]),
        
        ("Industrial Quality & Surface Inspection", CYAN, BORDER_CYAN,
         "High-Throughput Inline Defect Detection",
         [
             ("TSMC Lithography Defect Pipelines:", "Automated defect classification pipelines utilizing physics-informed vision to detect sub-surface nanoscale wafer defects during high-throughput fabrication [Reported]."),
             ("Semiconductor Yield Optimization:", "Closed-loop visual and thermal inspection systems predicting defect propagation across lithography stages, improving yield forecasting and tool uptime [Reported]."),
             ("Inline Battery Cell Inspection:", "Deployed at scale in EV battery gigafactories to detect micro-anomalies and weld defects under millisecond cycle times [Verified].")
         ]),
        
        ("Virtual Simulation & ADAS/ISO Validation", BRAND_NAVY, BORDER_SUBTLE,
         "Mission-Critical Enterprise Testing Software",
         [
             ("Applied Intuition Enterprise Suite:", "Powering end-to-end synthetic simulation, sensor modeling, and virtual compliance testing for global automotive Tier-1s and defense primes. Backed by $6B valuation and multi-million ARR [Verified]."),
             ("NVIDIA Isaac Sim & Omniverse:", "Enterprise digital twin simulation platform used for virtual commissioning, robot kinematics validation, and synthetic policy training under ISO 26262 and ISO 21448 [Verified]."),
             ("Regulatory Safety Compliance:", "Mandatory simulation testing suites replacing millions of risky physical road and factory trials with certified virtual benchmarks [Verified].")
         ])
    ]

    card_w = 3.68
    gap = 0.34
    for i, (title, color, border, sub, items) in enumerate(sectors):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        # Subtle top accent line
        add_rect(s, left, top, card_w, 0.025, color)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.22), Inches(card_w - 0.4), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "\n"
        r1.font.name = FONT_NAME; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY
        r2 = p.add_run()
        r2.text = sub
        r2.font.name = FONT_NAME; r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = color

        tx_body = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.25), Inches(card_w - 0.4), Inches(3.3))
        tf_b = tx_body.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for j, (hdr, desc) in enumerate(items):
            pj = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            if j > 0: pj.space_before = Pt(8)
            rj1 = pj.add_run()
            rj1.text = f"{hdr}\n"
            rj1.font.name = FONT_NAME; rj1.font.size = Pt(9.5); rj1.font.bold = True; rj1.font.color.rgb = INK_PRIMARY
            rj2 = pj.add_run()
            rj2.text = desc
            rj2.font.name = FONT_NAME; rj2.font.size = Pt(8.8); rj2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Notice the common denominator: Tier 1 winners sell software, simulation, and specialized mobility services—not unconstrained humanoid hardware.")
    set_notes(s, "Tier 1 deep-dive. Detail Waymo's 150k trips, TSMC's inline defect classification, and Applied Intuition's multi-million ARR contracts.")
    return s


def slide_08_tier2_tier3_deepdive():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Tier 2 & Tier 3 Analysis: Bounded Pilots vs. Lab Claims",
               "Evaluating active customer trials and identifying ungrounded marketing claims.")

    # Left: Tier 2 (Active Pilots)
    add_card(s, 0.8, 1.85, 6.4, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, 6.4, 0.025, AMBER)
    add_badge(s, 1.05, 2.05, "TIER 2: PRE-PRODUCTION PILOTS", bg=BORDER_AMBER, fg=AMBER, font_size=8.5, bold=True)

    tx_t2 = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(5.9), Inches(4.0))
    tf_t2 = tx_t2.text_frame
    tf_t2.word_wrap = True
    tf_t2.margin_left = tf_t2.margin_right = tf_t2.margin_top = tf_t2.margin_bottom = 0

    p_t2_h = tf_t2.paragraphs[0]
    r_t2_h = p_t2_h.add_run()
    r_t2_h.text = "Active Enterprise Trials in Bounded Industrial Facilities\n"
    r_t2_h.font.name = FONT_NAME; r_t2_h.font.size = Pt(12); r_t2_h.font.bold = True; r_t2_h.font.color.rgb = INK_PRIMARY

    pilots = [
        ("Figure AI at BMW Spartanburg Plant [Verified]",
         "Piloting Figure 02 humanoid robot for sheet-metal sub-assembly insertion in manufacturing cells. Confirmed in BMW Group Press Release (Aug 2024). Operation remains strictly bounded within staged fixtures with human monitors."),
        ("Apptronik Apollo at Mercedes-Benz [Verified]",
         "Testing Apollo humanoid robots for delivering assembly kits and parts to workers along vehicle assembly lines. Confirmed in Mercedes-Benz Press Release (Mar 2024). Low-speed transport in mapped corridors."),
        ("Agility Robotics Digit at Amazon & GXO Logistics [Reported]",
         "Testing Digit bipedal robots at Amazon's BFI1 fulfillment facility and GXO logistics hubs for empty tote retrieval and replenishment. Constrained paths with bounded payload capacity."),
        ("Boston Dynamics Stretch at DHL Supply Chain [Verified]",
         "Deploying Stretch mobile manipulation arms for unloading floor-loaded shipping containers at DHL distribution facilities. High reliability in box picking but single-task specialized form factor.")
    ]
    for name, desc in pilots:
        p_p = tf_t2.add_paragraph()
        p_p.space_before = Pt(6)
        rp1 = p_p.add_run()
        rp1.text = f"•  {name}: "
        rp1.font.name = FONT_NAME; rp1.font.size = Pt(9.5); rp1.font.bold = True; rp1.font.color.rgb = INK_PRIMARY
        rp2 = p_p.add_run()
        rp2.text = desc
        rp2.font.name = FONT_NAME; rp2.font.size = Pt(8.8); rp2.font.color.rgb = TEXT_LIGHT

    # Right: Tier 3 (Lab Claims)
    add_card(s, 7.53, 1.85, 5.0, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 7.53, 1.85, 5.0, 0.025, RED)
    add_badge(s, 7.78, 2.05, "TIER 3: LAB CLAIMS & HYPE", bg=BORDER_RED, fg=RED, font_size=8.5, bold=True)

    tx_t3 = s.shapes.add_textbox(Inches(7.78), Inches(2.40), Inches(4.5), Inches(4.0))
    tf_t3 = tx_t3.text_frame
    tf_t3.word_wrap = True
    tf_t3.margin_left = tf_t3.margin_right = tf_t3.margin_top = tf_t3.margin_bottom = 0

    p_t3_h = tf_t3.paragraphs[0]
    r_t3_h = p_t3_h.add_run()
    r_t3_h.text = "Unconstrained Claims with Zero Production Scale\n"
    r_t3_h.font.name = FONT_NAME; r_t3_h.font.size = Pt(12); r_t3_h.font.bold = True; r_t3_h.font.color.rgb = INK_PRIMARY

    lab_claims = [
        ("Zero-Shot Precision Assembly (<0.1mm) [Speculative]",
         "Claims of transferring tight-tolerance mechanical assembly (<0.1mm clearance) directly from simulation to real production cells without physical recalibration or fine-tuning. Contact friction breaks sim-to-real transfer."),
        ("Unstructured Multi-Step Domestic Tasks [Reported]",
         "Autonomous laundry folding, table clearing, or cooking without pre-scanned 3D maps or fixed fixtures. Demos consistently mask human teleoperation or curate 1-in-20 successful runs."),
        ("Universal Dexterity Humanoid Workers [Speculative]",
         "Claims that humanoids can replace general factory labor within 24 months. Overlooks the tactile sensing deficit, actuator thermal degradation, and <60s takt time requirements.")
    ]
    for name, desc in lab_claims:
        p_l = tf_t3.add_paragraph()
        p_l.space_before = Pt(8)
        rl1 = p_l.add_run()
        rl1.text = f"⚠  {name}\n"
        rl1.font.name = FONT_NAME; rl1.font.size = Pt(9.5); rl1.font.bold = True; rl1.font.color.rgb = RED
        rl2 = p_l.add_run()
        rl2.text = desc
        rl2.font.name = FONT_NAME; rl2.font.size = Pt(8.8); rl2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Tier 2 pilots validate physical feasibility in bounded cells, but cannot yet meet unconstrained enterprise plant reliability standards.")
    set_notes(s, "Contrast Tier 2 and Tier 3. Emphasize that BMW, Mercedes, and Amazon are conducting bounded trials. Do not confuse a pilot with an enterprise rollout.")
    return s


def slide_09_capital_matrix_p1():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Disclosed Capital Matrix: Foundation Models & Humanoids",
               "Over $2.2B in venture capital has poured into frontier robotics foundation model startups.")

    rounds = [
        ("Wayve", "$1.05B Series C", "May 2024", "SoftBank Group, NVIDIA, Microsoft", "Pilot / Early Production (Driving)", "AV Foundational World Models", GREEN),
        ("Figure AI", "$675M Series B", "Feb 2024", "Microsoft, Parkway, OpenAI Fund, NVIDIA, Jeff Bezos ($2.6B Val)", "Pilot (BMW Spartanburg)", "Figure 02 Humanoid Platform", GREEN),
        ("Physical Intelligence", "$400M Series A", "Nov 2024", "Bezos Expeditions, Thrive Capital, Lux Capital ($2.4B Val)", "Pilot / Research (π0 generalist model)", "π0 Flow Matching VLA", GREEN),
        ("1X Technologies", "$100M Series B", "Jan 2024", "OpenAI, Thrive Capital, EQT Ventures", "Pilot (NEO Bipedal / EVE)", "1X Androids Platform", GREEN)
    ]

    card_w = 11.73
    top_base = 1.85
    row_h = 0.88
    gap = 0.12

    for i, (company, funding, date, investors, maturity, leaders, tag_color) in enumerate(rounds):
        top = top_base + i * (row_h + gap)
        add_card(s, 0.8, top, card_w, row_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)

        tx = s.shapes.add_textbox(Inches(0.95), Inches(top + 0.12), Inches(card_w - 0.3), Inches(row_h - 0.24))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        r_c = p1.add_run()
        r_c.text = company + "  "
        r_c.font.name = FONT_NAME; r_c.font.size = Pt(12); r_c.font.bold = True; r_c.font.color.rgb = INK_PRIMARY
        
        r_f = p1.add_run()
        r_f.text = f"({funding}, {date})  ·  "
        r_f.font.name = FONT_NAME; r_f.font.size = Pt(10); r_f.font.bold = True; r_f.font.color.rgb = BRAND_BLUE
        
        r_tag = p1.add_run()
        r_tag.text = "[Verified]"
        r_tag.font.name = FONT_NAME; r_tag.font.size = Pt(9); r_tag.font.bold = True; r_tag.font.color.rgb = GREEN

        p2 = tf.add_paragraph()
        p2.space_before = Pt(3)
        r_inv = p2.add_run()
        r_inv.text = "Lead Investors: "
        r_inv.font.name = FONT_NAME; r_inv.font.size = Pt(9); r_inv.font.bold = True; r_inv.font.color.rgb = TEXT_MUTED
        r_inv_d = p2.add_run()
        r_inv_d.text = investors + "   |   "
        r_inv_d.font.name = FONT_NAME; r_inv_d.font.size = Pt(9); r_inv_d.font.color.rgb = TEXT_LIGHT

        r_mat = p2.add_run()
        r_mat.text = "Commercial Status: "
        r_mat.font.name = FONT_NAME; r_mat.font.size = Pt(9); r_mat.font.bold = True; r_mat.font.color.rgb = TEXT_MUTED
        r_mat_d = p2.add_run()
        r_mat_d.text = maturity
        r_mat_d.font.name = FONT_NAME; r_mat_d.font.size = Pt(9); r_mat_d.font.color.rgb = TEXT_LIGHT

    # Bottom summary callout
    add_card(s, 0.8, 5.80, 11.73, 0.80, bg=BG_CARD_ALT, border=BORDER_SUBTLE, border_width=0.75)
    tx_sum = s.shapes.add_textbox(Inches(1.05), Inches(5.88), Inches(11.3), Inches(0.65))
    tf_s = tx_sum.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    ps = tf_s.paragraphs[0]
    rs1 = ps.add_run()
    rs1.text = "Strategic Implication: "
    rs1.font.name = FONT_NAME; rs1.font.size = Pt(10); rs1.font.bold = True; rs1.font.color.rgb = BRAND_NAVY
    rs2 = ps.add_run()
    rs2.text = "Capital concentration in foundation models ($2.4B-$2.6B valuations) creates intense commercialization pressure. Frontier AI firms lack manufacturing domain experience and urgently require certified engineering systems integrators like LTTS to deploy into live industrial plants."
    rs2.font.name = FONT_NAME; rs2.font.size = Pt(9.2); rs2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Venture capital is aggressively subsidizing foundation model development. LTTS positions as the indispensable commercial deployment channel.")
    set_notes(s, "Disclosed Capital Matrix (Part 1). Detail Wayve, Figure, PI, and 1X rounds. Highlight how big tech (Microsoft, NVIDIA, SoftBank) is co-investing.")
    return s


def slide_10_capital_matrix_p2():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "Disclosed Capital Matrix: Automation, Simulation & Safety",
               "High-margin software infrastructure and digital twin platforms command enterprise multiples.")

    entries = [
        ("Industrial Automation AI (Fixed & Mobile)", [
            ("Skild AI ($300M Series A, Jul 2024)", "Valued at $1.5B, led by Lightspeed, Coatue, SoftBank, Bezos Expeditions. General-purpose robotics brain [Verified]."),
            ("Covariant (Amazon Transaction, Aug 2024)", "Amazon reverse acqui-hired founders Pieter Abbeel, Peter Chen, Rocky Duan, with non-exclusive model licensing [Verified]."),
            ("Bright Machines ($126M Series C, Jun 2024)", "Software-defined manufacturing assembly cells with micro-factories [Verified].")
        ], CYAN, BORDER_CYAN),

        ("Simulation & Digital Twin Platforms", [
            ("Applied Intuition ($250M Series E, Mar 2024)", "Valued at $6.0B, led by Lux Capital, Elad Gil, Porsche Investments. High ARR across automotive & defense [Verified]."),
            ("Scale AI ($1.0B Series F, May 2024)", "Valued at $13.8B, led by Accel with participation from tech giants. High-throughput data labeling & simulation [Verified]."),
            ("World Labs ($230M Seed/Series A, Sep 2024)", "Led by Founders Fund, NEA. 3D spatial intelligence and physics-based world generation [Verified].")
        ], BRAND_NAVY, BORDER_SUBTLE),

        ("Robotics Safety & Compliance Tooling", [
            ("Credo AI ($25M Series B, Jun 2024)", "Led by Sands Capital. Enterprise AI governance, auditing, and compliance management platforms [Reported]."),
            ("Holistic AI ($20M, 2024)", "Decibel Partners. AI risk audits, safety benchmarks, and automated assurance dossiers [Reported]."),
            ("Accredited Testing Labs (TÜV SÜD, UL Solutions)", "Statutory functional safety auditing, IEC 61508 / ISO 13849 certification, and plant insurance gating [Verified].")
        ], BRAND_BLUE, BORDER_SUBTLE)
    ]

    card_w = 3.68
    gap = 0.34
    for i, (category, items, color, border) in enumerate(entries):
        left = 0.8 + i * (card_w + gap)
        top = 1.85
        card_h = 4.75
        add_card(s, left, top, card_w, card_h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
        # Subtle top accent line
        add_rect(s, left, top, card_w, 0.025, color)

        tx = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.22), Inches(card_w - 0.4), Inches(0.65))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = category
        r.font.name = FONT_NAME; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = INK_PRIMARY

        tx_b = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.95), Inches(card_w - 0.4), Inches(3.6))
        tf_b = tx_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

        for j, (name, desc) in enumerate(items):
            pj = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            if j > 0: pj.space_before = Pt(7)
            rj1 = pj.add_run()
            rj1.text = f"{name}\n"
            rj1.font.name = FONT_NAME; rj1.font.size = Pt(9.5); rj1.font.bold = True; rj1.font.color.rgb = INK_PRIMARY
            rj2 = pj.add_run()
            rj2.text = desc
            rj2.font.name = FONT_NAME; rj2.font.size = Pt(8.5); rj2.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Notice that simulation (Applied Intuition, Scale AI) and testing platforms command $6B-$14B valuations on pure software gross margins.")
    set_notes(s, "Disclosed Capital Matrix (Part 2). Point out Applied Intuition at $6B and Scale AI at $13.8B. Enterprise simulation software scales profitably.")
    return s


def slide_11_capital_asymmetry():
    s = new_slide()
    add_header(s, "Module 1 · Commercial State", "The Capital vs. Maturity Asymmetry: The Hardware Trap",
               "Over $2.2B in humanoid hardware yields <$20M revenue; infrastructure software captures all margin.")

    # Left: The Humanoid Capital Trap
    add_card(s, 0.8, 1.85, 5.7, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 0.8, 1.85, 5.7, 0.025, RED)
    add_badge(s, 1.05, 2.05, "THE HUMANOID CAPITAL TRAP", bg=BORDER_RED, fg=RED, font_size=8.5, bold=True)

    tx_l = s.shapes.add_textbox(Inches(1.05), Inches(2.40), Inches(5.2), Inches(4.0))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p1 = tf_l.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Capital Flooding Ahead of Operational Reliability\n"
    r1.font.name = FONT_NAME; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = INK_PRIMARY

    points_trap = [
        ("The Revenue Disconnect:", "Over $2.2B has flowed into general-purpose humanoid OEMs over the last 18 months [Verified]. However, customer revenue across the entire sub-segment remains under $20M industry-wide [Estimated]."),
        ("Hardware MTBF Bottleneck:", "Humanoid hardware faces severe Mean Time Between Failures (< 50 hours of continuous multi-joint actuation) due to harmonic drive wear and cable fatigue [Estimated]."),
        ("Thermal Derating Constraints:", "Compact high-torque actuators suffer thermal derating under sustained loads, forcing robots to slow down or enter cooling cool-downs during continuous shifts [Estimated]."),
        ("Exorbitant Prototype BOM Costs:", "Current prototype Bill of Materials ranges from $100,000 to $250,000 per unit, preventing positive unit economics at low production volumes [Estimated].")
    ]
    for h, d in points_trap:
        p = tf_l.add_paragraph()
        p.space_before = Pt(6)
        rh = p.add_run()
        rh.text = f"⚠  {h} "
        rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = RED
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    # Right: The Profitable Software Layer & LTTS Implication
    add_card(s, 6.83, 1.85, 5.7, 4.75, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75)
    add_rect(s, 6.83, 1.85, 5.7, 0.025, GREEN)
    add_badge(s, 7.08, 2.05, "THE CASH-FLOW-POSITIVE INFRASTRUCTURE LAYER", bg=BORDER_GREEN, fg=GREEN, font_size=8.5, bold=True)

    tx_r = s.shapes.add_textbox(Inches(7.08), Inches(2.40), Inches(5.2), Inches(4.0))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr1 = tf_r.paragraphs[0]
    rr1 = pr1.add_run()
    rr1.text = "High-Margin Software & Engineering Services\n"
    rr1.font.name = FONT_NAME; rr1.font.size = Pt(12); rr1.font.bold = True; rr1.font.color.rgb = INK_PRIMARY

    points_infra = [
        ("SaaS Gross Margins (70%-80%):", "In contrast to hardware OEMs, virtual simulation, validation tooling, and synthetic data infrastructure companies scale on enterprise SaaS models with 70%-80% gross margins [Verified]."),
        ("Enterprise Proof Points:", "Applied Intuition secured a $6B valuation backed by multi-million-dollar ARR contracts with automotive OEMs and defense primes (Press Release, Mar 2024) [Verified]."),
        ("Strategic Implication for LTTS:", "Venture capital is aggressively subsidizing hardware experimentation. LTTS should position upstream as the neutral integration, verification, and testing partner that captures lucrative service revenue regardless of which hardware vendor wins [Verified].")
    ]
    for h, d in points_infra:
        p = tf_r.add_paragraph()
        p.space_before = Pt(8)
        rh = p.add_run()
        rh.text = f"✔  {h} "
        rh.font.name = FONT_NAME; rh.font.size = Pt(9.5); rh.font.bold = True; rh.font.color.rgb = GREEN
        rd = p.add_run()
        rd.text = d
        rd.font.name = FONT_NAME; rd.font.size = Pt(9); rd.font.color.rgb = TEXT_LIGHT

    add_takeaway(s, "Hardware OEMs burn capital battling MTBF and BOM limits. LTTS sells the essential integration and safety picks and shovels.")
    set_notes(s, "The Capital vs Maturity Asymmetry. This is a foundational insight: let VCs fund hardware risk; LTTS captures high-margin integration revenue.")
    return s
