# API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

## `GET /health`

Returns application health.

## `POST /documents`

Uploads and indexes a document.

Form field:

- `file`: PDF, DOCX, TXT, or Markdown file

Response:

```json
{
  "document_id": "a9f...",
  "filename": "sample.pdf",
  "chunks_indexed": 12,
  "message": "Document indexed successfully."
}
```

## `POST /query`

Runs semantic retrieval and generates a grounded answer.

Request:

```json
{
  "question": "What are the main risks?",
  "top_k": 4
}
```

Response:

```json
{
  "answer": "The main risks are ...",
  "sources": [
    {
      "source": "sample.pdf",
      "page": 2,
      "chunk_id": "sample.pdf:p2:c3",
      "score": 0.82,
      "preview": "The document states ..."
    }
  ],
  "latency_ms": 842.12
}
```
