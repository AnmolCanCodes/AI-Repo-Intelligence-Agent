from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings():
    """Initializes and returns the HuggingFace sentence transformer embedding model."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )