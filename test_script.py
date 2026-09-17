
from app.ingestion.github import GitHubIngestion
from app.ingestion.scanner import scan_repository
from app.ingestion.chunker import chunk_files

from app.retrieval.vectorstore import create_vectorstore
from app.retrieval.retriever import retrieve_relevant_chunks


def main():
    repo_url = "https://github.com/AnmolCanCodes/Youtube-research-tool"

    ingestion = GitHubIngestion()

    repo_path, repo_name = ingestion.clone_repository(
        repo_url
    )

    try:
        files = scan_repository(repo_path)

        print(f"Files found: {len(files)}")

        chunks = chunk_files(
            files,
            repo_path
        )

        print(f"Chunks created: {len(chunks)}")

        vectorstore = create_vectorstore(chunks)

        results = retrieve_relevant_chunks(
            vectorstore,
            "Where is authentication implemented?",
            k=5
        )

        for index, document in enumerate(results, start=1):
            print(f"\n--- Result {index} ---")
            print(
                "File:",
                document.metadata.get("file_path")
            )
            print(
                "Language:",
                document.metadata.get("language")
            )
            print(document.page_content[:500])

    finally:
        # Keep the clone during early development if needed.
        # Cleanup can be enabled once ingestion is stable.
        pass


if __name__ == "__main__":
    main()