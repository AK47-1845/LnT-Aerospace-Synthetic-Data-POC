"""
Executive Editorial Design System V2
Pure Studio White Backgrounds, Georgia + Calibri Typographic Pairing,
Continuous McKinsey Tabular Exhibits, High-Contrast LaTeX Math.
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

OUTPUT_PPTX = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\The_Practice_of_Physical_AI_Executive_Master_23.pptx"
MATH_DIR = r"c:\Users\k18ka\Downloads\Genuity IO all documents\LTTS\math_imgs_deck"
os.makedirs(MATH_DIR, exist_ok=True)

# ── 100% Pure Studio White Canvas System ───────────────────────────────────────
BG_CANVAS      = RGBColor(0xFF, 0xFF, 0xFF)   # Pure Studio White (100% of slides)
BG_CARD        = RGBColor(0xF8, 0xFA, 0xFC)   # Slate 50 tint for soft container
BG_CARD_ALT    = RGBColor(0xF1, 0xF5, 0xF9)   # Slate 100 for nested structures
BG_CARD_ACCENT = RGBColor(0xEE, 0xF2, 0xF6)   # Slate 150
BG_CARD_BLUE   = RGBColor(0xF0, 0xF7, 0xFF)   # Very soft blue highlight

# ── Core Executive Inks (High Contrast & Legibility) ──────────────────────────
INK_PRIMARY    = RGBColor(0x0F, 0x17, 0x2A)   # Slate 900 / Deep Ink
TEXT_DARK      = RGBColor(0x1E, 0x29, 0x3B)   # Slate 800
TEXT_LIGHT     = RGBColor(0x33, 0x41, 0x55)   # Slate 700
TEXT_MUTED     = RGBColor(0x64, 0x74, 0x8B)   # Slate 500
TEXT_FAINT     = RGBColor(0x94, 0xA3, 0xB8)   # Slate 400
WHITE          = RGBColor(0x0F, 0x17, 0x2A)   # For legacy compatibility in light mode
COLOR_WHITE    = RGBColor(0xFF, 0xFF, 0xFF)   # Pure white for navy headers/callouts

# ── Corporate Brand Identity & Strategic Accents ──────────────────────────────
BRAND_NAVY     = RGBColor(0x00, 0x2B, 0x49)   # L&T Corporate Deep Navy
BRAND_BLUE     = RGBColor(0x0A, 0x58, 0xCA)   # Executive Royal Blue
GOLD           = RGBColor(0xB4, 0x53, 0x09)   # Warm Ochre / Amber
CYAN           = RGBColor(0x02, 0x84, 0xC7)   # Cerulean / Sky
GREEN          = RGBColor(0x04, 0x78, 0x57)   # Forest Emerald (Verified)
AMBER          = RGBColor(0xC2, 0x41, 0x0C)   # Terracotta (Estimated)
RED            = RGBColor(0xB9, 0x1C, 0x1C)   # Crimson (Critique / Hazard)
PURPLE         = RGBColor(0x6D, 0x28, 0xD9)   # Royal Indigo (Theory / CoE)

# ── Hairlines & Borders ────────────────────────────────────────────────────────
BORDER_SUBTLE  = RGBColor(0xE2, 0xE8, 0xF0)   # Slate 200 hairline
BORDER_LINE    = RGBColor(0xCB, 0xD5, 0xE1)   # Slate 300 divider
BORDER_BLUE    = RGBColor(0xBF, 0xDB, 0xFE)   # Soft blue border
BORDER_GOLD    = RGBColor(0xFE, 0xF3, 0xC7)
BORDER_GREEN   = RGBColor(0xD1, 0xFA, 0xE5)
BORDER_RED     = RGBColor(0xFE, 0xE2, 0xE2)
BORDER_AMBER   = RGBColor(0xFF, 0xED, 0xD5)
BORDER_PURPLE  = RGBColor(0xF3, 0xE8, 0xFF)

# ── Refined Modern Typography Hierarchy ──────────────────────────────────────
# Segoe UI: Friendly, modern, human, crystal clear, non-sterile
FONT_TITLE     = "Segoe UI"
FONT_BODY      = "Segoe UI"
FONT_MONO      = "Consolas"

# Aliases for backward compatibility
FONT_NAME      = FONT_BODY
FONT_SERIF     = FONT_TITLE

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
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    text = fig.text(0, 0, f'${latex_str}$', fontsize=fontsize, color='#0F172A', math_fontfamily='cm')
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

def add_card(slide, l, t, w, h, bg=BG_CARD, border=BORDER_SUBTLE, border_width=1.0, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, corner_radius=0.035):
    shape = slide.shapes.add_shape(shape_type, Inches(l), Inches(t), Inches(w), Inches(h))
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE and corner_radius is not None:
        shape.adjustments[0] = corner_radius
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    if border:
        shape.line.color.rgb = border
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape

def add_pill_badge(slide, l, t, text, bg=None, fg=BRAND_BLUE, font_size=10, bold=True, pad_w=0.45):
    w = max(1.2, len(text) * 0.085 + pad_w)
    pill_bg = bg if bg else RGBColor(0xEE, 0xF2, 0xFF)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(0.32))
    shape.adjustments[0] = 0.5
    shape.fill.solid()
    shape.fill.fore_color.rgb = pill_bg
    shape.line.color.rgb = RGBColor(0xC7, 0xD2, 0xFE)
    shape.line.width = Pt(0.75)
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_TITLE
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.color.rgb = fg
    return shape

def add_header(slide, module_tag, title, subtitle=None):
    # Top Category Pill Tracker
    add_pill_badge(slide, 0.8, 0.38, module_tag.upper(), bg=RGBColor(0xEE, 0xF2, 0xFF), fg=BRAND_BLUE, font_size=9.5, bold=True)

    # Action Title (Enlarged to 28pt bold Segoe UI)
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.73), Inches(0.65))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title
    r_t.font.name = FONT_TITLE
    r_t.font.size = Pt(28)
    r_t.font.bold = True
    r_t.font.color.rgb = INK_PRIMARY

    # Subtitle / Strategic Context
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.48), Inches(11.73), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        r_sub = p_sub.add_run()
        r_sub.text = subtitle
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(12.5)
        r_sub.font.color.rgb = TEXT_MUTED

    # Minimalist hairline rule across slide
    div_full = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.88), Inches(11.73), Inches(0.015))
    div_full.fill.solid()
    div_full.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4)
    div_full.line.fill.background()

    # Small navy accent anchor
    anchor = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.88), Inches(1.2), Inches(0.025))
    anchor.fill.solid()
    anchor.fill.fore_color.rgb = BRAND_NAVY
    anchor.line.fill.background()

def add_takeaway(slide, text, l=0.8, t=6.85, w=11.73, h=0.35):
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4)
    div.line.fill.background()

    tx = slide.shapes.add_textbox(Inches(l), Inches(t + 0.05), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    
    r1 = p.add_run()
    r1.text = "STRATEGIC TAKEAWAY  —  "
    r1.font.name = FONT_TITLE
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = BRAND_BLUE
    
    r2 = p.add_run()
    r2.text = text
    r2.font.name = FONT_BODY
    r2.font.size = Pt(11)
    r2.font.color.rgb = TEXT_DARK

def set_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text

def add_badge(slide, l, t, text, bg=None, fg=BRAND_NAVY, font_size=9.5, bold=True):
    return add_pill_badge(slide, l, t, text, bg=bg, fg=fg, font_size=font_size, bold=bold)

