from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

from app.graph.graph import graph_app
from app.ingestion.github import GitHubIngestion
from app.ingestion.scanner import scan_repository
from app.ingestion.chunker import chunk_files
from app.retrieval.vectorstore import create_vectorstore

router = APIRouter()


class MessageTurn(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[MessageTurn]] = []


class ChatResponse(BaseModel):
    question: str
    answer: str
    referenced_files: List[str]


class RepoUploadRequest(BaseModel):
    repo_url: str


class RepoUploadResponse(BaseModel):
    message: str
    repo_name: str
    files_processed: int
    chunks_created: int


@router.post("/upload-repo", response_model=RepoUploadResponse)
async def upload_repository(payload: RepoUploadRequest):
    """Clones a GitHub repository, processes it, and creates vector embeddings."""
    if not payload.repo_url.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Repository URL cannot be empty.",
        )

    try:
        # Initialize GitHub ingestion
        github_ingestion = GitHubIngestion()

        # Clone the repository
        local_repo_path, repo_name = github_ingestion.clone_repository(payload.repo_url)

        # Scan for supported files
        file_paths = scan_repository(local_repo_path)

        if not file_paths:
            github_ingestion.cleanup(local_repo_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No supported files found in the repository.",
            )

        # Chunk the files
        chunks = chunk_files(file_paths, local_repo_path)

        if not chunks:
            github_ingestion.cleanup(local_repo_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content chunks created from the repository.",
            )

        # Create vectorstore
        create_vectorstore(chunks)

        # Cleanup the cloned repository
        github_ingestion.cleanup(local_repo_path)

        return RepoUploadResponse(
            message="Repository successfully processed and indexed.",
            repo_name=repo_name,
            files_processed=len(file_paths),
            chunks_created=len(chunks),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing repository: {str(e)}",
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_with_repo(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty.",
        )

    try:
        # Convert incoming JSON history to LangChain message objects
        formatted_history = []
        for msg in payload.chat_history:
            if msg.role == "user":
                formatted_history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                formatted_history.append(AIMessage(content=msg.content))

        # Invoke graph with question and formatted history
        initial_state = {
            "question": payload.question,
            "chat_history": formatted_history
        }
        final_state = graph_app.invoke(initial_state)

        # Collect unique file paths
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

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}",
        )