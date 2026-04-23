import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


st.set_page_config(page_title="Document Q&A", layout="centered")

st.title("Document Q&A")
st.caption("Upload a PDF, DOCX, TXT, or Markdown file, then ask questions from its content.")

with st.sidebar:
    st.header("Backend")
    api_base_url = st.text_input("FastAPI URL", value=API_BASE_URL)
    top_k = st.slider("Sources to retrieve", min_value=1, max_value=8, value=4)

    try:
        health = requests.get(f"{api_base_url}/health", timeout=5)
        if health.ok:
            st.success("API connected")
        else:
            st.warning("API responded with an error")
    except requests.RequestException:
        st.error("Start FastAPI first")

uploaded_file = st.file_uploader(
    "Upload document",
    type=["pdf", "docx", "txt", "md"],
    accept_multiple_files=False,
)

if uploaded_file and st.button("Index document", type="primary"):
    with st.spinner("Indexing document..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        try:
            response = requests.post(f"{api_base_url}/documents", files=files, timeout=120)
            response.raise_for_status()
            result = response.json()
            st.session_state["last_document"] = result
            st.success(f"Indexed {result['chunks_indexed']} chunks from {result['filename']}")
        except requests.RequestException as exc:
            st.error(f"Could not index document: {exc}")

if "last_document" in st.session_state:
    doc = st.session_state["last_document"]
    st.info(f"Current document: {doc['filename']}")

question = st.text_area("Ask a question", placeholder="What are the key points in this document?")

if st.button("Ask", disabled=not question.strip()):
    with st.spinner("Searching and generating answer..."):
        payload = {"question": question, "top_k": top_k}
        try:
            response = requests.post(f"{api_base_url}/query", json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()

            st.subheader("Answer")
            st.write(result["answer"])
            st.caption(f"Latency: {result['latency_ms']} ms")

            if result["sources"]:
                st.subheader("Sources")
                for source in result["sources"]:
                    label = source["source"]
                    if source.get("page"):
                        label = f"{label} - page {source['page']}"
                    with st.expander(label):
                        st.write(source["preview"])
                        st.caption(f"Chunk: {source['chunk_id']} | Score: {source.get('score')}")
        except requests.RequestException as exc:
            st.error(f"Could not get an answer: {exc}")
