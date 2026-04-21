"""
The Practice of Physical AI — Executive Human-Centric Design System
Shared across all slide generator modules.

Adheres to top-tier management consulting (McKinsey, BCG) and modern editorial design principles (Stripe, Linear, Apple Keynote).
"""

import io
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_Deck.pptx"
MATH_DIR = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\math_imgs_deck"
os.makedirs(MATH_DIR, exist_ok=True)

# ── Human Executive Color Palette ─────────────────────────────────────────────
# Clean, luminous, professional canvas & card fills
BG_CANVAS      = RGBColor(0xFF, 0xFF, 0xFF)   # Crisp Studio White
BG_CARD        = RGBColor(0xF8, 0xFA, 0xFC)   # Slate 50 tint for soft container
BG_CARD_ALT    = RGBColor(0xF1, 0xF5, 0xF9)   # Slate 100 for nested structures
BG_CARD_ACCENT = RGBColor(0xEE, 0xF2, 0xF6)   # Slate 150

# Core Typographic Inks (high contrast, ultra-readable, human)
INK_PRIMARY    = RGBColor(0x0F, 0x17, 0x2A)   # Slate 900 / Deep Ink
TEXT_DARK      = RGBColor(0x1E, 0x29, 0x3B)   # Slate 800
TEXT_LIGHT     = RGBColor(0x33, 0x41, 0x55)   # Slate 700 (maps to readable dark slate)
TEXT_MUTED     = RGBColor(0x64, 0x74, 0x8B)   # Slate 500
TEXT_FAINT     = RGBColor(0x94, 0xA3, 0xB8)   # Slate 400

# Preserving variable name 'WHITE' for existing slide scripts:
# In light mode, all titles and headings mapped to WHITE now become INK_PRIMARY!
WHITE          = RGBColor(0x0F, 0x17, 0x2A)   # Deep Slate Ink for titles
COLOR_WHITE    = RGBColor(0xFF, 0xFF, 0xFF)   # Pure white for dark banners/badges

# L&T Corporate Brand Identity & Strategic Accents (deep, sophisticated, WCAG AAA)
BRAND_NAVY     = RGBColor(0x00, 0x2B, 0x49)   # L&T Corporate Deep Navy
BRAND_BLUE     = RGBColor(0x0A, 0x58, 0xCA)   # Executive Royal Blue
GOLD           = RGBColor(0xB4, 0x53, 0x09)   # Warm Amber / Ochre
CYAN           = RGBColor(0x02, 0x84, 0xC7)   # Deep Cerulean / Sky
GREEN          = RGBColor(0x04, 0x78, 0x57)   # Forest Emerald (Verified)
AMBER          = RGBColor(0xC2, 0x41, 0x0C)   # Terracotta (Estimated)
RED            = RGBColor(0xB9, 0x1C, 0x1C)   # Deep Crimson (Critique / Hazard)
PURPLE         = RGBColor(0x6D, 0x28, 0xD9)   # Royal Indigo (Theory / CoE)

# Hairlines & Borders (Fine 0.5pt-0.75pt, no neon outlines!)
BORDER_SUBTLE  = RGBColor(0xE2, 0xE8, 0xF0)   # Slate 200 hairline
BORDER_LINE    = RGBColor(0xCB, 0xD5, 0xE1)   # Slate 300 divider
BORDER_GOLD    = RGBColor(0xFE, 0xF3, 0xC7)   # Soft amber tint
BORDER_CYAN    = RGBColor(0xE0, 0xF2, 0xFE)   # Soft cyan tint
BORDER_GREEN   = RGBColor(0xD1, 0xFA, 0xE5)   # Soft emerald tint
BORDER_RED     = RGBColor(0xFE, 0xE2, 0xE2)   # Soft red tint
BORDER_AMBER   = RGBColor(0xFF, 0xED, 0xD5)   # Soft amber tint
BORDER_PURPLE  = RGBColor(0xF3, 0xE8, 0xFF)   # Soft purple tint

