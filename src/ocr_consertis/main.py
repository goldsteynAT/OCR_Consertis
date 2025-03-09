import os
from pdf_processing import batch_convert_pdfs

if __name__ == "__main__":
    # Example usage:
    input_path = r"C:\Users\danie\Desktop\neuocr\Test_ohne_OCR"   # Replace this path accordingly
    output_dir = r"C:\Users\danie\Desktop\neuocr\Test_mit_OCR"  # Replace this path accordingly

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    batch_convert_pdfs(input_path, output_dir)