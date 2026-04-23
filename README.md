# Document Review - Simple RAG Q&A App

A simple local Retrieval-Augmented Generation app built with Python, FastAPI, Streamlit, LangChain, Groq API, and Gemma. Users can upload a PDF or document, index it, and ask questions based on the uploaded content.

## Features

- Async FastAPI backend for document upload, ingestion, querying, and health checks
- Simple Streamlit frontend for upload and Q&A
- Modular RAG architecture with replaceable LLM, embedding, vector store, and loader layers
- Groq-hosted Gemma model integration via `langchain-groq`
- HuggingFace sentence-transformer embeddings
- Chroma persistent vector index
- PDF, DOCX, TXT, and Markdown ingestion
- Retrieval metadata and source citations in responses
- Testable chunking and vector-store boundaries

## Project Structure

```text
app/
  api/              FastAPI routers
  core/             settings and logging
  models/           Pydantic request/response schemas
  rag/              ingestion, chunking, retrieval, LLM, pipeline
  services/         application services
  utils/            shared helpers
frontend/           Streamlit user interface
data/
  uploads/          uploaded source documents
  indexes/          persistent vector indexes
tests/              unit tests
```

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GROQ_API_KEY`.

Run the FastAPI backend:

```powershell
uvicorn app.main:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health

In a second terminal, run the Streamlit frontend:

```powershell
streamlit run frontend/streamlit_app.py
```

Open the Streamlit URL shown in the terminal, usually:

- Frontend: http://localhost:8501

## Recommended Local Workflow

1. Start FastAPI with `uvicorn app.main:app --reload`.
2. Start Streamlit with `streamlit run frontend/streamlit_app.py`.
3. Upload a PDF, DOCX, TXT, or Markdown file.
4. Click `Index document`.
5. Ask a question and review the answer with sources.

## API Usage

Upload and ingest a document:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/documents" `
  -F "file=@sample.pdf"
```

Ask a question:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/query" `
  -H "Content-Type: application/json" `
  -d "{\"question\":\"What is this document about?\",\"top_k\":4}"
```

## Tests and Quality

```powershell
pytest
ruff check .
```

## GitHub Push

After creating an empty GitHub repository:

```powershell
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

If your GitHub account requires a token for HTTPS, use Git Credential Manager when prompted or use SSH:

```powershell
git remote set-url origin git@github.com:<your-username>/<repo-name>.git
git push -u origin main
```
