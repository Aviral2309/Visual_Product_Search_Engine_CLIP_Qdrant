"""
main.py

FastAPI server for the Visual Product Search Engine.

Run:
uv run uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from src.search import (
    _get_embedder,
    _get_store,
    search_products,
)

# =========================
# Response Models
# =========================


class SearchResult(BaseModel):
    """
    One matching product.
    """

    id: int

    score: float = Field(
        ...,
        description=("Cosine similarity score " "(0.0 to 1.0)."),
    )

    image_path: str
    filename: str
    category: str


class SearchResponse(BaseModel):
    """
    Full search response.
    """

    query: str
    top_k: int
    results: list[SearchResult]
    total_indexed: int


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str
    total_indexed: int
    model: str


# =========================
# Lifespan Events
# =========================


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Starting server...")

    print("🔧 Loading CLIP model...")

    _get_embedder()

    print("🗂️ Connecting to Qdrant...")

    _get_store()

    print("✅ Server ready.")

    yield

    print("🛑 Server shutdown.")


# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="Visual Product Search API",
    description=("Semantic image search using " "CLIP embeddings + Qdrant."),
    version="1.0.0",
    lifespan=lifespan,
)


# =========================
# Health Endpoint
# =========================


@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    """

    store = _get_store()

    return HealthResponse(
        status="ok",
        total_indexed=store.count(),
        model="openai/clip-vit-base-patch32",
    )


# =========================
# Search Endpoint
# =========================


@app.get(
    "/search",
    response_model=SearchResponse,
)
async def search(
    q: Annotated[
        str,
        Query(description=("Natural language query " "like 'red sneakers'")),
    ],
    top_k: Annotated[
        int,
        Query(
            ge=1,
            le=20,
            description="Number of results",
        ),
    ] = 5,
) -> SearchResponse:
    """
    Search products using text.
    """

    if not q.strip():

        raise HTTPException(
            status_code=400,
            detail=("Query parameter " "'q' cannot be empty."),
        )

    try:

        results = search_products(
            q,
            top_k=top_k,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    store = _get_store()

    return SearchResponse(
        query=q,
        top_k=top_k,
        results=[SearchResult(**r) for r in results],
        total_indexed=store.count(),
    )
