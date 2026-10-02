from pathlib import Path
from typing import Set, Tuple, List
from git import Repo
from langchain_community.vectorstores import FAISS

from app.ingestion.scanner import scan_repository
from app.ingestion.chunker import chunk_files
from app.retrieval.vectorstore import delete_chunks_by_filepaths, generate_chunk_ids


def process_git_diff(
    repo_path: str, 
    old_commit: str, 
    new_commit: str
) -> Tuple[Set[str], Set[str]]:
    """Analyzes Git diff between two commits to identify modified, deleted, and added files.
    
    Returns:
        Tuple[Set[str], Set[str]]: (file_paths_to_evict, file_paths_to_reindex)
    """
    repo = Repo(repo_path)
    diff = repo.commit(old_commit).diff(repo.commit(new_commit))

    paths_to_evict: Set[str] = set()
    paths_to_reindex: Set[str] = set()

    for item in diff:
        # Deletion
        if item.deleted_file:
            paths_to_evict.add(item.a_path)
        # Modification
        elif item.a_path == item.b_path:
            paths_to_evict.add(item.a_path)
            paths_to_reindex.add(item.b_path)
        # Rename (Delete old path, index new path)
        elif item.renamed_file:
            paths_to_evict.add(item.a_path)
            paths_to_reindex.add(item.b_path)
        # Added
        elif item.new_file:
            paths_to_reindex.add(item.b_path)

    return paths_to_evict, paths_to_reindex


def incremental_reindex(
    vectorstore: FAISS,
    repo_path: str,
    old_commit: str,
    new_commit: str
) -> FAISS:
    """Updates FAISS incrementally: evicts deleted/modified vectors and inserts fresh chunks."""
    repo_base = Path(repo_path).resolve()
    
    # 1. Parse changed paths using Git
    paths_to_evict, paths_to_reindex = process_git_diff(repo_path, old_commit, new_commit)

    # 2. Evict old vectors (Solves Ghost Chunks!)
    delete_chunks_by_filepaths(vectorstore, paths_to_evict)

    # 3. Read and re-chunk modified/added files
    files_to_process = [repo_base / p for p in paths_to_reindex if (repo_base / p).exists()]
    
    if files_to_process:
        new_chunks = chunk_files(files_to_process, repo_base_path=repo_base)
        
        if new_chunks:
            new_ids = generate_chunk_ids(new_chunks)
            vectorstore.add_documents(documents=new_chunks, ids=new_ids)
            print(f"[FAISS Sync] Added {len(new_chunks)} new/updated chunks into FAISS.")

    return vectorstore