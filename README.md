# Pattern Language Miner

The **Pattern Language Miner** is a modular Python application designed to **extract**, **structure**, **generate**, and **catalog** recurring content patterns from Markdown, HTML, and plain text documents. It applies NLP techniques and semantic clustering to build a reusable and machine-readable knowledge base that supports documentation reuse, authoring automation, and AI optimization.

## Purpose

The Pattern Language Miner enables a corpus-driven approach to pattern discovery and synthesis. It automates the creation of reusable content units by identifying patterns based on:

- **Lexical Recurrence** (frequent phrasing)
- **Semantic Similarity** (conceptual proximity)
- **Information Typing** (procedural, conceptual, reference, etc.)
- **Generative Output** (natural language summaries)

It is inspired by:

- Christopher Alexander's *Pattern Language*
- Robert E. Horn's *Information Mapping*
- NLP and discourse modeling practices

## Capabilities

| Capability   | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Extract      | Identify frequent lexical patterns using configurable n-gram and POS filters |
| Enrich       | Automatically infer metadata (title, summary, keywords, problem)             |
| Cluster      | Group similar patterns using vector embeddings and clustering                |
| Generate     | Convert structured YAML into human-readable sentences or HTML                |
| Export       | Produce graph views (Mermaid, GraphML, Neo4j Cypher)                         |

## Key Use Cases

- Build a structured pattern library from documentation
- Prepare reusable training or reference content
- Analyze phrasing across a content corpus
- Generate summaries for publication, training, or onboarding
- Feed AI systems (e.g., RAG or LLM-based copilots) with structured patterns

## Documentation

- [Set up and installation of the Pattern Language Miner](docs/set-up-and-installation.md)
- [Configuration File Reference (`config.yml`)](docs/configuration-file-reference.md)
- [How-To Manual](docs/application-guide.md)
- [Corpus-Driven Design Overview](docs/application-design.md)
- [Workflow](docs/workflow.md)
- [Docker and Weaviate Integration](docs/instructions_for_docker.md)
- [Troubleshooting](docs/troubleshooting.md)

## Architecture Overview

Pattern Language Miner follows a modular architecture:

- **Parser Layer** - Supports `.txt`, `.md`, and `.html` files
- **Pattern Extractor** - Uses NLTK for lexical pattern detection
- **Semantic Clusterer** - Embeds patterns with sentence-transformers and clusters using UMAP and KMeans
- **Enricher** - Adds normalized metadata fields like title, problem, and keywords
- **Sentence Generator** - Converts YAML into publishable content
- **Graph Exporter** - Builds graph views in Mermaid, GraphML, or Neo4j Cypher formats
- **CLI Interface** - Provides subcommands for each functional module
- **Weaviate Integration (optional)** - Enables persistent semantic search over patterns

Read more in the [Corpus-Driven Pattern Extraction and Generation Tool](docs/application-design.md).

## License

This project is licensed under the [MIT License](LICENSE).