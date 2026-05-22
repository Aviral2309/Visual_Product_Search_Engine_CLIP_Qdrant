````md
# 🔍 Visual Product Search Engine

A multimodal AI-powered semantic image search engine built using:

- OpenAI CLIP
- Qdrant Vector Database
- FastAPI
- React + TailwindCSS

Search product images using natural language queries like:

- "black sneakers"
- "white shirt"
- "blue dress"

instead of traditional keyword matching.

---

# 🚀 Features

- Semantic text-to-image search
- CLIP embeddings for multimodal retrieval
- Qdrant vector database integration
- FastAPI backend API
- Interactive React frontend
- Persistent local vector storage

---

# 🧠 Architecture

```text
Text Query
   ↓
CLIP Text Encoder
   ↓
512-dim Embedding
   ↓
Qdrant Vector Search
   ↓
Matching Product Images
````

---

# ⚙️ Tech Stack

## Backend

* FastAPI
* PyTorch
* Transformers
* Qdrant

## Frontend

* React
* TailwindCSS
* Framer Motion

## AI/ML

* OpenAI CLIP
* Vector Embeddings
* Semantic Search

---

# 📦 Setup

## Backend

```bash
uv venv --python 3.11
.venv\Scripts\activate

uv add fastapi uvicorn torch transformers==4.41.2 datasets==2.19.1 huggingface_hub==0.23.2 pillow numpy qdrant-client
```

Prepare dataset:

```bash
uv run python src/prepare_data.py
```

Index images:

```bash
uv run python src/indexer.py
```

Run API:

```bash
uv run uvicorn main:app --port 8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://127.0.0.1:8000
```

---

# 🔎 API Endpoints

## Health Check

```text
GET /health
```

## Semantic Search

```text
GET /search?q=black+sneakers
```

---

# 🎯 Resume Highlights

* Built multimodal semantic search engine using CLIP + Qdrant
* Implemented vector embedding retrieval pipeline
* Developed FastAPI backend with semantic retrieval
* Created responsive React frontend for AI-powered product search

---

# 👨‍💻 Author

### Aviral Mittal

AI / ML / GenAI Enthusiast

```
```
