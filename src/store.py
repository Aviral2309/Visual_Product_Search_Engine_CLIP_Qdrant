"""
store.py

Manages a Qdrant vector collection for product image embeddings.

Uses local path mode:
data is persisted to disk between Python runs.

To switch to Qdrant Cloud later,
change exactly one line in __init__.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

# Collection name
COLLECTION_NAME = "products"

# CLIP embedding dimension
VECTOR_DIM = 512

# Cosine similarity
DISTANCE = Distance.COSINE

# Local database path
DB_PATH = "data/qdrant_db"


class VectorStore:
    """
    Wrapper around Qdrant vector database.
    """

    def __init__(self) -> None:

        # Local persistent Qdrant
        self.client = QdrantClient(path=DB_PATH)

        # Ensure collection exists
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """
        Create collection if it does not exist.
        """

        existing_names = [c.name for c in self.client.get_collections().collections]

        if COLLECTION_NAME not in existing_names:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_DIM,
                    distance=DISTANCE,
                ),
            )

            print(f"✅ Created Qdrant collection: '{COLLECTION_NAME}'")

        else:

            count = self.client.count(COLLECTION_NAME).count

            print(f"✅ Connected to '{COLLECTION_NAME}' " f"({count} vectors indexed)")

    def upsert_batch(
        self,
        ids: list[int],
        vectors: list[np.ndarray],
        payloads: list[dict[str, Any]],
    ) -> None:
        """
        Insert/update vectors in Qdrant.
        """

        points = [
            PointStruct(
                id=point_id,
                vector=vec.tolist(),
                payload=meta,
            )
            for point_id, vec, meta in zip(
                ids,
                vectors,
                payloads,
            )
        ]

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search most similar vectors.
        """

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector.tolist(),
            limit=top_k,
        ).points

        return [
            {
                "id": hit.id,
                "score": round(hit.score, 4),
                "payload": hit.payload,
            }
            for hit in results
        ]

    def count(self) -> int:
        """
        Return total vector count.
        """

        return self.client.count(COLLECTION_NAME).count
