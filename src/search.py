"""
search.py

Provides search_products():
the core text-to-image search function.

Used by:
- CLI testing
- FastAPI backend
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make src/ importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embedder import CLIPEmbedder
from src.store import VectorStore

# Shared singleton instances
_embedder: CLIPEmbedder | None = None
_store: VectorStore | None = None


def _get_embedder() -> CLIPEmbedder:
    """
    Return shared CLIP embedder instance.
    """

    global _embedder

    if _embedder is None:
        _embedder = CLIPEmbedder()

    return _embedder


def _get_store() -> VectorStore:
    """
    Return shared VectorStore instance.
    """

    global _store

    if _store is None:
        _store = VectorStore()

    return _store


def search_products(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Search product images using natural language.

    Args:
        query:
            Text query like "red sneakers"

        top_k:
            Number of results to return

    Returns:
        List of result dictionaries
    """

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    embedder = _get_embedder()
    store = _get_store()

    # Encode text query
    query_vector = embedder.embed_text(query)

    # Vector search in Qdrant
    raw_results = store.search(
        query_vector,
        top_k=top_k,
    )

    # Flatten payload structure
    return [
        {
            "id": r["id"],
            "score": r["score"],
            "image_path": r["payload"].get(
                "image_path",
                "",
            ),
            "filename": r["payload"].get(
                "filename",
                "",
            ),
            "category": r["payload"].get(
                "category",
                "unknown",
            ),
        }
        for r in raw_results
    ]


# CLI entrypoint
if __name__ == "__main__":

    query = sys.argv[1] if len(sys.argv) > 1 else "sneakers"

    print(f"\n🔍 Searching for: '{query}'\n")

    results = search_products(
        query,
        top_k=5,
    )

    for rank, r in enumerate(
        results,
        start=1,
    ):

        print(
            f"#{rank} "
            f"score={r['score']:.4f} "
            f"category={r['category']:<12} "
            f"file={r['filename']}"
        )
