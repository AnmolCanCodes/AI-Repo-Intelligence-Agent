
import os

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Configuration
    HF_TOKEN: SecretStr | None = Field(default=None,description="Hugging Face API token")

    HF_MODEL: str = Field(default="zai-org/GLM-5.3",description="Hugging Face model repository ID")

    GITHUB_TOKEN: SecretStr | None = Field(default=None,description="GitHub Personal Access Token")

    # Storage Paths
    VECTORSTORE_DIRECTORY: str = Field(
        default="data/vectorstore",
        description="Directory for vector store persistence"
    )

    TEMP_CLONE_DIR: str = Field(
        default="data/temp_repos",
        description="Directory for temporary repository clones"
    )

    # Chunking Configuration
    CHUNK_SIZE: int = Field(default=1000,description="Code chunk size for embeddings")

    CHUNK_OVERLAP: int = Field(default=150,description="Overlap between code chunks")

    # File Ingestion Configuration
    ALLOWED_EXTENSIONS: set[str] = Field(
        default_factory=lambda: {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".json",
            ".yaml",
            ".yml",
            ".md",
        },
        description="File extensions allowed for ingestion"
    )

    IGNORED_DIRS: set[str] = Field(
        default_factory=lambda: {
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "venv",
            "dist",
            "build",
            ".idea",
            ".vscode",
        },
        description="Directories ignored during repository scanning"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @staticmethod
    def _read_env_secret(*names: str) -> str:
        for name in names:
            value = os.getenv(name)
            if value is not None:
                cleaned = value.strip().strip('"').strip("'")
                if cleaned:
                    return cleaned
        return ""

    @property
    def hf_token_str(self) -> str:
        direct = self._read_env_secret("HF_TOKEN", "HF_TOEKN")
        if direct:
            return direct
        return (
            self.HF_TOKEN.get_secret_value()
            if self.HF_TOKEN
            else ""
        )

    @property
    def github_token_str(self) -> str:
        direct = self._read_env_secret("GITHUB_TOKEN")
        if direct:
            return direct
        return (
            self.GITHUB_TOKEN.get_secret_value()
            if self.GITHUB_TOKEN
            else ""
        )


settings = Settings()