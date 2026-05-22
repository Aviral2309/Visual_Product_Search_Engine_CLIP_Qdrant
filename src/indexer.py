"""
indexer.py

Offline indexing script:
- reads product images
- embeds them using CLIP
- stores vectors in Qdrant

Run:
uv run python src/indexer.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make src/ importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embedder import CLIPEmbedder
from src.store import VectorStore

# Image folder
IMAGES_DIR = Path("data/images")

# Batch size for Qdrant writes
BATCH_SIZE = 32


def extract_category(filename: str) -> str:
    """
    Extract category from filename.

    Example:
    0042_sneaker.png -> sneaker
    """

    stem = Path(filename).stem

    parts = stem.split("_", maxsplit=1)

    return parts[1] if len(parts) > 1 else "unknown"


def index_images() -> None:
    """
    Encode all images and store vectors in Qdrant.
    """

    image_paths = sorted(IMAGES_DIR.glob("*.png"))

    if not image_paths:

        print(f"❌ No images found in {IMAGES_DIR}/")
        print("Run: uv run python src/prepare_data.py")

        sys.exit(1)

    print(f"🖼️ Found {len(image_paths)} images to index")

    # Load CLIP
    embedder = CLIPEmbedder()

    # Connect to Qdrant
    store = VectorStore()

    # Skip if already indexed
    if store.count() >= len(image_paths):

        print(f"✅ Already indexed " f"{store.count()} images.")

        print("Delete data/qdrant_db/ " "to force re-indexing.")

        return

    # Batch containers
    batch_ids: list[int] = []
    batch_vectors = []
    batch_payloads: list[dict] = []

    total_indexed = 0

    for idx, image_path in enumerate(image_paths):

        # Encode image
        try:
            vector = embedder.embed_image(image_path)

        except Exception as e:

            print(f"⚠️ Skipping {image_path.name}: {e}")

            continue

        # Metadata payload
        payload = {
            "image_path": str(image_path),
            "filename": image_path.name,
            "category": extract_category(image_path.name),
        }

        batch_ids.append(idx)
        batch_vectors.append(vector)
        batch_payloads.append(payload)

        # Flush batch
        if len(batch_ids) == BATCH_SIZE:

            store.upsert_batch(
                batch_ids,
                batch_vectors,
                batch_payloads,
            )

            total_indexed += len(batch_ids)

            print(f"Indexed " f"{total_indexed}/" f"{len(image_paths)} images...")

            batch_ids.clear()
            batch_vectors.clear()
            batch_payloads.clear()

    # Final leftover batch
    if batch_ids:

        store.upsert_batch(
            batch_ids,
            batch_vectors,
            batch_payloads,
        )

        total_indexed += len(batch_ids)

    print(f"\n✅ Indexing complete! " f"{total_indexed} images stored in Qdrant.")


if __name__ == "__main__":
    index_images()
