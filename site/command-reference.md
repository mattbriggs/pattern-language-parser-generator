# Command Reference: Pattern Language Miner CLI

The **Pattern Language Miner CLI** is a modular command-line interface that supports pattern discovery, enrichment, clustering, summarization, and graph export of recurring lexical structures in text-based content. It is designed for knowledge engineers, content strategists, and machine learning practitioners working with structured authoring and content reuse.

---

## `analyze`

**Purpose**: Extract frequent lexical patterns (n-grams) from structured or unstructured documents.

**Command Syntax**:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli analyze \
  --config config.yaml \
  --input-dir ./docs \
  --output-dir ./patterns-raw \
  --log-level INFO
```

### Parameters

| Parameter      | Description                                             | Required | Example          |
| -------------- | ------------------------------------------------------- | -------- | ---------------- |
| `--config`     | Path to YAML configuration file                         | ✅        | `./config.yaml`  |
| `--input-dir`  | Directory containing `.md`, `.txt`, or `.html` files    | ✅        | `./docs`         |
| `--output-dir` | Directory to save extracted pattern YAML files          | ✅        | `./patterns-raw` |
| `--log-level`  | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | ❌        | `DEBUG`          |

### Output

* Individual YAML pattern files (e.g., `pattern-00001.yaml`)
* Optional summary files (JSON or stats pending future updates)

---

## `enrich`

**Purpose**: Enrich raw patterns with inferred metadata: `title`, `summary`, `keywords`, and `problem`.

**Command Syntax**:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli enrich \
  --input-dir ./patterns-raw \
  --output-dir ./patterns-enriched
```

### Parameters

| Parameter      | Description                                 | Required | Example               |
| -------------- | ------------------------------------------- | -------- | --------------------- |
| `--input-dir`  | Directory with raw pattern YAML files       | ✅        | `./patterns-raw`      |
| `--output-dir` | Output directory for enriched pattern files | ✅        | `./patterns-enriched` |

### Output Structure

Each enriched YAML file will include:

| Field      | Description                                          |
| ---------- | ---------------------------------------------------- |
| `title`    | Inferred from the `solution` field                   |
| `summary`  | Generated description of the pattern                 |
| `keywords` | List of tokens extracted from the solution           |
| `problem`  | Heuristically inferred problem based on the solution |

---

## `cluster`

**Purpose**: Group semantically similar patterns using vector embeddings and clustering.

**Command Syntax**:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli cluster \
  --input-dir ./patterns-enriched \
  --output-dir ./patterns-cluster \
  --field solution \
  --batch-size 32
```

### Parameters

| Parameter      | Description                                 | Required | Example               |
| -------------- | ------------------------------------------- | -------- | --------------------- |
| `--input-dir`  | Directory of enriched YAML files            | ✅        | `./patterns-enriched` |
| `--output-dir` | Output folder for cluster results           | ✅        | `./patterns-cluster`  |
| `--field`      | Field to embed for similarity clustering    | ❌        | `solution`            |
| `--batch-size` | Embedding batch size for inference pipeline | ❌        | `32`                  |

### Output

* `clustered_patterns.json`: Patterns with cluster IDs
* `clusters.png`: 2D visualization of the clusters

---

## `summarize-clusters`

**Purpose**: Generate a human-readable summary of each cluster group.

**Command Syntax**:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli summarize-clusters \
  --input-json ./patterns-cluster/clustered_patterns.json \
  --output-path ./patterns-cluster/summary.md
```

### Parameters

| Parameter       | Description                               | Required | Example                                      |
| --------------- | ----------------------------------------- | -------- | -------------------------------------------- |
| `--input-json`  | Clustered JSON with pattern metadata      | ✅        | `./patterns-cluster/clustered_patterns.json` |
| `--output-path` | Markdown file to save the cluster summary | ✅        | `./patterns-cluster/summary.md`              |

---

## `generate-sentences`

**Purpose**: Generate natural language descriptions from structured patterns.

**Command Syntax**:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli generate-sentences \
  --input-dir ./patterns-enriched \
  --output-path ./patterns-generated.md \
  --format markdown
```

### Parameters

| Parameter       | Description                                | Required | Example               |
| --------------- | ------------------------------------------ | -------- | --------------------- |
| `--input-dir`   | Directory of enriched YAML pattern files   | ✅        | `./patterns-enriched` |
| `--output-path` | Destination for generated sentence content | ✅        | `./patterns.md`       |
| `--format`      | Output format: `text`, `markdown`, `html`  | ❌        | `markdown`            |

---

## `export-graph`

**Purpose**: Convert enriched patterns into graph representations for visualization or integration.

**Command Syntax**:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli export-graph \
  --input-json ./patterns-cluster/clustered_patterns.json \
  --format graphml \
  --output-path ./patterns-graph.graphml
```

### Parameters

| Parameter       | Description                                   | Required | Example                                      |
| --------------- | --------------------------------------------- | -------- | -------------------------------------------- |
| `--input-json`  | Path to the enriched or clustered JSON file   | ✅        | `./patterns-cluster/clustered_patterns.json` |
| `--format`      | Format: `graphml`, `mermaid`, `neo4j`, `json` | ✅        | `graphml`                                    |
| `--output-path` | Output file to save the graph                 | ✅        | `./patterns-graph.graphml`                   |

---

## Related Topics

* [Configuration File Reference](configuration-file-reference.md)
* [Using the Pattern Enricher](application-guide.md#enrich)
* [Understanding Clusters](application-design.md#clustering)
* [Troubleshooting Pattern Miner](troubleshooting.md)
* [Set up and Installation](set-up-and-installation.md)
* [Docker and Weaviate Integration](instructions_for_docker.md)