FONT_NAME      = "Segoe UI"
FONT_SERIF     = "Georgia"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.500)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
blank_layout = prs.slide_layouts[6]

def new_slide(bg_color=BG_CANVAS):
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = bg_color
    return slide

def render_math(latex_str, fontsize=18, color='#0F172A', dpi=300):
    # Enforce high-contrast dark ink for crisp executive readability
    if color in ['#DFB756', '#38BDF8', '#34D399', '#FB923C', '#F87171', '#C084FC', '#FFFFFF', 'white', 'cyan', 'gold']:
        color = '#0F172A'
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    text = fig.text(0, 0, f'${latex_str}$', fontsize=fontsize, color=color, math_fontfamily='cm')
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)
    pad = 8
    w_in = (bbox.width + pad * 2) / dpi
    h_in = (bbox.height + pad * 2) / dpi
    fig.set_size_inches(max(w_in, 0.4), max(h_in, 0.25))
    text.set_position((pad / fig.get_window_extent().width, pad / fig.get_window_extent().height))
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=pad/dpi)
    plt.close(fig)
    buf.seek(0)
    return buf.read()

def add_math_image(slide, latex_str, l, t, fontsize=18, color='#0F172A', max_h=0.8):
    img_bytes = render_math(latex_str, fontsize=fontsize, color=color)
    img_stream = io.BytesIO(img_bytes)
    pic = slide.shapes.add_picture(img_stream, Inches(l), Inches(t))
    if pic.height > Inches(max_h):
        aspect = pic.width / pic.height
        pic.height = Inches(max_h)
        pic.width = int(Inches(max_h) * aspect)
    return pic

def add_rect(slide, l, t, w, h, fill_color, border_color=None, border_width=1, shape_type=MSO_SHAPE.RECTANGLE):
    shape = slide.shapes.add_shape(shape_type, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape

def add_card(slide, l, t, w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=0.75, shape_type=MSO_SHAPE.RECTANGLE):
    return add_rect(slide, l, t, w, h, bg, border, border_width, shape_type=shape_type)

def add_header(slide, module_tag, title, subtitle=None):
    # Top Category Tracker
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.36), Inches(10.0), Inches(0.24))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = False
    tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    r_tag = p_tag.add_run()
    r_tag.text = module_tag.upper()
    r_tag.font.name = FONT_NAME
    r_tag.font.size = Pt(8.5)
    r_tag.font.bold = True
    r_tag.font.color.rgb = BRAND_NAVY

    # Action Title (Insight-Driven, Bold Slate)
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.58), Inches(11.73), Inches(0.54))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title
    r_t.font.name = FONT_NAME
    r_t.font.size = Pt(22)
    r_t.font.bold = True
    r_t.font.color.rgb = INK_PRIMARY

    # Subtitle
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.14), Inches(11.73), Inches(0.32))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        r_sub = p_sub.add_run()
        r_sub.text = subtitle
        r_sub.font.name = FONT_NAME
        r_sub.font.size = Pt(11)
        r_sub.font.color.rgb = TEXT_MUTED

    # Refined Hairline Divider with Navy Anchor
    div_full = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.52), Inches(11.73), Inches(0.01))
    div_full.fill.solid()
    div_full.fill.fore_color.rgb = BORDER_SUBTLE
    div_full.line.fill.background()

    anchor = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.52), Inches(1.2), Inches(0.02))
    anchor.fill.solid()
    anchor.fill.fore_color.rgb = BRAND_NAVY
    anchor.line.fill.background()

