# Changelog

All notable changes to Pattern Language Miner are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2024-03-01

### Added

- **`pyproject.toml`** — modern PEP 517/518 build configuration with `setuptools`, tool config for `pytest`, `black`, `isort`, `ruff`, `mypy`, and `coverage`
- **`pattern-miner` entry-point** — installed script calling `pattern_language_miner.cli:cli`
- **Pipeline package** — `pipeline/pipeline.py` and `pipeline/events.py` implement the Chain-of-Responsibility and Observer patterns for composable, event-driven pipeline orchestration
- **`--n-clusters` option** on the `cluster` command — allows configuring KMeans cluster count from the CLI
- **`test_walker.py`** — unit tests for `DirectoryWalker` and `ParserFactory`
- **`test_pipeline.py`** — unit tests for `Pipeline`, `PipelineStep`, and `EventBus`
- **`conftest.py`** — shared pytest fixtures for config files and sample YAML patterns
- **MkDocs with Material theme** — full documentation site with mermaid.js diagram support
- **Software Requirements Specification** (`docs/srs.md`) — includes use cases, functional/non-functional requirements, and full UML diagrams (class, sequence, state, component)
- **Changelog** (`docs/changelog.md`) and **Roadmap** (`docs/roadmap.md`)
- **User Guide** section in docs: Getting Started, Installation, Quick Start, Commands, Configuration, Workflows, Troubleshooting
- Sphinx-compatible **Google-style docstrings** on all public modules, classes, and functions
- Module-level `logger = logging.getLogger(__name__)` in every source module
- Populated `__init__.py` for every sub-package with public `__all__` exports

### Changed

- **`PatternExtractor`** — replaced `print()` calls with `logging`; removed duplicate `os` import; extracted `_CONFIG_SCHEMA` constant
- **`YamlWriter`** — fixed duplicate file-open bug (file was opened and written twice per pattern)
- **`cli.py`** — removed emoji from log messages for PEP 8 compliance; renamed `format` parameter to `fmt` to avoid shadowing the built-in; added `--n-clusters` to `cluster` command
- **`PatternEnricher`** — uses `list[str]` → `List[str]` for Python 3.10 compatibility; replaced bare `except` with `except OSError`
- **`PatternClusterer`** — `plt.figure()` replaced with `fig, ax = plt.subplots()` to avoid global state
- **`GraphExporter.export_neo4j`** — replaced inline `chr()` escape with a clear string replacement
- **`DirectoryWalker.walk`** — uses `sorted()` for deterministic file ordering across operating systems
- All `__init__.py` files in sub-packages now export public symbols

### Fixed

- `YamlWriter.write()` opened and wrote each file twice; fixed to write once
- `PatternExtractor._split_blocks` returned the full document when `block_elements` was empty regardless of scope; now correctly defaults to returning `[doc]`
- `SemanticCluster.cluster_sentences()` did not handle empty input; now returns `[]` immediately

### Security

- Removed emoji characters from log format strings that could cause encoding issues on some terminals

---

## [0.9.0] — 2024-01-15

### Added

- Initial implementation of `analyze`, `enrich`, `cluster`, `generate-sentences`, `summarize-clusters`, and `export-graph` CLI commands
- `PatternExtractor` — NLTK n-gram frequency mining with configurable scope and POS filtering
- `PatternEnricher` — heuristic metadata inference (title, summary, problem, keywords)
- `PatternClusterer` — sentence-transformer embeddings, KMeans, and UMAP visualisation
- `SentenceGenerator` — grammar-template sentence generation in text/Markdown/HTML
- `GraphExporter` — knowledge-graph export in GraphML, Mermaid, Neo4j Cypher, and JSON
- `WeaviateStore` — optional vector-database adapter
- JSON Schema validation for `config.yaml`
- Docker Compose configuration for Weaviate
- Initial test suite: `test_parser.py`, `test_extractor.py`, `test_enrich_patterns.py`, `test_cluster.py`, `test_yaml_writer.py`, `test_generate_sentences.py`, `test_graph_export.py`, `integration_test.py`
