from langchain_core.documents import Document

from app.core.config import settings
from app.rag.embeddings import build_embeddings


class VectorStore:
    def __init__(self) -> None:
        self._store = None

    def _get_store(self):
        if self._store is not None:
            return self._store

        try:
            from langchain_community.vectorstores import Chroma
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install langchain-community and chromadb.") from exc

        self._store = Chroma(
            collection_name=settings.collection_name,
            embedding_function=build_embeddings(),
            persist_directory=str(settings.chroma_dir),
        )
        return self._store

    async def add_documents(self, chunks: list[Document]) -> int:
        if not chunks:
            return 0
        store = self._get_store()
        ids = [chunk.metadata["chunk_id"] for chunk in chunks]
        await store.aadd_documents(chunks, ids=ids)
        return len(chunks)

    async def similarity_search(self, query: str, top_k: int) -> list[tuple[Document, float]]:
        store = self._get_store()
        return await store.asimilarity_search_with_relevance_scores(query, k=top_k)