def add_takeaway(slide, text, l=0.8, t=6.85, w=11.73, h=0.35, is_dark=False):
    # Clean, quiet, editorial bottom rule
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(0.01))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(0x1E, 0x3A, 0x5F) if is_dark else BORDER_SUBTLE
    div.line.fill.background()

    tx = slide.shapes.add_textbox(Inches(l), Inches(t + 0.05), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    
    r1 = p.add_run()
    r1.text = "STRATEGIC TAKEAWAY  —  "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = GOLD if is_dark else BRAND_NAVY
    
    r2 = p.add_run()
    r2.text = text
    r2.font.name = FONT_NAME
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0xBA, 0xE6, 0xFD) if is_dark else TEXT_LIGHT

def set_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text

def add_badge(slide, l, t, text, bg=None, fg=BRAND_NAVY, font_size=8.5, bold=True):
    w = max(0.85, len(text) * 0.075 + 0.3)
    card_bg = bg if bg else BG_CARD_ALT
    rect = add_rect(slide, l, t, w, 0.24, card_bg, border_color=BORDER_SUBTLE, border_width=0.5, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = rect.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_NAME
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.color.rgb = fg
    return w

def add_stat_box(slide, l, t, w, h, number, label, sublabel=None, num_color=BRAND_NAVY):
    add_card(slide, l, t, w, h, bg=BG_CARD, border=BORDER_SUBTLE)
    tx = slide.shapes.add_textbox(Inches(l + 0.18), Inches(t + 0.12), Inches(w - 0.36), Inches(h - 0.24))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = number
    r1.font.name = FONT_NAME
    r1.font.size = Pt(26)
    r1.font.bold = True
    r1.font.color.rgb = num_color
    
    p2 = tf.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = label
    r2.font.name = FONT_NAME
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.color.rgb = INK_PRIMARY
    
    if sublabel:
        p3 = tf.add_paragraph()
        p3.space_before = Pt(2)
        r3 = p3.add_run()
        r3.text = sublabel
        r3.font.name = FONT_NAME
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = TEXT_MUTED

def section_divider_slide(module_num, title, subtitle, bullets):
    # Dramatic, authoritative L&T Deep Corporate Navy chapter break
    s = new_slide(bg_color=BRAND_NAVY)
    
    # Gold top accent line
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.15), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()

    # Module tracker
    tx_mod = s.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(8.0), Inches(0.3))
    tf_m = tx_mod.text_frame
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
    pm = tf_m.paragraphs[0]
    rm = pm.add_run()
    rm.text = f"MODULE {module_num:02d} · STRATEGIC FOCUS"
    rm.font.name = FONT_NAME; rm.font.size = Pt(9); rm.font.bold = True; rm.font.color.rgb = GOLD
    
    # Big Title
    tx = s.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.0), Inches(1.5))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    r.font.name = FONT_NAME
    r.font.size = Pt(36)
    r.font.bold = True
    r.font.color.rgb = COLOR_WHITE
    
    p_sub = tf.add_paragraph()
    p_sub.space_before = Pt(6)
    r_sub = p_sub.add_run()
    r_sub.text = subtitle
    r_sub.font.name = FONT_NAME
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    div = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.4), Inches(8.0), Inches(0.015))
    div.fill.solid(); div.fill.fore_color.rgb = GOLD; div.line.fill.background()
    
    tx_b = s.shapes.add_textbox(Inches(1.0), Inches(3.7), Inches(10.0), Inches(3.0))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    for i, b in enumerate(bullets):
        p_item = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        if i > 0: p_item.space_before = Pt(8)
        r_num = p_item.add_run()
        r_num.text = "—   "
        r_num.font.name = FONT_NAME
        r_num.font.size = Pt(12)
        r_num.font.bold = True
        r_num.font.color.rgb = GOLD
        r_txt = p_item.add_run()
        r_txt.text = b
        r_txt.font.name = FONT_NAME
        r_txt.font.size = Pt(12)
        r_txt.font.color.rgb = RGBColor(0xF1, 0xF5, 0xF9)

    set_notes(s, f"Module {module_num}: {title}. Executive briefing transition setting strategic context.")
    return s
