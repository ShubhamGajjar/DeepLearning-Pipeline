# src/data_processing/loader.py
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Union, Tuple

# Supported file types and their loading functions
LOADER_MAPPING = {
    ".pdf": lambda path: load_pdf_document(path),
    ".txt": lambda path: load_text_document(path),
    # Add more mappings here for .docx, .md, etc. if needed later
}

def load_pdf_document(file_path: Union[str, Path]) -> List[Tuple[str, Dict]]:
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {file_path}")

    documents = []
    try:
        doc = fitz.open(path)
        for page_num, page in enumerate(doc):
            text = page.get_text("text") # "text" for plain text, "html" for more structure, "dict" for detailed
            if text.strip(): # Only add if there's actual text
                documents.append((text, {"source": str(path.name), "page": page_num + 1}))
        doc.close()
    except Exception as e:
        print(f"Error processing PDF {path.name}: {e}")
        # Optionally re-raise or return empty list / partial data
        # For now, we'll let it propagate if it's a fitz error, or print and continue if not.
        # Depending on desired robustness, could add more specific error handling here.
        raise  # Re-raise the exception to be handled upstream or logged
    return documents

def load_text_document(file_path: Union[str, Path]) -> List[Tuple[str, Dict]]:
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.suffix.lower() != ".txt":
        raise ValueError(f"File is not a TXT file: {file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if text.strip():
            return [(text, {"source": str(path.name)})]
        else:
            return [] # Return empty list if file is empty or only whitespace
    except Exception as e:
        print(f"Error processing TXT file {path.name}: {e}")
        raise
    return []


def load_documents(source_dir: Union[str, Path]) -> List[Tuple[str, Dict]]:
    source_path = Path(source_dir)
    if not source_path.exists() or not source_path.is_dir():
        raise FileNotFoundError(f"Source directory not found or is not a directory: {source_dir}")

    all_documents = []
    for file_path in source_path.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext in LOADER_MAPPING:
                try:
                    print(f"Loading document: {file_path.name}")
                    loaded_docs = LOADER_MAPPING[ext](file_path)
                    all_documents.extend(loaded_docs)
                except Exception as e:
                    print(f"Failed to load {file_path.name}: {e}")
            else:
                print(f"Skipping unsupported file type: {file_path.name}")
    
    if not all_documents:
        print(f"No documents successfully loaded from {source_dir}. Check file types and content.")

    return all_documents

# Example usage (modified for manual input)
if __name__ == "__main__":
    from pathlib import Path

    # Default directory to look for files if only a filename is given
    default_data_dir = Path("data/raw")
    print(f"Default search directory for files if no full path is given: {default_data_dir.resolve()}")
    print("You can also provide an absolute path to a file.")

    while True:
        file_input = input("\nEnter the path to a PDF or TXT file (or type 'all' to load from data/raw, or 'quit' to exit): ").strip()

        if file_input.lower() == 'quit':
            break
        elif file_input.lower() == 'all':
            print(f"\n--- Loading all supported documents from '{default_data_dir}' ---")
            try:
                if default_data_dir.exists() and default_data_dir.is_dir():
                    all_loaded_docs = load_documents(default_data_dir)
                    print(f"Total documents/pages loaded: {len(all_loaded_docs)}")
                    for i, (content, meta) in enumerate(all_loaded_docs):
                        if i < 5: # Print details for first few
                            print(f"  Doc {i+1}: Content='{content[:70].strip().replace(chr(10), ' ')}...', Meta={meta}")
                else:
                    print(f"Directory {default_data_dir} not found or is not a directory.")
            except Exception as e:
                print(f"Error loading all documents: {e}")
            continue # Go back to prompt

        # Try to resolve the input as a path
        # If it's just a filename, assume it's in default_data_dir
        file_path_obj = Path(file_input)
        if not file_path_obj.is_absolute() and not file_path_obj.exists():
            # If not absolute and doesn't exist as is, try prepending default_data_dir
            file_path_obj = default_data_dir / file_input

        if not file_path_obj.exists() or not file_path_obj.is_file():
            print(f"Error: File not found or is not a file: {file_path_obj}")
            continue

        ext = file_path_obj.suffix.lower()
        loaded_file_docs = []

        try:
            if ext == ".pdf":
                print(f"\n--- Loading PDF: {file_path_obj.name} ---")
                loaded_file_docs = load_pdf_document(file_path_obj)
            elif ext == ".txt":
                print(f"\n--- Loading TXT: {file_path_obj.name} ---")
                loaded_file_docs = load_text_document(file_path_obj)
            else:
                print(f"Unsupported file type: {ext}. Please provide a .pdf or .txt file.")
                continue

            if loaded_file_docs:
                print(f"Successfully loaded {len(loaded_file_docs)} item(s) from {file_path_obj.name}:")
                for i, (content, meta) in enumerate(loaded_file_docs):
                    print(f"  Item {i+1}:")
                    print(f"    Metadata: {meta}")
                    print(f"    Content Preview: '{content[:150].strip().replace(chr(10), ' ')}...'") # Show a bit more
            else:
                print(f"No content loaded from {file_path_obj.name} (file might be empty or unsupported).")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path_obj}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {file_path_obj.name}: {e}")