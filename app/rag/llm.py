from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import settings


class GroqGemmaClient:
    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")

        try:
            from langchain_groq import ChatGroq
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install langchain-groq to enable Groq LLM responses.") from exc

        self._client = ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.groq_model,
            temperature=0.1,
            max_tokens=700,
        )
        return self._client

    async def answer(self, question: str, context: str) -> str:
        client = self._get_client()
        messages = [
            SystemMessage(
                content=(
                    "You are a precise document Q&A assistant. Answer only from the supplied "
                    "context. If the context is insufficient, say you do not know. Include concise "
                    "reasoning and avoid inventing facts."
                )
            ),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}"),
        ]
        response = await client.ainvoke(messages)
        return str(response.content)
