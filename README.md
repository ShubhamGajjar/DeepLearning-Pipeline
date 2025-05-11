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
*   **Deep Learning Framework:** PyTorch (with CUDA 12.2 support)
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

```text
DeepLearning-Pipeline/
├── .dvc/                     # DVC metadata and cache configuration
├── .github/
│   └── workflows/            # GitHub Actions for CI/CD (e.g., testing, linting)
├── .dockerignore             # Specifies intentionally untracked files for Docker
├── .gitignore                # Specifies intentionally untracked files for Git
├── data/
│   ├── raw/                  # Raw input documents (e.g., PDFs, TXTs) - Tracked by DVC
│   └── processed/            # Processed data (e.g., chunked text, embeddings) - Tracked by DVC
├── models/                   # Trained/downloaded models (large files tracked by DVC or logged by MLflow)
├── notebooks/                # Jupyter notebooks for exploration, experimentation
├── src/                      # Source code for the application
│   ├── data_processing/      # Modules for document loading, cleaning, and chunking
│   │   ├── __init__.py
│   │   ├── loader.py         # Functions to load and extract text from various file types
│   │   └── chunker.py        # Functions for text splitting strategies
│   ├── embedding/            # Modules for generating text embeddings
│   │   ├── __init__.py
│   │   └── embedder.py       # Functions to create embeddings using sentence transformers
│   ├── vector_store/         # Modules for interacting with the vector database
│   │   ├── __init__.py
│   │   └── faiss_store.py    # FAISS implementation for storing and querying embeddings
│   ├── llm/                    # Modules for interacting with the Language Model
│   │   ├── __init__.py
│   │   └── generator.py      # Functions for prompting the LLM and generating responses/summaries
│   ├── pipeline/               # Orchestrates the RAG workflow
│   │   ├── __init__.py
│   │   └── rag_pipeline.py   # Core logic combining retrieval and generation
│   ├── api/                    # FastAPI application and related modules
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app definition, endpoints
│   │   ├── schemas.py        # Pydantic models for request/response validation
│   │   └── dependencies.py   # Shared dependencies for API routes (e.g., RAG pipeline instance)
│   └── core/                   # Core utilities, configuration, and constants
│       ├── __init__.py
│       ├── config.py         # Application configuration (e.g., model names, paths)
│       └── utils.py          # Common utility functions
├── tests/                    # Unit and integration tests using pytest
│   ├── __init__.py
│   ├── test_data_processing.py
│   ├── test_embedding.py
│   └── test_api.py
├── .env.example              # Example environment variables file
├── app.py                    # Main entry point to run the FastAPI application (if not combined with api/main.py)
├── Dockerfile                # Instructions to build the Docker image
├── docker-compose.yml        # (Optional) For multi-container setups (e.g., app + vector DB service)
├── requirements.txt          # Python dependencies (generated by `uv pip freeze`)
├── dvc.yaml                  # DVC pipeline definition file
├── params.yaml               # Parameters for DVC stages (e.g., chunk size, model names)
└── README.md                 # This file!
```

## Setup and Running (To be detailed as project progresses)
1.  Clone the repository.
2.  Install dependencies using `uv`.
3.  Set up DVC.
4.  Run the application (locally or via Docker).
