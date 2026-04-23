from time import perf_counter

from app.core.config import settings
from app.models.schemas import QueryResponse, SourceChunk
from app.rag.llm import GroqGemmaClient
from app.rag.vector_store import VectorStore


class RAGPipeline:
    def __init__(self, vector_store: VectorStore | None = None, llm: GroqGemmaClient | None = None) -> None:
        self.vector_store = vector_store or VectorStore()
        self.llm = llm or GroqGemmaClient()

    async def answer(self, question: str, top_k: int | None = None) -> QueryResponse:
        started = perf_counter()
        resolved_top_k = top_k or settings.top_k
        matches = await self.vector_store.similarity_search(question, resolved_top_k)
        filtered = [
            (doc, score)
            for doc, score in matches
            if score is None or score >= settings.score_threshold
        ]

        if not filtered:
            latency_ms = (perf_counter() - started) * 1000
            return QueryResponse(
                answer="I do not know based on the indexed documents.",
                sources=[],
                latency_ms=round(latency_ms, 2),
            )

        context = self._format_context(filtered)
        answer = await self.llm.answer(question, context)
        latency_ms = (perf_counter() - started) * 1000
        return QueryResponse(
            answer=answer,
            sources=[self._source_from_match(doc, score) for doc, score in filtered],
            latency_ms=round(latency_ms, 2),
        )

    @staticmethod
    def _format_context(matches) -> str:
        blocks = []
        for doc, score in matches:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "n/a")
            blocks.append(f"[source={source}, page={page}, score={score}]\n{doc.page_content}")
        return "\n\n---\n\n".join(blocks)

    @staticmethod
    def _source_from_match(doc, score: float | None) -> SourceChunk:
        text = " ".join(doc.page_content.split())
        return SourceChunk(
            source=str(doc.metadata.get("source", "unknown")),
            page=doc.metadata.get("page"),
            chunk_id=str(doc.metadata.get("chunk_id", "")),
            score=round(score, 4) if score is not None else None,
            preview=text[:260],
        )
