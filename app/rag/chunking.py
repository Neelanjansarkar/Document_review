from langchain_core.documents import Document

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:  # pragma: no cover - handled in environments before dependencies are installed
    RecursiveCharacterTextSplitter = None


class ContextAwareChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, documents: list[Document]) -> list[Document]:
        if RecursiveCharacterTextSplitter is None:
            raise RuntimeError("Install langchain-text-splitters to enable document chunking.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True,
        )
        chunks = splitter.split_documents(documents)
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = self._chunk_id(chunk, index)
            chunk.metadata["chunk_index"] = index
        return chunks

    @staticmethod
    def _chunk_id(document: Document, index: int) -> str:
        source = str(document.metadata.get("source", "document")).replace("\\", "/")
        page = document.metadata.get("page")
        page_part = f"p{page}" if page is not None else "p0"
        return f"{source}:{page_part}:c{index}"
