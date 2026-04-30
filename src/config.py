"""Project-wide settings, loaded from environment + .env.

Paths are anchored at the repo root so this works regardless of where
scripts are invoked from. All path overrides come from env vars (or .env)
so the project is portable across machines without code changes — see the
plan's "cross-machine portability" section.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Repo root = src/ -> parent twice
REPO_ROOT = Path(__file__).resolve().parent.parent

# Load .env from repo root if present (gitignored, holds API tokens etc.)
load_dotenv(REPO_ROOT / ".env")


def _env_path(key: str, default: Path) -> Path:
    raw = os.environ.get(key)
    return Path(raw).expanduser().resolve() if raw else default


@dataclass(frozen=True)
class Settings:
    repo_root: Path = REPO_ROOT
    data_dir: Path = _env_path("DATA_DIR", REPO_ROOT / "data")
    raw_dir: Path = _env_path("RAW_DIR", REPO_ROOT / "data" / "raw")
    db_path: Path = _env_path("DB_PATH", REPO_ROOT / "data" / "db" / "metadata.sqlite")
    chroma_path: Path = _env_path("CHROMA_PATH", REPO_ROOT / "data" / "db" / "chroma")
    eval_dir: Path = _env_path("EVAL_DIR", REPO_ROOT / "data" / "eval")

    # Defaults that may move into Provider abstraction in Week 2
    default_visibility: str = os.environ.get("DEFAULT_VISIBILITY", "private")

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path.as_posix()}"


settings = Settings()
