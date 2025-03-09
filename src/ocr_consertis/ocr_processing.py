import os
import ocrmypdf

def apply_ocr_to_pdf(input_pdf: str, output_pdf: str, use_gpu: bool = False, language: str = "deu+eng", deskew: bool = True, jobs: int = 1) -> None:
    """
    Applies OCR to a PDF file using ocrmypdf and generates a searchable PDF.
    
    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path where the OCR-processed PDF should be saved.
        use_gpu (bool): Whether to use GPU acceleration if available.
        language (str): OCR languages (e.g., "deu+eng").
        deskew (bool): Whether to apply deskewing.
        jobs (int): Number of parallel jobs to use internally in ocrmypdf.
    """
    try:
        if use_gpu:
            # When using GPU, force OCR on all pages
            ocrmypdf.ocr(
                input_pdf,
                output_pdf,
                language=language,
                force_ocr=True,
                deskew=deskew,
                jobs=jobs
            )
        else:
            # When not using GPU, skip OCR if a text layer already exists
            ocrmypdf.ocr(
                input_pdf,
                output_pdf,
                language=language,
                skip_text=True,
                deskew=deskew,
                jobs=jobs
            )
        print(f"✅ OCR applied: {input_pdf} -> {output_pdf}")
    except Exception as e:
        print(f"❌ Error processing {input_pdf}: {e}")

def batch_ocr_pdfs(input_dir: str, output_dir: str, use_gpu: bool = False, language: str = "deu+eng", deskew: bool = True, jobs: int = 1) -> None:
    """
    Processes all PDFs in the input_dir, applies OCR, and saves them in the output_dir.
    The directory structure is preserved.
    Displays progress with an overall progress bar and a status table.
    
    Args:
        input_dir (str): Directory containing PDFs to process.
        output_dir (str): Directory to save OCR-processed PDFs.
        use_gpu (bool): Whether to use GPU acceleration if available.
        language (str): OCR languages (e.g., "deu+eng").
        deskew (bool): Whether to apply deskewing.
        jobs (int): Number of parallel jobs to use internally in ocrmypdf.
    """
    # Gather all PDF files from input_dir
    pdf_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    total = len(pdf_files)
    completed = []
    
    # Import the progress display function
    from progress_display import display_progress

    for idx, input_pdf in enumerate(pdf_files, start=1):
        # Determine output file path preserving directory structure
        relative_dir = os.path.relpath(os.path.dirname(input_pdf), input_dir)
        target_dir = os.path.join(output_dir, relative_dir)
        os.makedirs(target_dir, exist_ok=True)
        output_pdf = os.path.join(target_dir, os.path.basename(input_pdf))
        
        # Determine progress state
        in_progress = input_pdf
        next_items = pdf_files[idx:]  # Remaining files
        display_progress(completed, in_progress, next_items, idx - 1, total)
        
        # Process current PDF with the provided OCR parameters
        apply_ocr_to_pdf(input_pdf, output_pdf, use_gpu=use_gpu, language=language, deskew=deskew, jobs=jobs)
        completed.append(input_pdf)
