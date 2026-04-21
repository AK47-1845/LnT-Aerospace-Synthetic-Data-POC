import os
import sys
import comtypes.client

def export_deck():
    ppt_path = os.path.abspath("The_Practice_of_Physical_AI_Executive_Master_23.pptx")
    pdf_path = os.path.abspath("The_Practice_of_Physical_AI_Executive_Master_23.pdf")
    pdf_alt = os.path.abspath("The_Practice_of_Physical_AI_Executive_Deck_Final.pdf")
    out_dir = os.path.abspath("deck_preview_23")
    os.makedirs(out_dir, exist_ok=True)

    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    deck = powerpoint.Presentations.Open(ppt_path)

    print(f"Exporting PDF to: {pdf_path}")
    deck.SaveAs(pdf_path, 32)
    try:
        deck.SaveAs(pdf_alt, 32)
        print(f"Also exported PDF to: {pdf_alt}")
    except Exception:
        pass

    total_slides = deck.Slides.Count
    print(f"Exporting all {total_slides} slides to PNG in: {out_dir}")
    for slide_idx in range(1, total_slides + 1):
        slide = deck.Slides[slide_idx]
        out_png = os.path.join(out_dir, f"slide_{slide_idx:02d}.png")
        slide.Export(out_png, "PNG", 1920, 1080)
        print(f"  Exported slide {slide_idx:02d}/{total_slides:02d} -> {os.path.basename(out_png)}")

    deck.Close()
    powerpoint.Quit()
    print("Export complete!")

if __name__ == "__main__":
    export_deck()
