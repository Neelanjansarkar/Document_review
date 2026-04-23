import pytest
from langchain_core.documents import Document

from app.rag.pipeline import RAGPipeline


class FakeVectorStore:
    async def similarity_search(self, query: str, top_k: int):
        return [
            (
                Document(
                    page_content="FastAPI exposes async endpoints for document question answering.",
                    metadata={"source": "architecture.md", "page": 1, "chunk_id": "architecture.md:p1:c0"},
                ),
                0.91,
            )
        ]


class FakeLLM:
    async def answer(self, question: str, context: str) -> str:
        return "The backend uses async FastAPI endpoints for Q&A."


@pytest.mark.asyncio
async def test_rag_pipeline_returns_answer_with_sources() -> None:
    pipeline = RAGPipeline(vector_store=FakeVectorStore(), llm=FakeLLM())

    response = await pipeline.answer("How does the backend expose Q&A?", top_k=1)

    assert "FastAPI" in response.answer
    assert response.sources[0].source == "architecture.md"
