import os
from pdf_processing import batch_convert_pdfs
from ocr_processing import batch_process_ocr  # OCR-Funktion importieren

if __name__ == "__main__":
    # Beispielpfade
    input_path = r"C:\Users\danie\Desktop\neuocr\Test_ohne_OCR"   # Ordner mit PDFs
    output_dir = r"C:\Users\danie\Desktop\neuocr\Test_mit_OCR"    # Ordner für PNGs & OCR-Texte

    # Sicherstellen, dass das Ausgabe-Verzeichnis existiert
    os.makedirs(output_dir, exist_ok=True)
    
    # 1️⃣ PDF in PNG konvertieren
    batch_convert_pdfs(input_path, output_dir)

    # 2️⃣ OCR auf die generierten PNGs anwenden
    batch_process_ocr(output_dir, output_dir)

    print("✅ Verarbeitung abgeschlossen! PNGs & OCR-Textdateien gespeichert.")
