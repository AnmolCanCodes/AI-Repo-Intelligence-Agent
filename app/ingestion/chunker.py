import os
from pathlib import Path
from typing import List,Dict,Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import settings


EXTENSION_TO_LANGUAGE: Dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
}

def _detect_language(file_path:Path)->str:
    ext = file_path.suffix.lower()
    return EXTENSION_TO_LANGUAGE.get(ext,"unknown")

def chunk_files(file_paths: List[Path],repo_base_path: Path | str)-> List[Document]:
    """Reads source files, extracts content and metadata, and splits them into

    chunked LangChain Document objects.
    
    Args:
        file_paths: List of absolute or relative Path objects for scanned files.
        repo_base_path: Base directory of the repository to compute relative file paths.
        
    Returns:
        List[Document]: A list of LangChain Document objects containing chunked code
                        and metadata (content, file_path, language).
    """
    repo_base = Path(repo_base_path).resolve()
    raw_documents: List[Document] = []

    for path in file_paths:
        file_path_obj = Path(path).resolve()

        # Calculate clean relative file path (e.g., "auth/routes.py")
        try:
            rel_file_path = str(file_path_obj.relative_to(repo_base))
        except ValueError:
            rel_file_path = str(file_path_obj)

        language = _detect_language(file_path_obj)

        try:
            content = file_path_obj.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                content = file_path_obj.read_text(encoding="latin-1")
            except Exception as e:
                print(f"Skipping unreadable file {rel_file_path}:{e}")
                continue
        except Exception as e:
            print(f"Error reading file {rel_file_path}: {e}")
            continue

        if not content.strip():
            continue

        # Create base Document preserving essential metadata
        doc = Document(
            page_content=content,
            metadata={
                "file_path": rel_file_path,
                "language": language,
            }
        )
        raw_documents.append(doc)

    if not raw_documents:
        return []

    text_spiltter = RecursiveCharacterTextSplitter(
        chunk_size = settings.CHUNK_SIZE,
        chunk_overlap = settings.CHUNK_OVERLAP,
        length_function = len,
        is_separator_regex= False
    )

    chunked_documents = text_spiltter.split_documents(raw_documents)
    return chunked_documents


