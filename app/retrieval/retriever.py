from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def create_retriever(vectorstore: FAISS, k: int = 5):
    """Creates a retriever interface from a FAISS vectorstore."""
    # Fixed typo: search_kwargs (not search_kwags)
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )


def retrieve_relevant_chunks(vectorstore: FAISS, query: str, k: int = 5) -> List[Document]:
    """Helper function to directly query top-k relevant code chunks for a given question."""
    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )
    retriever = create_retriever(vectorstore, k=k)
    return retriever.invoke(query)