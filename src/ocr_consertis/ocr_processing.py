import os
import pytesseract
from PIL import Image

def perform_ocr_on_image(image_path: str) -> dict:
    """
    Performs OCR on a single image using pytesseract.
    
    Returns:
        A dictionary containing the extracted text and OCR metadata.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        raise RuntimeError(f"Error opening image {image_path}: {e}")
    
    text = pytesseract.image_to_string(image)
    # Optionally, get detailed OCR data
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    return {"text": text, "data": ocr_data}

def batch_process_ocr(input_dir: str, output_dir: str) -> None:
    """
    Recursively processes all PNG images in the input_dir, performs OCR on each image,
    and saves the extracted text as a .txt file in the corresponding output directory.
    The directory structure is preserved.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".png"):
                image_path = os.path.join(root, file)
                ocr_result = perform_ocr_on_image(image_path)
                
                # Preserve directory structure for output
                relative_path = os.path.relpath(root, input_dir)
                target_dir = os.path.join(output_dir, relative_path)
                os.makedirs(target_dir, exist_ok=True)
                
                output_file = os.path.join(target_dir, f"{os.path.splitext(file)[0]}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(ocr_result["text"])
                print(f"OCR processed: {image_path} -> {output_file}")
