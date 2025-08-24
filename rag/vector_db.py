from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, Qdrant
from rag.config import CHROMA_PATH, QDRANT_URL, QDRANT_API_KEY

def get_embeddings(model_name="all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)

def build_vector_db(docs, embeddings, backend="chroma"):
    if backend == "chroma":
        return Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_PATH)
    elif backend == "qdrant":
        return Qdrant.from_documents(docs, embeddings, url=QDRANT_URL, api_key=QDRANT_API_KEY, collection_name="healthbridge-docs")
    else:
        raise Exception("Unknown vector db backend")
