from app.rag.vector_store import VectorStore

vector_store = VectorStore()


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks for RAG indexing
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def index_documents(text):
    """
    Add document chunks to FAISS
    """

    chunks = chunk_text(text)

    vector_store.add_documents(chunks)


def retrieve_documents(query, top_k=5):
    """
    Retrieve relevant chunks
    """

    results = vector_store.search(query, k=top_k)

    return results