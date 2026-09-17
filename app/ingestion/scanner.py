
from pathlib import Path

from app.config.settings import settings


def scan_repository(
    repository_path: str | Path
) -> list[Path]:
    """
    Scans a cloned repository and returns supported files.

    Skips ignored directories and files that exceed
    the maximum configured file size.
    """

    repo_path = Path(repository_path).resolve()

    if not repo_path.exists():
        raise FileNotFoundError(
            f"Repository not found: {repo_path}"
        )

    if not repo_path.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {repo_path}"
        )

    valid_files: list[Path] = []

    for file_path in repo_path.rglob("*"):

        if not file_path.is_file():
            continue

        rel_parts = file_path.relative_to(repo_path).parts

        # Skip ignored directories and filenames
        if any(
            part in settings.IGNORED_DIRS
            for part in rel_parts
        ):
            continue

        # Only allow configured file extensions
        if file_path.suffix.lower() not in settings.ALLOWED_EXTENSIONS:
            continue

        # Skip excessively large files
        if file_path.stat().st_size > 1_000_000:
            continue

        valid_files.append(file_path)

    return valid_files