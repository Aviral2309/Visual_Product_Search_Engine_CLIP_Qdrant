"""
prepare_data.py

Downloads Fashion MNIST from HuggingFace and saves 500 product images
to disk as PNG files, ready for CLIP indexing.

Run once before indexing:
uv run python src/prepare_data.py
"""

from pathlib import Path

from datasets import load_dataset
from PIL import Image

# Where to save the product images on disk
IMAGES_DIR = Path("data/images")

# How many images to save
NUM_IMAGES = 500

# Fixed seed for reproducibility
SEED = 42

# Label mapping for Fashion MNIST
LABEL_NAMES = [
    "tshirt",  # 0
    "trouser",  # 1
    "pullover",  # 2
    "dress",  # 3
    "coat",  # 4
    "sandal",  # 5
    "shirt",  # 6
    "sneaker",  # 7
    "bag",  # 8
    "ankle_boot",  # 9
]


def prepare_dataset() -> None:
    """
    Download Fashion MNIST and save resized images locally.
    """

    # Create image directory
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    print("📥 Downloading Fashion MNIST from HuggingFace...")

    # Load training split
    dataset = load_dataset("fashion_mnist", split="train")

    # Shuffle and select subset
    dataset = dataset.shuffle(seed=SEED).select(range(NUM_IMAGES))

    print(f"💾 Saving {NUM_IMAGES} images to {IMAGES_DIR}/ ...")

    for idx, item in enumerate(dataset):

        # Convert numeric label to text
        label_name = LABEL_NAMES[item["label"]]

        # Example filename: 0042_sneaker.png
        filename = f"{idx:04d}_{label_name}.png"

        filepath = IMAGES_DIR / filename

        # PIL image object
        img: Image.Image = item["image"]

        # Resize for CLIP compatibility
        img = img.resize((224, 224), Image.LANCZOS)

        # Convert grayscale → RGB
        img = img.convert("RGB")

        # Save image
        img.save(filepath)

    print(f"✅ Done! {NUM_IMAGES} images saved to {IMAGES_DIR}/")


if __name__ == "__main__":
    prepare_dataset()
