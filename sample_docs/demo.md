# Demo Architecture Notes

The application exposes document question answering through async FastAPI endpoints.

Uploaded documents are saved, parsed, split into overlapping semantic chunks, embedded with a sentence-transformer model, and stored in Chroma.

When a user asks a question, the API retrieves the most relevant chunks and sends them to Gemma through the Groq API. The final answer includes source metadata so users can inspect where the answer came from.
