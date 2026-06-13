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


def _env_float(key: str, default: float) -> float:
    raw = os.environ.get(key)
    return float(raw) if raw else default


def _env_int(key: str, default: int) -> int:
    raw = os.environ.get(key)
    return int(raw) if raw else default


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

    # Evidence-gate thresholds (Step 5). They operate in the [0,1] normalized
    # score space defined in src/retrieval/gate.py. Calibrated 2026-06-13 on
    # the 42-question bank (30 answerable + 12 out-of-scope), hybrid backend,
    # tspec_md corpus. Descriptive, NOT statistically powered — retune when
    # the corpus/index or gate backend changes. Calibration finding: on a
    # §6.2/6.3-only index the RRF top score saturates (~0.9+ for most queries,
    # dipping to ~0.5 only for the most foreign hard-OOS), so it barely
    # discriminates in- vs out-of-scope; term coverage
    # is the load-bearing signal — hence the coverage-dominant weights. The
    # answer_floor sits in a THIN gap (~0.03) above the weakest answerable
    # question, so these floors are sensitive; see research notes.
    gate_min_results: int = _env_int("GATE_MIN_RESULTS", 2)
    gate_min_top_score: float = _env_float("GATE_MIN_TOP_SCORE", 0.20)
    gate_strong_score: float = _env_float("GATE_STRONG_SCORE", 0.55)
    gate_answer_floor: float = _env_float("GATE_ANSWER_FLOOR", 0.65)
    gate_low_floor: float = _env_float("GATE_LOW_FLOOR", 0.50)
    gate_w_score: float = _env_float("GATE_W_SCORE", 0.2)
    gate_w_consist: float = _env_float("GATE_W_CONSIST", 0.2)
    gate_w_cover: float = _env_float("GATE_W_COVER", 0.6)
    gate_mode: str = os.environ.get("GATE_MODE", "balanced")

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path.as_posix()}"


settings = Settings()
