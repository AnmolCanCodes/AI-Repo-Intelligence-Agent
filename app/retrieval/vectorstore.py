
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config.settings import settings
from app.retrieval.embeddings import create_embeddings


def create_vectorstore(
    chunks: list[Document],
    save_path: str | None = None
) -> FAISS:
    """
    Creates a FAISS vectorstore from code chunks
    and saves it locally.
    """

    if not chunks:
        raise ValueError(
            "Cannot create vectorstore: no chunks provided."
        )

    embeddings = create_embeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    persist_dir = Path(
        save_path or settings.VECTORSTORE_DIRECTORY
    )

    persist_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(str(persist_dir))

    return vectorstore


def load_vectorstore(
    load_path: str | None = None
) -> FAISS:
    """
    Loads an existing FAISS vectorstore from disk.
    """

    embeddings = create_embeddings()

    persist_dir = Path(
        load_path or settings.VECTORSTORE_DIRECTORY
    )

    if not persist_dir.exists():
        raise FileNotFoundError(
            f"Vector store not found at {persist_dir}"
        )

    return FAISS.load_local(
        folder_path=str(persist_dir),
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )