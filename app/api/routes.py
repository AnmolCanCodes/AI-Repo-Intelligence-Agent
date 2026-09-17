from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl

from app.ingestion.github import GitHubIngestion
from app.ingestion.scanner import scan_repository
from app.ingestion.chunker import chunk_files
from app.retrieval.vectorstore import create_vectorstore
from app.graph.graph import graph_app

router = APIRouter()


# Request/Response Schemas
class RepositoryRequest(BaseModel):
    url: str


class RepositoryResponse(BaseModel):
    message: str
    repo_name: str
    files_scanned: int
    chunks_indexed: int


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    referenced_files: List[str]


@router.post(
    "/repository",
    response_model=RepositoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest a GitHub repository",
    description="Clones a GitHub repository, scans supported files, chunks code, and builds the FAISS vector index.",
)
async def ingest_repository(payload: RepositoryRequest):
    ingestor = GitHubIngestion()
    local_repo_path = None

    try:
        # 1. Clone repository
        local_repo_path, repo_name = ingestor.clone_repository(payload.url)

        # 2. Scan repository for supported source code files
        valid_files = scan_repository(local_repo_path)
        if not valid_files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No supported source code files found in the repository.",
            )

        # 3. Chunk source code files while preserving relative path metadata
        chunks = chunk_files(valid_files, repo_base_path=local_repo_path)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to extract readable content or generate chunks from repository files.",
            )

        # 4. Embed chunks and save to FAISS vectorstore
        create_vectorstore(chunks)

        return RepositoryResponse(
            message="Repository successfully ingested and indexed.",
            repo_name=repo_name,
            files_scanned=len(valid_files),
            chunks_indexed=len(chunks),
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting repository: {str(e)}",
        )

    finally:
        # Clean up temporary clone directory
        if local_repo_path:
            ingestor.cleanup(local_repo_path)


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question about the indexed repository",
    description="Executes the LangGraph workflow to retrieve code context and generate a response.",
)
async def chat_with_repo(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty.",
        )

    try:
        # Run state machine graph
        initial_state = {"question": payload.question}
        final_state = graph_app.invoke(initial_state)

        # Collect unique file paths from retrieved documents metadata
        retrieved_docs = final_state.get("retrieved_documents", [])
        referenced_files = list(
            {
                doc.metadata.get("file_path")
                for doc in retrieved_docs
                if doc.metadata.get("file_path")
            }
        )

        return ChatResponse(
            question=payload.question,
            answer=final_state.get("answer", "No answer generated."),
            referenced_files=referenced_files,
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No repository index found. Please ingest a repository via /repository first.",
        ) from e
    except ValueError as e:
        if "HF_TOKEN" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e),
            ) from e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}",
        ) from e