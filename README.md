# Pattern Language Miner

A modular Python tool that automatically extracts, enriches, clusters, and exports reusable content patterns from Markdown, HTML, and plain-text document corpora.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Purpose

Pattern Language Miner enables a corpus-driven approach to pattern discovery and synthesis. It automates the creation of reusable content units by identifying patterns based on:

- **Lexical Recurrence** — frequent phrasing detected via configurable n-gram analysis
- **Semantic Similarity** — conceptual proximity measured with sentence embeddings
- **Information Typing** — procedural, conceptual, reference content classification
- **Generative Output** — natural-language sentence synthesis from structured YAML

Inspired by Christopher Alexander's *A Pattern Language* and Robert E. Horn's *Information Mapping*.

---

## Capabilities

| Capability | Description |
|---|---|
| **Extract** | Identify frequent lexical patterns using configurable n-gram and POS filters |
| **Enrich** | Automatically infer metadata (title, summary, keywords, problem) |
| **Cluster** | Group similar patterns using vector embeddings, KMeans, and UMAP |
| **Generate** | Convert structured YAML into human-readable sentences or HTML |
| **Export** | Produce knowledge graphs (Mermaid, GraphML, Neo4j Cypher, JSON) |

---

## Quick Start

```bash
# Install
git clone https://github.com/your-org/pattern-language-miner.git
cd pattern-language-miner
python -m venv ENV && source ENV/bin/activate
pip install -e ".[dev]"
python setup_resources.py

# Run the pipeline
pattern-miner analyze    --config config.yaml --input-dir ./docs --output-dir ./raw
pattern-miner enrich     --input-dir ./raw    --output-dir ./enriched
pattern-miner cluster    --input-dir ./enriched --output-dir ./clusters
pattern-miner generate-sentences --input-dir ./enriched --output-path ./output.md --format markdown
pattern-miner export-graph --input-json ./clusters/clustered_patterns.json --output-path ./graph.mmd --format mermaid
```

---

## Pipeline Overview

```
Raw Documents (txt / md / html)
    ↓  [Parser Factory]
    ↓  [Pattern Extractor]  — NLTK n-grams
Raw Patterns (YAML)
    ↓  [Pattern Enricher]   — title · summary · keywords · problem
Enriched Patterns (YAML)
    ├→  [Pattern Clusterer]  — SentenceTransformer · KMeans · UMAP
    ├→  [Sentence Generator] — text / Markdown / HTML
    └→  [Graph Exporter]     — GraphML · Mermaid · Neo4j · JSON
```

---

## Project Structure

```
src/pattern_language_miner/
├── cli.py               # Click CLI entry-point
├── walker.py            # Directory walker + parser factory
├── parser/              # BaseParser + Text/Markdown/HTML implementations
├── extractor/           # N-gram extraction + semantic sentence clustering
├── enricher/            # Metadata inference
├── cluster/             # KMeans + UMAP semantic clustering
├── generator/           # Natural-language sentence generation
├── graph/               # Knowledge-graph export
├── writer/              # YAML file writer
├── vector_store/        # Weaviate adapter (optional)
├── pipeline/            # Pipeline orchestrator + event bus
├── patterns/            # Core Pattern data class
├── utils/               # Config validation, logging, progress
└── schema/              # JSON Schema files
```

---

## Documentation

Full documentation is available at the project docs site (served via `mkdocs serve`):

```bash
pip install -e ".[docs]"
mkdocs serve
```

Documentation includes:

- **User Guide** — installation, quick start, commands, configuration, workflows, troubleshooting
- **Reference** — CLI reference, configuration reference, Docker/Weaviate guide
- **Design** — architecture diagrams, design patterns catalogue
- **SRS** — Software Requirements Specification with full UML diagrams
- **Changelog** and **Roadmap**

---

## Development

```bash
# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src/pattern_language_miner --cov-report=term-missing

# Lint
ruff check src/ tests/

# Format
black src/ tests/
isort src/ tests/
```

---

## License

MIT License — see [LICENSE](LICENSE).
