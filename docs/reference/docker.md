# Docker & Weaviate Integration

Weaviate is an optional vector-database backend that enables semantic similarity search over your pattern library. It is **not required** for the core extraction, enrichment, clustering, or graph-export workflows.

---

## Requirements

- [Docker](https://www.docker.com/) installed and running
- An [OpenAI API key](https://platform.openai.com/account/api-keys) (for the `text2vec-openai` module)

---

## Setup

### 1. Set Your OpenAI API Key

```bash
export OPENAI_APIKEY=your-key-here
```

Add this to your shell profile (`~/.zshrc`, `~/.bash_profile`) to persist it across sessions.

### 2. Start Weaviate

From the project root directory:

```bash
docker compose up -d
```

This launches Weaviate on port `8080` with a persistent `weaviate_data` volume.

### 3. Verify Weaviate is Running

```bash
curl http://localhost:8080/v1/.well-known/ready
# Expected: {"status":"READY"}
```

---

## Maintenance Commands

| Action | Command |
|---|---|
| Start | `docker compose up -d` |
| Stop (keep data) | `docker compose down` |
| Stop + delete all data | `docker compose down -v` |
| View logs | `docker compose logs -f` |
| Restart clean | `docker compose down -v && docker compose up -d` |

---

## Volume Management

```bash
docker volume ls                     # List all volumes
docker volume inspect weaviate_data  # Inspect the Weaviate volume
docker volume rm weaviate_data       # Remove (after docker compose down)
```

---

## Using WeaviateStore in Code

```python
from pattern_language_miner.vector_store.weaviate_store import WeaviateStore

store = WeaviateStore(url="http://localhost:8080", class_name="Pattern")

# Index a pattern
store.upsert_pattern({
    "id": "P-001",
    "name": "Install Package",
    "context": "software setup",
    "solution": "apt-get install <package>",
})

# Semantic search
results = store.query_similar_patterns("how to install software", top_k=5)

# Delete by ID
store.delete_pattern("P-001")
```

---

## Notes

- Port `8080` must not be in use by another service.
- Restart Weaviate if you change your `OPENAI_APIKEY`.
- Weaviate uses the `text2vec-openai` module — each indexing request calls the OpenAI Embeddings API and incurs usage costs.
