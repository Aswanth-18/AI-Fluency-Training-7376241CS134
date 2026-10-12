"""Shared configuration and constructors for the assessment project."""

from __future__ import annotations

import hashlib
import math
import os
import re
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
CHROMA_DIR = PROJECT_DIR / "chroma_db"
COLLECTION_NAME = "student_handbook"

load_dotenv(PROJECT_DIR / ".env", override=False)

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()
MODEL = os.getenv("MODEL", "qwen2.5:1.5b").strip()
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "ollama").strip().lower()
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text").strip()
DEFAULT_MAX_DISTANCE = 0.75


class HashEmbeddings:
    """Deterministic, offline feature-hash embeddings for demos and tests.

    These embeddings require no model download, but are much less semantically
    capable than Ollama or FastEmbed. Select them with EMBED_PROVIDER=hash.
    """

    def __init__(self, dimensions: int = 384) -> None:
        self.dimensions = dimensions

    def _embed(self, text: str) -> list[float]:
        words = re.findall(r"\w+", text.lower())
        features = words + [f"{left}_{right}" for left, right in zip(words, words[1:])]
        vector = [0.0] * self.dimensions
        for feature in features:
            digest = hashlib.sha256(feature.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]
        return vector

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


def _missing_dependency(package: str, purpose: str, error: ImportError) -> RuntimeError:
    return RuntimeError(
        f"{package} is required for {purpose}. Activate this project's virtual "
        "environment and run: pip install -r requirements.txt"
    )


def get_llm():
    """Create the configured Ollama or Groq-compatible chat model."""
    if PROVIDER == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as error:
            raise _missing_dependency("langchain-ollama", "the Ollama chat model", error) from error
        return ChatOllama(model=MODEL, temperature=0)

    if PROVIDER in {"groq", "openai_compatible"}:
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is empty. Set it in this project's .env file "
                "without committing that file."
            )
        base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1").strip()
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as error:
            raise _missing_dependency("langchain-openai", "the Groq-compatible chat model", error) from error
        return ChatOpenAI(
            model=MODEL,
            api_key=api_key,
            base_url=base_url,
            temperature=0,
        )

    raise RuntimeError(
        f"Unsupported PROVIDER={PROVIDER!r}. Choose 'ollama' or 'groq' in .env."
    )


def get_embeddings():
    """Create the configured Ollama, FastEmbed, or offline hash embedder."""
    if EMBED_PROVIDER == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError as error:
            raise _missing_dependency("langchain-ollama", "Ollama embeddings", error) from error
        return OllamaEmbeddings(model=EMBED_MODEL)

    if EMBED_PROVIDER == "fastembed":
        try:
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        except ImportError as error:
            raise _missing_dependency("langchain-community and fastembed", "FastEmbed", error) from error
        return FastEmbedEmbeddings(model_name=EMBED_MODEL)

    if EMBED_PROVIDER == "hash":
        return HashEmbeddings()

    raise RuntimeError(
        f"Unsupported EMBED_PROVIDER={EMBED_PROVIDER!r}. Choose 'ollama', "
        "'fastembed', or 'hash' in .env."
    )


def get_vector_store(*, require_existing: bool = False):
    """Open the project's persistent Chroma collection."""
    if require_existing and (
        not CHROMA_DIR.is_dir() or not any(CHROMA_DIR.iterdir())
    ):
        raise RuntimeError(
            f"No Chroma database was found at {CHROMA_DIR}. Run "
            "'python 1_ingest.py' first."
        )
    try:
        from langchain_chroma import Chroma
    except ImportError as error:
        raise _missing_dependency("langchain-chroma", "the Chroma vector store", error) from error

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},
    )


def get_max_distance() -> float:
    """Return the configured cosine-distance cutoff, or a clear config error."""
    raw_value = os.getenv("MAX_DISTANCE", str(DEFAULT_MAX_DISTANCE))
    try:
        value = float(raw_value)
    except ValueError as error:
        raise RuntimeError(f"MAX_DISTANCE must be a number, not {raw_value!r}.") from error
    if not math.isfinite(value) or not 0 <= value <= 2:
        raise RuntimeError("MAX_DISTANCE must be between 0 and 2 for cosine distance.")
    return value
