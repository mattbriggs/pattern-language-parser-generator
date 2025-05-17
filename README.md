# Pattern Language Miner

The **Pattern Language Miner** is a modular Python application designed to extract, structure, and catalog recurring content patterns from Markdown, HTML, and plain text documents. It leverages NLP techniques and semantic clustering to build a structured knowledge base of reusable documentation patterns suitable for reuse, search, and AI optimization.

## Documentation

* [Instructions for Docker and Weaviate Integration](docs/instructions_for_docker.md)
* [Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool](docs/application-design.md)
* [Pattern Language Miner: How-To Manual](docs/application-guide.md)
* [Workflow](docs/workflow.md)
* [config.yml Reference and Usage Guide](docs/configuration-file-reference.md)
* [Troubleshooting](docs/troubleshooting.md)

> [NOTE!]
> Docs are in process and may have wrong parameters, order.

## ✨ Purpose

This tool automates the discovery of patterns based on lexical recurrence and semantic similarity using techniques drawn from:

* Christopher Alexander's *Pattern Language*
* Robert E. Horn's *Information Mapping*
* NLP-based frequency analysis and clustering

It supports output to structured YAML conforming to a custom JSON Schema, suitable for reuse in reference and training systems.
## 🧱 Architecture Overview

* **Parser Layer:** Modular, pluggable parsing for `.txt`, `.md`, and `.html`
* **Pattern Extractor:** Lexical pattern mining via NLTK
* **Semantic Clusterer:** Optional clustering via sentence-transformers
* **Output Engine:** Emits validated YAML files for each pattern
* **Vector Store Integration:** Optional integration with Weaviate for persistent search and semantic indexing
* **Command Line Interface:** Scriptable CLI interface for batch processing
## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/pattern-language-miner.git
cd pattern-language-miner
```

### 2. Create a virtual environment (macOS with VS Code)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Make sure your VS Code workspace uses `.venv` as the Python interpreter.

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```
## 📦 NLTK Setup

I've included a script to help get the resources you need. Also note that the NLTK is a previous version (3.7).

You can run:

```bash
python setup_resources.py
```

## 🧠 Optional: Weaviate (Vector Search)

The application integrates with a local Weaviate instance for semantic clustering.

### 1. Export your OpenAI API key (for text2vec)

```bash
export OPENAI_APIKEY=your-openai-key
```

### 2. Start Weaviate using Docker

```bash
docker compose -f docker-compose.yml up -d
```

Check availability: [http://localhost:8080/v1/.well-known/ready](http://localhost:8080/v1/.well-known/ready)
## 🚀 Running the Application

Use the CLI to analyze a directory of files:

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli \
--log-level DEBUG \
analyze \
  --input-dir ./sample_docs analyze\
  --output-dir ./patterns_output \
```
## 🧪 Running Tests

```bash
PYTHONPATH=src pytest
```
## 🛠 Maintenance

* Use `requirements.txt` for consistent dependency versions.
* Clear `weaviate_data/` volume if you need to reset Weaviate.
* New document types can be added by implementing a new `BaseParser`.
## 📁 Project Structure

```

docs/                    # Insructions and notes on how to use this tool
logs/                    # Location of the log files when debugging
src/pattern_language_miner/
├── parser/              # File parsers for text, HTML, markdown
├── extractor/           # Lexical and semantic pattern extractors
├── output/              # YAML and assembly writer
├── vector_store/        # Weaviate vector store client
├── utils/               # Logging and progress tools
├── cli.py               # CLI entry point
├── schema/              # JSON schema for pattern validation
tests/                   # Unit + integration tests
docker-compose.yml       # Weaviate container config
requirements.txt         # Script dependencies
setup_resources.py       # Script to install NLTK resources
```
## 📄 License

MIT License. © Final State Press 2025