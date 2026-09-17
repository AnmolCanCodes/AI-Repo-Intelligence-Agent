from pathlib import Path
from urllib.parse import urlparse

import shutil
import tempfile

from typing import Tuple

from git import Repo, GitCommandError

from app.config.settings import settings


class GitHubIngestion:
    """Handles cloning GitHub repositories locally."""

    def __init__(self):
        self.github_token = settings.github_token_str
        self.base_temp_dir = Path(settings.TEMP_CLONE_DIR)

        # Ensure the temporary clone directory exists
        self.base_temp_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def extract_repo_name(self, repo_url: str) -> str:
        """
        Extracts a safe repository identifier from a GitHub URL.

        Example:
            https://github.com/owner/my-repo.git
            -> owner_my-repo
        """

        parsed = urlparse(repo_url.strip())

        if parsed.scheme not in {"http", "https"}:
            raise ValueError(
                "Only HTTP/HTTPS GitHub URLs are supported."
            )

        if parsed.netloc.lower() != "github.com":
            raise ValueError(
                "Only github.com repositories are supported."
            )

        parts = [
            part for part in parsed.path.strip("/").split("/")
            if part
        ]

        if len(parts) != 2:
            raise ValueError(
                "Expected a GitHub URL in the format "
                "https://github.com/owner/repository"
            )

        owner, repo = parts
        repo = repo.removesuffix(".git")

        if not owner or not repo:
            raise ValueError("Invalid GitHub repository URL.")

        return f"{owner}_{repo}"

    def clone_repository(self, repo_url: str) -> Tuple[str, str]:
        """
        Clones a GitHub repository into a temporary directory.

        Returns:
            Tuple[str, str]:
                (local_repo_path, repo_identifier)
        """

        repo_name = self.extract_repo_name(repo_url)

        target_dir = Path(
            tempfile.mkdtemp(
                prefix=f"{repo_name}_",
                dir=str(self.base_temp_dir)
            )
        )

        # Clean the input URL up front
        clean_url = repo_url.strip()

        # Safely inject the authentication token into the URL scheme if present
        if self.github_token:
            if clean_url.startswith("https://"):
                clean_url = clean_url.replace("https://", f"https://{self.github_token}@")
            elif clean_url.startswith("http://"):
                clean_url = clean_url.replace("http://", f"http://{self.github_token}@")

        clone_kwargs = {
            "url": clean_url,
            "to_path": str(target_dir),
            "depth": 1,
        }

        try:
            print(
                f"Cloning repository: {repo_url} "
                f"into {target_dir}..."
            )

            Repo.clone_from(**clone_kwargs)

            print(
                f"Successfully cloned: {repo_name}"
            )

            return str(target_dir), repo_name

        except GitCommandError as e:
            shutil.rmtree(
                target_dir,
                ignore_errors=True
            )

            raise RuntimeError(
                f"Failed to clone repository "
                f"'{repo_url}': {e.stderr or str(e)}"
            ) from e

    @staticmethod
    def cleanup(repo_path: str) -> None:
        """Removes the local cloned repository."""

        path = Path(repo_path)

        if path.exists():
            shutil.rmtree(path)

            print(
                f"Cleaned up temporary repo directory: {path}"
            )
