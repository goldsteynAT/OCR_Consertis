import os
import pathlib
import fitz  # PyMuPDF
from typing import Iterator, List

def get_output_directory(pdf_path: str, input_base: str, output_base: str) -> str:
    """
    Berechnet das Zielverzeichnis für eine PDF, basierend auf ihrer relativen Position
    im input_base-Verzeichnis, und erstellt das Verzeichnis im output_base, falls nicht vorhanden.
    """
    rel_dir = os.path.relpath(os.path.dirname(pdf_path), input_base)
    target_dir = os.path.join(output_base, rel_dir)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def convert_pdf_to_images(pdf_path: str, output_dir: str) -> List[str]:
    """
    Öffnet ein PDF mit PyMuPDF und speichert jede Seite als PNG-Bild im output_dir.
    Gibt eine Liste der erstellten Bildpfade zurück.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Fehler beim Öffnen der PDF-Datei {pdf_path}: {e}")

    output_files = []
    base_name = pathlib.Path(pdf_path).stem
    for page_number in range(doc.page_count):
        page = doc[page_number]
        zoom_x, zoom_y = 2.5, 2.5  # Höhere DPI für bessere Bildqualität
        matrix = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=matrix)

        output_file = os.path.join(output_dir, f"{base_name}_seite_{page_number + 1}.png")
        try:
            pix.save(output_file)
            output_files.append(output_file)
        except Exception as e:
            print(f"Fehler beim Speichern von Seite {page_number + 1} aus {pdf_path}: {e}")
    doc.close()
    return output_files

def process_pdf_files(input_path: str) -> Iterator[str]:
    """
    Sucht alle PDF-Dateien im angegebenen input_path.
    Bei einem Ordner werden alle PDFs (auch in Unterordnern) gefunden.
    Bei einer einzelnen PDF wird diese zurückgegeben.
    """
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    yield os.path.join(root, file)
    elif os.path.isfile(input_path) and input_path.lower().endswith(".pdf"):
        yield input_path
    else:
        raise ValueError("Der angegebene Pfad muss eine PDF-Datei oder ein Ordner mit PDF-Dateien sein.")

def batch_convert_pdfs(input_path: str, output_base: str) -> None:
    """
    Batch-Konvertierung: Durchläuft alle PDF-Dateien im input_path, berechnet für jede
    den entsprechenden Zielordner im output_base und wandelt die PDFs in PNGs um.
    Zeigt den Fortschritt im Terminal an.
    """
    pdf_files = list(process_pdf_files(input_path))
    total = len(pdf_files)
    if total == 0:
        print("Keine PDF-Dateien gefunden.")
        return

    print(f"Starte Konvertierung von {total} PDF(s)...")
    for idx, pdf_file in enumerate(pdf_files, start=1):
        target_dir = get_output_directory(pdf_file, input_path, output_base)
        print(f"[{idx}/{total}] Verarbeite: {pdf_file} -> Ziel: {target_dir}")
        try:
            images = convert_pdf_to_images(pdf_file, target_dir)
            print(f"  -> {len(images)} Seite(n) als PNG gespeichert.")
        except Exception as e:
            print(f"  -> Fehler bei der Verarbeitung von {pdf_file}: {e}")

if __name__ == "__main__":
    # Beispielaufruf:
    input_path = r"pfad\zum\pdf_ordner"       # Pfad zum Ordner mit den Quell-PDFs
    output_base = r"pfad\zum\ausgabeordner"    # Basis-Ausgabeverzeichnis für PNGs

    batch_convert_pdfs(input_path, output_base)
