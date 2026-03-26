# Installation

## Requirements

- Python **3.10** or later
- pip
- (Optional) Docker — for the Weaviate semantic search backend

---

## Install from Source

```bash
# 1. Clone the repository
git clone https://github.com/your-org/pattern-language-miner.git
cd pattern-language-miner

# 2. Create a virtual environment
python -m venv ENV
source ENV/bin/activate          # macOS / Linux
# ENV\Scripts\activate           # Windows

# 3. Install the package with all dependencies
pip install -e ".[dev]"

# 4. Download required NLTK resources
python setup_resources.py
```

---

## Verify the Installation

```bash
pattern-miner --help
```

You should see the top-level help text listing all available commands.

---

## Optional: Weaviate (Semantic Search)

If you want to use the vector-search features, start Weaviate via Docker Compose:

```bash
docker compose up -d
```

See [Docker & Weaviate](../reference/docker.md) for full setup instructions.

---

## Upgrade

```bash
pip install --upgrade -e "."
```

---

## Dependencies Overview

| Package | Purpose |
|---|---|
| `click` | CLI framework |
| `nltk` | Tokenisation and n-gram extraction |
| `sentence-transformers` | Semantic embedding for clustering |
| `scikit-learn` | KMeans clustering |
| `umap-learn` | Dimensionality reduction for visualisation |
| `networkx` | Graph construction and export |
| `PyYAML` | Pattern serialisation |
| `beautifulsoup4` | HTML parsing |
| `weaviate-client` | Optional vector-store integration |
