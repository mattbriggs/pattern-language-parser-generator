# Instructions for Docker and Weaviate Integration

This guide provides comprehensive instructions for managing the lifecycle of a local **Weaviate** instance using Docker, specifically for use with the Pattern Language Miner application.
## 🚀 Overview

Weaviate is a vector database that allows fast semantic search and retrieval. In this application, it supports:

* Storing structured pattern data
* Performing similarity queries using OpenAI embeddings

You'll run Weaviate locally using Docker with optional persistence and access control.
## 🔧 Requirements

* [Docker](https://www.docker.com/) installed and running
* Internet access to download Docker images
* Your [OpenAI API key](https://platform.openai.com/account/api-keys) if using the `text2vec-openai` module
## 📦 Setup

### 1. Set Your OpenAI API Key

Export your API key to your shell environment:

```bash
export OPENAI_APIKEY=your-key-here
```

> **Note**: You can store this in your `.zshrc` or `.bash_profile` for reuse.

### 2. Start Weaviate with Docker Compose

Run the following in the root directory of the project:

```bash
docker compose up -d
```

This uses the included `docker-compose.yml` file to:

* Launch Weaviate
* Enable the OpenAI vector module
* Persist data in a Docker volume (`weaviate_data`)
## ✅ Verifying Weaviate is Running

Visit:

```
http://localhost:8080/v1/.well-known/ready
```

You should see a JSON `{ "status": "READY" }` if the container is running properly.
## 🧪 Interacting With Weaviate

### Inspect Logs

```bash
docker compose logs -f
```

### Enter Container Shell (optional)

```bash
docker exec -it $(docker ps -qf "ancestor=cr.weaviate.io/semitechnologies/weaviate:1.30.2") /bin/sh
```
## 🧹 Maintenance

### Stop Weaviate

```bash
docker compose down
```

This stops the container but retains the volume.

### Remove All Data

```bash
docker compose down -v
```

This stops the container and deletes all indexed pattern data.

### Restart Clean Instance

```bash
docker compose down -v
docker compose up -d
```
## 🧱 Persistent Volume

The Docker Compose file mounts a named volume:

```yaml
volumes:
  - weaviate_data:/var/lib/weaviate
```

To manually inspect or remove it:

```bash
docker volume ls
docker volume inspect weaviate_data
docker volume rm weaviate_data
```
## 📂 Where Weaviate Fits in the App

* The `WeaviateStore` class (in `vector_store/weaviate_store.py`) connects to `http://localhost:8080`
* Patterns are indexed using their `id`, `context`, `solution`, and `name` fields
* Similarity queries can be performed via `query_similar_patterns()`
## 📄 Helpful References

* [Weaviate Docs](https://weaviate.io/developers/weaviate)
* [Docker Compose Reference](https://docs.docker.com/compose/)
* [OpenAI Embedding API](https://platform.openai.com/docs/guides/embeddings)
## 🧑‍💻 Typical Workflow

```bash
# Start Weaviate
docker compose up -d

# Run your CLI tool to ingest patterns
python -m pattern_language_miner.cli analyze --input-dir data --output-dir output

# Query Weaviate through WeaviateStore class or REST API
```
## 🏁 Final Notes

* You must restart Weaviate if your OpenAI key changes.
* Make sure port 8080 is not in use by another service.

