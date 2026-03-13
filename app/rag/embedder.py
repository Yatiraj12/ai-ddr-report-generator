from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")


def embed_text(texts):
    """
    Convert list of text chunks into embeddings
    """
    embeddings = model.encode(texts)
    return embeddings