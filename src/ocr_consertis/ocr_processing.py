import os
import ocrmypdf

def apply_ocr_to_pdf(input_pdf: str, output_pdf: str, use_gpu: bool = False, language: str = "deu+eng", deskew: bool = True, jobs: int = 1) -> None:
    """
    Applies OCR to a PDF file using ocrmypdf and generates a searchable PDF.
    
    Args:
        input_pdf (str): Normalized path to the input PDF file.
        output_pdf (str): Path where the OCR-processed PDF should be saved.
        use_gpu (bool): Whether to use GPU acceleration if available.
        language (str): OCR languages (e.g., "deu+eng").
        deskew (bool): Whether to apply deskewing.
        jobs (int): Number of parallel jobs to use internally in ocrmypdf.
    """
    try:
        if use_gpu:
            ocrmypdf.ocr(
                input_pdf,
                output_pdf,
                language=language,
                force_ocr=True,
                deskew=deskew,
                jobs=jobs
            )
        else:
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

def batch_ocr_pdfs(input_dir: str, output_dir: str, use_gpu: bool = False, language: str = "deu+eng", deskew: bool = True, jobs: int = 1, status_file: str = None) -> None:
    """
    Processes all PDFs in the input_dir, applies OCR, and saves them in the output_dir.
    The directory structure is preserved. Supports pause/resume functionality by saving the processing
    status to a JSON file.
    
    Args:
        input_dir (str): Directory containing PDFs to process.
        output_dir (str): Directory to save OCR-processed PDFs.
        use_gpu (bool): Whether to use GPU acceleration if available.
        language (str): OCR languages (e.g., "deu+eng").
        deskew (bool): Whether to apply deskewing.
        jobs (int): Number of parallel jobs to use internally in ocrmypdf.
        status_file (str): Path to the status file (if None, defaults to 'ocr_status.json' in output_dir).
    """
    from status_manager import load_status, save_status
    from progress_display import display_progress

    if status_file is None:
        status_file = os.path.join(output_dir, "ocr_status.json")
    
    # Load previously processed PDFs (normalize paths)
    processed = load_status(status_file)
    
    # Gather all PDF files from input_dir and normalize them
    pdf_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.normpath(os.path.abspath(os.path.join(root, file)))
                pdf_files.append(path)
    total = len(pdf_files)
    
    try:
        for idx, input_pdf in enumerate(pdf_files, start=1):
            # Skip if already processed
            if input_pdf in processed:
                continue
            
            # Determine output file path preserving directory structure
            relative_dir = os.path.relpath(os.path.dirname(input_pdf), os.path.abspath(input_dir))
            target_dir = os.path.join(output_dir, relative_dir)
            os.makedirs(target_dir, exist_ok=True)
            output_pdf = os.path.join(target_dir, os.path.basename(input_pdf))
            
            # Update progress display
            in_progress = input_pdf
            next_items = [pdf for pdf in pdf_files if pdf not in processed and pdf != input_pdf]
            display_progress(processed, in_progress, next_items, len(processed), total)
            
            # Process current PDF
            apply_ocr_to_pdf(input_pdf, output_pdf, use_gpu=use_gpu, language=language, deskew=deskew, jobs=jobs)
            
            # Mark as completed and save status
            processed.append(input_pdf)
            save_status(status_file, processed)
    except KeyboardInterrupt:
        print("\n⏸ Process interrupted. Saving current status...")
        save_status(status_file, processed)
        print("Status saved. You can resume processing later.")
