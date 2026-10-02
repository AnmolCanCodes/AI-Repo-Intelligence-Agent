import os
from typing import List, Set
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.config.settings import settings
from app.retrieval.embeddings import create_embeddings


def generate_chunk_ids(chunks: List[Document]) -> List[str]:
    """Generates unique deterministic IDs for every chunk based on path and index."""
    file_counters = {}
    chunk_ids = []

    for chunk in chunks:
        file_path = chunk.metadata.get("file_path", "unknown")
        counter = file_counters.get(file_path, 0)
        
        # ID format: "auth/routes.py::0", "auth/routes.py::1"
        chunk_id = f"{file_path}::{counter}"
        chunk_ids.append(chunk_id)
        
        file_counters[file_path] = counter + 1

    return chunk_ids


def create_vectorstore(chunks: List[Document], save_path: str = None) -> FAISS:
    """Creates FAISS vectorstore with explicit, deterministic IDs for easy eviction."""
    embeddings = create_embeddings()
    chunk_ids = generate_chunk_ids(chunks)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
        ids=chunk_ids  # Attach explicit IDs
    )

    persist_dir = save_path or settings.VECTORSTORE_DIRECTORY
    os.makedirs(persist_dir, exist_ok=True)
    vectorstore.save_local(persist_dir)

    return vectorstore


def load_vectorstore() -> FAISS:
    """Loads the FAISS vectorstore from the persisted directory."""
    embeddings = create_embeddings()
    persist_dir = settings.VECTORSTORE_DIRECTORY
    vectorstore = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
    return vectorstore


def delete_chunks_by_filepaths(vectorstore: FAISS, file_paths: Set[str]) -> None:
    """Evicts all chunk vectors associated with specific relative file paths (Fixes Ghost Chunks)."""
    if not file_paths:
        return

    # Scan internal docstore to find vector IDs matching the target file paths
    ids_to_delete = []
    for doc_id, doc in vectorstore.docstore._dict.items():
        if doc.metadata.get("file_path") in file_paths:
            ids_to_delete.append(doc_id)

    if ids_to_delete:
        vectorstore.delete(ids_to_delete)
        print(f"[FAISS Eviction] Evicted {len(ids_to_delete)} stale vectors across {len(file_paths)} files.")