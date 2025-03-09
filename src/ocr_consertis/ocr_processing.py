import os
import ocrmypdf

def apply_ocr_to_pdf(input_pdf: str, output_pdf: str, use_gpu: bool = False) -> None:
    """
    Applies OCR to a PDF file using ocrmypdf and generates a searchable PDF.
    
    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path where the OCR-processed PDF should be saved.
        use_gpu (bool): Whether to use GPU acceleration if available.
    """
    try:
        if use_gpu:
            # When using GPU, force OCR on all pages
            ocrmypdf.ocr(
                input_pdf,
                output_pdf,
                language="deu+eng",
                force_ocr=True,
                deskew=True
            )
        else:
            # When not using GPU, skip OCR if a text layer already exists
            ocrmypdf.ocr(
                input_pdf,
                output_pdf,
                language="deu+eng",
                skip_text=True,
                deskew=True
            )
        print(f"✅ OCR applied: {input_pdf} -> {output_pdf}")
    except Exception as e:
        print(f"❌ Error processing {input_pdf}: {e}")

def batch_ocr_pdfs(input_dir: str, output_dir: str, use_gpu: bool = False) -> None:
    """
    Processes all PDFs in the input_dir in parallel, applies OCR, and saves them in the output_dir.
    The directory structure is preserved.
    Displays progress with an overall progress bar and a status table.
    
    Args:
        input_dir (str): Directory containing PDFs to process.
        output_dir (str): Directory to save OCR-processed PDFs.
        use_gpu (bool): Whether to use GPU acceleration if available.
    """
    import concurrent.futures
    from progress_display import display_progress

    # Gather all PDF files from input_dir and prepare tasks
    tasks = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                input_pdf = os.path.join(root, file)
                relative_dir = os.path.relpath(os.path.dirname(input_pdf), input_dir)
                target_dir = os.path.join(output_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)
                output_pdf = os.path.join(target_dir, file)
                tasks.append((input_pdf, output_pdf))
    total = len(tasks)
    completed = []
    
    # Process tasks in parallel using ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_task = {
            executor.submit(apply_ocr_to_pdf, input_pdf, output_pdf, use_gpu): (input_pdf, output_pdf)
            for input_pdf, output_pdf in tasks
        }
        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            try:
                future.result()
            except Exception as exc:
                print(f"❌ Error processing {task[0]}: {exc}")
            completed.append(task[0])
            # For progress display: current task is the last one processed
            in_progress = task[0]
            # Next items: tasks not yet completed
            next_items = [t[0] for t in tasks if t[0] not in completed]
            display_progress(completed, in_progress, next_items, len(completed), total)
