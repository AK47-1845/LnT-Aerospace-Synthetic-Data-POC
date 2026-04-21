import os
import sys
import comtypes.client

def export_deck():
    ppt_path = os.path.abspath("The_Practice_of_Physical_AI_Executive_Deck.pptx")
    pdf_path = os.path.abspath("The_Practice_of_Physical_AI_Executive_Deck.pdf")
    out_dir = os.path.abspath("deck_preview_master")
    os.makedirs(out_dir, exist_ok=True)

    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    
    deck = powerpoint.Presentations.Open(ppt_path)
    
    # Save as PDF (format 32 = ppSaveAsPDF)
    print(f"Exporting PDF to: {pdf_path}")
    deck.SaveAs(pdf_path, 32)
    
    # Export key slides to PNG
    slides_to_export = [1, 2, 3, 6, 9, 17, 19, 28, 32, 40, 44, 45, 49, 50, 51]
    
    for slide_num in slides_to_export:
        slide = deck.Slides[slide_num]
        out_png = os.path.join(out_dir, f"slide_{slide_num:02d}.png")
        print(f"Exporting slide {slide_num} to: {out_png}")
        slide.Export(out_png, "PNG", 1920, 1080)
        
    deck.Close()
    powerpoint.Quit()
    print("Export complete!")

if __name__ == "__main__":
    export_deck()
