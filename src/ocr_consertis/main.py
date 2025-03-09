import os
import time  # Import für Zeitmessung
from ocr_processing import batch_ocr_pdfs

if __name__ == "__main__":
    input_path = r"C:\Users\danie\Desktop\neuocr\Test_ohne_OCR"   # Directory containing original PDFs
    output_dir = r"C:\Users\danie\Desktop\neuocr\Test_mit_OCR"    # Directory for OCR-processed (searchable) PDFs

    os.makedirs(output_dir, exist_ok=True)

    print("🚀 Starting OCR processing...\n")

    # ⏱ Startzeit erfassen
    start_time = time.time()

    # Apply OCR directly on PDFs using ocrmypdf with progress display and parallel processing
    batch_ocr_pdfs(input_path, output_dir, use_gpu=False)

    # ⏱ Endzeit erfassen
    end_time = time.time()
    
    # ⏳ Verarbeitungszeit berechnen
    elapsed_time = end_time - start_time
    print(f"\n✅ OCR-Processing completed in {elapsed_time:.2f} seconds! Searchable PDFs saved.")
