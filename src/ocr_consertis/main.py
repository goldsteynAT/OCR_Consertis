import os
import time
from ocr_processing import batch_ocr_pdfs

if __name__ == "__main__":
    input_path = r"C:\Users\danie\Desktop\neuocr\Test_ohne_OCR"   # Directory containing original PDFs
    output_dir = r"C:\Users\danie\Desktop\neuocr\Test_mit_OCR"       # Directory for OCR-processed (searchable) PDFs

    os.makedirs(output_dir, exist_ok=True)

    # OCR parameter options for testing and performance tuning
    use_gpu = False          # Set True to enable GPU acceleration (if available)
    language = "deu+eng"     # OCR languages (adjust as needed)
    deskew = False            # Enable or disable deskewing
    jobs = 4                 # Number of parallel jobs used by ocrmypdf internally

    print("🚀 Starting OCR processing...\n")
    start_time = time.time()

    # Apply OCR directly on PDFs using ocrmypdf with adjustable parameters
    batch_ocr_pdfs(input_path, output_dir, use_gpu=use_gpu, language=language, deskew=deskew, jobs=jobs)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n✅ OCR-Processing completed in {elapsed_time:.2f} seconds! Searchable PDFs saved.")
