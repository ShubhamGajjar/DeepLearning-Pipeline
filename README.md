# Intelligent Document Assistant: A Deep Learning Production Pipeline

This project implements an Intelligent Document Assistant using a Retrieval Augmented Generation (RAG) approach. It serves as a demonstration of a full MLOps pipeline, from data ingestion and model training/selection to API deployment and containerization.

The assistant allows users to upload multiple documents (PDF, TXT) and then ask questions about their content or request summaries.

## Features
*   **Multiple Document Upload:** Supports PDF and TXT file formats.
*   **Question Answering:** Ask natural language questions about the uploaded documents.
*   **Summarization:** Generate concise summaries of individual documents or selections.
*   **Advanced Retrieval:** (Planned) Explore techniques beyond simple semantic search for better context retrieval.
*   **RESTful API:** Exposes functionality via a FastAPI backend.
*   **Dockerized Deployment:** Packaged for easy deployment using Docker.
*   **MLOps Practices:** Incorporates Git, DVC for data/model versioning, MLflow (or W&B) for experiment tracking, and automated testing.

## Tech Stack (Initial Plan)
*   **Programming Language:** Python 3.12
*   **Deep Learning Framework:** PyTorch (with CUDA 12.1 support)
*   **Core AI/ML Libraries:**
    *   `transformers` (Hugging Face for LLMs and embedding models)
    *   `sentence-transformers` (for efficient text embeddings)
    *   `faiss-gpu` (or `faiss-cpu`, for vector storage and similarity search)
    *   `bitsandbytes` (for LLM quantization)
*   **API Framework:** FastAPI
*   **Web Server:** Uvicorn
*   **Data Handling:**
    *   `pypdf2` / `pymupdf` (for PDF processing)
    *   `unstructured` (for diverse document parsing)
    *   `langchain` (or `llama-index` - for RAG framework components, TBD)
*   **Containerization:** Docker, Docker Compose
*   **Version Control:** Git, GitHub
*   **Data & Model Versioning:** DVC (Data Version Control)
*   **Experiment Tracking:** MLflow (or Weights & Biases)
*   **Testing:** `pytest`
*   **Package Management:** `uv`

## GPU Optimization Techniques
*   **Mixed Precision (AMP):** Utilizing Automatic Mixed Precision for faster training/inference where applicable.
*   **Quantization:** Using techniques like 4-bit/8-bit loading for LLMs (e.g., via `bitsandbytes`) to reduce memory footprint.
*   **Optimized Kernels:** Leveraging libraries like FlashAttention (if supported by models and hardware) for attention mechanisms.
*   **Efficient Batching:** For embedding generation and LLM inference.
*   **ONNX Runtime:** (Potential) Exporting models to ONNX for optimized inference.

## Project Structure (Initial Draft)


## Setup and Running (To be detailed as project progresses)
1.  Clone the repository.
2.  Install dependencies using `uv`.
3.  Set up DVC.
4.  Run the application (locally or via Docker).
