from app.core.config import settings


def build_embeddings():
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install langchain-huggingface and sentence-transformers.") from exc

    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
