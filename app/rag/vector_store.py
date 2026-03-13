import os
import faiss
import pickle
import numpy as np

from app.rag.embedder import embed_text

VECTOR_DB_DIR = "data/vector_db"
VECTOR_DB_PATH = os.path.join(VECTOR_DB_DIR, "faiss_index")
TEXT_STORE_PATH = os.path.join(VECTOR_DB_DIR, "texts.pkl")


class VectorStore:

    def __init__(self):

        self.dimension = 384  # embedding size for MiniLM

        # Ensure directory exists
        os.makedirs(VECTOR_DB_DIR, exist_ok=True)

        # If index exists → load it
        if os.path.exists(VECTOR_DB_PATH):

            try:
                self.index = faiss.read_index(VECTOR_DB_PATH)

                if os.path.exists(TEXT_STORE_PATH):
                    with open(TEXT_STORE_PATH, "rb") as f:
                        self.texts = pickle.load(f)
                else:
                    self.texts = []

            except Exception as e:
                # fallback if file corrupted
                print("⚠️ FAISS index corrupted, creating new index:", e)
                self.index = faiss.IndexFlatL2(self.dimension)
                self.texts = []

        else:
            # Create new FAISS index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.texts = []

    def add_documents(self, documents):

        # Prevent adding empty documents
        if not documents:
            return

        embeddings = embed_text(documents)

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)

        self.texts.extend(documents)

        # Persist FAISS index
        self.save()

    def save(self):

        # Ensure directory exists
        os.makedirs(VECTOR_DB_DIR, exist_ok=True)

        faiss.write_index(self.index, VECTOR_DB_PATH)

        with open(TEXT_STORE_PATH, "wb") as f:
            pickle.dump(self.texts, f)

    def search(self, query, k=5):

        if len(self.texts) == 0:
            return []

        query_embedding = embed_text([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])

        return results