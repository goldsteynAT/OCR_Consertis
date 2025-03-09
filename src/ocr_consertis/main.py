import os
from ocr_processing import batch_ocr_pdfs

if __name__ == "__main__":
    input_path = r"C:\Users\danie\Desktop\neuocr\Test_ohne_OCR"   # Directory containing original PDFs
    output_dir = r"C:\Users\danie\Desktop\neuocr\Test_mit_OCR"       # Directory for OCR-processed (searchable) PDFs

    os.makedirs(output_dir, exist_ok=True)
    
    # Apply OCR directly on PDFs using ocrmypdf with progress display
    batch_ocr_pdfs(input_path, output_dir, use_gpu=False)

    print("✅ OCR-Processing completed! Searchable PDFs saved.")
