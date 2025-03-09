import os
import pathlib
import fitz  # PyMuPDF
from typing import Iterator, List

def convert_pdf_to_images(pdf_path: str, output_dir: str) -> List[str]:
    """
    Opens a PDF using PyMuPDF and saves each page as a PNG image in the output_dir.
    Returns a list of the generated image file paths.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Error opening the PDF file {pdf_path}: {e}")

    output_files = []
    base_name = pathlib.Path(pdf_path).stem
    for page_number in range(doc.page_count):
        page = doc[page_number]
        # Set higher DPI for better image quality
        zoom_x = 2.5  # Adjust scaling factor for horizontal resolution
        zoom_y = 2.5  # Adjust scaling factor for vertical resolution
        matrix = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=matrix)

        output_file = os.path.join(output_dir, f"{base_name}_page_{page_number + 1}.png")
        try:
            pix.save(output_file)
            output_files.append(output_file)
        except Exception as e:
            print(f"Error saving page {page_number + 1} from {pdf_path}: {e}")
    doc.close()
    return output_files

def process_pdf_files(input_path: str) -> Iterator[str]:
    """
    Identifies all PDF files from the given input_path.
    If input_path is a directory, it returns all PDFs (including in subdirectories).
    If input_path is a single PDF file, it returns that file.
    """
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    yield os.path.join(root, file)
    elif os.path.isfile(input_path) and input_path.lower().endswith(".pdf"):
        yield input_path
    else:
        raise ValueError("The provided path must be either a PDF file or a directory containing PDFs.")

def batch_convert_pdfs(input_path: str, output_dir: str) -> None:
    """
    Batch conversion: Iterates through all PDF files in input_path and converts them to images.
    Displays progress in the terminal.
    """
    pdf_files = list(process_pdf_files(input_path))
    total = len(pdf_files)
    if total == 0:
        print("No PDF files found.")
        return

    print(f"Starting conversion of {total} PDF(s)...")
    for idx, pdf_file in enumerate(pdf_files, start=1):
        print(f"[{idx}/{total}] Processing: {pdf_file}")
        try:
            images = convert_pdf_to_images(pdf_file, output_dir)
            print(f"  -> {len(images)} page(s) converted to PNG.")
        except Exception as e:
            print(f"  -> Error processing {pdf_file}: {e}")


