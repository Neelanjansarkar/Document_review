from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from app.core.config import settings
from app.models.schemas import DocumentIngestResponse, QueryRequest, QueryResponse
from app.rag.chunking import ContextAwareChunker
from app.rag.document_loader import DocumentLoader
from app.rag.pipeline import RAGPipeline
from app.rag.vector_store import VectorStore
from app.utils.file_utils import safe_filename


class DocumentService:
    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.chunker = ContextAwareChunker(settings.chunk_size, settings.chunk_overlap)
        self.vector_store = VectorStore()
        self.pipeline = RAGPipeline(vector_store=self.vector_store)

    async def ingest_upload(self, file: UploadFile) -> DocumentIngestResponse:
        filename = safe_filename(file.filename or "document")
        suffix = Path(filename).suffix.lower()
        if suffix not in self.loader.supported_extensions:
            raise ValueError("Unsupported file type. Upload PDF, DOCX, TXT, or Markdown.")

        document_id = uuid4().hex
        target_path = settings.upload_dir / f"{document_id}_{filename}"
        await self._save_upload(file, target_path)

        documents = self.loader.load(target_path)
        if not documents:
            raise ValueError("No readable text found in the uploaded document.")

        for document in documents:
            document.metadata["document_id"] = document_id
            document.metadata["original_filename"] = filename

        chunks = self.chunker.split(documents)
        indexed_count = await self.vector_store.add_documents(chunks)
        return DocumentIngestResponse(
            document_id=document_id,
            filename=filename,
            chunks_indexed=indexed_count,
        )

    async def answer(self, request: QueryRequest) -> QueryResponse:
        return await self.pipeline.answer(request.question, request.top_k)

    @staticmethod
    async def _save_upload(file: UploadFile, target_path: Path) -> None:
        async with aiofiles.open(target_path, "wb") as out_file:
            while content := await file.read(1024 * 1024):
                await out_file.write(content)
