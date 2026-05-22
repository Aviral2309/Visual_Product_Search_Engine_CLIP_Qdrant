"""
embedder.py

Wraps the CLIP model with two methods:

- embed_image(path) → 512-dim vector from an image file
- embed_text(query) → 512-dim vector from a text string

Both vectors live in the same mathematical space,
which enables text-to-image similarity search.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

# CLIP model identifier
MODEL_ID = "openai/clip-vit-base-patch32"


class CLIPEmbedder:
    """
    Loads CLIP once and exposes embed_image / embed_text methods.

    Reuse a single instance.
    Loading CLIP repeatedly is expensive.
    """

    def __init__(self) -> None:

        # GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"🔧 Loading CLIP on: {self.device}")

        # Preprocessing pipeline
        self.processor = CLIPProcessor.from_pretrained(MODEL_ID)

        # Model
        self.model = CLIPModel.from_pretrained(MODEL_ID).to(self.device)

        # Inference mode
        self.model.eval()

        print("✅ CLIP model ready.")

    def embed_image(self, image_path: str | Path) -> np.ndarray:
        """
        Encode image into 512-dim normalized embedding.
        """

        # Load image
        image = Image.open(image_path).convert("RGB")

        # Preprocess
        inputs = self.processor(images=image, return_tensors="pt")

        # Move tensors to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Inference
        with torch.no_grad():

            raw = self.model.get_image_features(**inputs)

            # Compatibility handling
            if hasattr(raw, "pooler_output"):
                features = raw.pooler_output

            elif hasattr(raw, "image_embeds"):
                features = raw.image_embeds

            else:
                features = raw

        # Normalize embeddings
        features = features / features.norm(dim=-1, keepdim=True)

        return features.squeeze().cpu().numpy()

    def embed_text(self, query: str) -> np.ndarray:
        """
        Encode text into 512-dim normalized embedding.
        """

        # Tokenize text
        inputs = self.processor(
            text=[query], return_tensors="pt", padding=True, truncation=True
        )

        # Move tensors to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Inference
        with torch.no_grad():

            raw = self.model.get_text_features(**inputs)

            # Compatibility handling
            if hasattr(raw, "pooler_output"):
                features = raw.pooler_output

            elif hasattr(raw, "text_embeds"):
                features = raw.text_embeds

            else:
                features = raw

        # Normalize embeddings
        features = features / features.norm(dim=-1, keepdim=True)

        return features.squeeze().cpu().numpy()
