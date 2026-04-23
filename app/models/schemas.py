from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str


class DocumentIngestResponse(BaseModel):
    document_id: str
    filename: str
    chunks_indexed: int
    message: str = "Document indexed successfully."


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=12)


class SourceChunk(BaseModel):
    source: str
    page: int | None = None
    chunk_id: str
    score: float | None = None
    preview: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    latency_ms: float
