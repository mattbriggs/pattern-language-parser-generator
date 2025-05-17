# Pattern Language Miner

The **Pattern Language Miner** is a modular Python application designed to extract, structure, and catalog recurring content patterns from Markdown, HTML, and plain text documents. It leverages NLP techniques and semantic clustering to build a structured knowledge base of reusable documentation patterns suitable for reuse, search, and AI optimization.

## Purpose of the Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool

This tool automates the discovery of patterns based on lexical recurrence and semantic similarity using techniques drawn from:

* Christopher Alexander's *Pattern Language*
* Robert E. Horn's *Information Mapping*
* Natural Language Process NLP-based frequency analysis and clustering

It supports output to structured YAML conforming to a custom JSON Schema, suitable for reuse in reference and training systems.

## Documentation

* [Set up and installation of the Pattern Language Miner](docs/set-up-and-installation.md)
* [Instructions for Docker and Weaviate Integration](docs/instructions_for_docker.md)
* [Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool](docs/application-design.md)
* [Pattern Language Miner: How-To Manual](docs/application-guide.md)
* [Workflow](docs/workflow.md)
* [config.yml Reference and Usage Guide](docs/configuration-file-reference.md)
* [Troubleshooting](docs/troubleshooting.md)

## 🧱 Architecture Overview

Pattern Language Miner is a modular tool for extracting patterns from text, markdown, and HTML files. It uses NLTK for pattern mining and sentence-transformers for clustering, emitting validated YAML files.

* **Parser Layer:** Modular, pluggable parsing for `.txt`, `.md`, and `.html`
* **Pattern Extractor:** Lexical pattern mining via NLTK
* **Semantic Clusterer:** Optional clustering via sentence-transformers
* **Output Engine:** Emits validated YAML files for each pattern
* **Vector Store Integration:** Optional integration with Weaviate for persistent search and semantic indexing
* **Command Line Interface:** Scriptable CLI interface for batch processing

You can read more about the design of the tool at [Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool](docs/application-design.md).

## 📄 License

MIT License