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

# Example usage (optional, for testing the module directly)
if __name__ == "__main__":
    # Create dummy files for testing
    Path("temp_test_docs").mkdir(exist_ok=True)
    with open("temp_test_docs/sample.txt", "w") as f:
        f.write("This is a sample text document.\nIt has multiple lines.")

    # Create a dummy PDF (requires a library like reportlab, or use an existing small PDF)
    # For simplicity, we'll assume you have a sample.pdf in 'temp_test_docs' if you want to test PDF loading.
    # If not, PDF loading test will be skipped or error out gracefully in the example.
    
    # Example: Create a simple PDF using PyMuPDF for testing if you don't have one
    try:
        pdf_path = Path("temp_test_docs/sample.pdf")
        if not pdf_path.exists(): # Only create if it doesn't exist
            doc = fitz.open() # new empty PDF
            page = doc.new_page()
            page.insert_text((72, 72), "This is page 1 of a sample PDF.")
            page = doc.new_page()
            page.insert_text((72, 72), "This is page 2 of the sample PDF.")
            doc.save(str(pdf_path))
            doc.close()
            print(f"Created dummy PDF: {pdf_path}")
    except Exception as e:
        print(f"Could not create dummy PDF for testing: {e}")


    print("\n--- Testing load_text_document ---")
    try:
        txt_docs = load_text_document("temp_test_docs/sample.txt")
        for content, meta in txt_docs:
            print(f"Content: '{content[:50]}...', Metadata: {meta}")
    except Exception as e:
        print(f"Error testing load_text_document: {e}")

    print("\n--- Testing load_pdf_document ---")
    if Path("temp_test_docs/sample.pdf").exists():
        try:
            pdf_docs = load_pdf_document("temp_test_docs/sample.pdf")
            for content, meta in pdf_docs:
                print(f"Content: '{content[:50]}...', Metadata: {meta}")
        except Exception as e:
            print(f"Error testing load_pdf_document: {e}")
    else:
        print("Skipping PDF test, sample.pdf not found in temp_test_docs/")
        

    print("\n--- Testing load_documents (from directory) ---")
    try:
        all_loaded_docs = load_documents("temp_test_docs")
        print(f"Total documents/pages loaded: {len(all_loaded_docs)}")
        for i, (content, meta) in enumerate(all_loaded_docs):
            if i < 3: # Print details for first few
                 print(f"Doc {i+1}: Content='{content[:30].strip().replace(chr(10), '')}...', Meta={meta}")
    except Exception as e:
        print(f"Error testing load_documents: {e}")

    # Clean up dummy files (optional)
    # import shutil
    # shutil.rmtree("temp_test_docs")
    # print("\nCleaned up temp_test_docs directory.")