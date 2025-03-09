import json
import os

def load_status(status_file: str) -> list:
    """
    Loads the list of processed PDFs from a JSON status file.
    
    Args:
        status_file (str): Path to the status file.
    
    Returns:
        list: List of normalized processed PDF file paths.
    """
    if status_file and os.path.exists(status_file):
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    # Normalize each path
                    return [os.path.normpath(os.path.abspath(p)) for p in data]
        except Exception as e:
            print(f"Error loading status file: {e}")
    return []

def save_status(status_file: str, processed: list) -> None:
    """
    Saves the list of processed PDFs to a JSON status file.
    
    Args:
        status_file (str): Path to the status file.
        processed (list): List of normalized processed PDF file paths.
    """
    try:
        if status_file:
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(processed, f, indent=4)
    except Exception as e:
        print(f"Error saving status file: {e}")
