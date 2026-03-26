# Commands

All commands are available via the `pattern-miner` entry-point or
`python -m pattern_language_miner.cli`.

---

## Global Options

```
pattern-miner [OPTIONS] COMMAND [ARGS]...
```

| Option | Default | Description |
|---|---|---|
| `--log-level` | `INFO` | Python logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `--help` | — | Show help and exit |

---

## `analyze`

Extract frequent lexical n-gram patterns from a directory of documents.

```bash
pattern-miner analyze \
  --config <path>       \
  --input-dir <path>    \
  --output-dir <path>
```

| Option | Required | Description |
|---|---|---|
| `--config` | Yes | Path to the YAML extraction config file |
| `--input-dir` | Yes | Directory containing source documents |
| `--output-dir` | Yes | Directory where extracted pattern YAMLs are written |

**Output:** One `pattern-NNNNN.yaml` file per extracted pattern.

**Example:**
```bash
pattern-miner analyze \
  --config config.yaml \
  --input-dir ./docs \
  --output-dir ./raw-patterns
```

---

## `enrich`

Add inferred metadata fields (`title`, `summary`, `problem`, `keywords`) to raw patterns.

```bash
pattern-miner enrich \
  --input-dir <path>  \
  --output-dir <path>
```

| Option | Required | Description |
|---|---|---|
| `--input-dir` | Yes | Directory of raw extracted YAML pattern files |
| `--output-dir` | Yes | Directory where enriched files are written (same filenames) |

**Example:**
```bash
pattern-miner enrich \
  --input-dir ./raw-patterns \
  --output-dir ./enriched
```

---

## `cluster`

Cluster enriched patterns using sentence-transformer embeddings, KMeans, and UMAP.

```bash
pattern-miner cluster \
  --input-dir <path>   \
  --output-dir <path>  \
  [--field TEXT]       \
  [--batch-size INT]   \
  [--n-clusters INT]
```

| Option | Default | Description |
|---|---|---|
| `--input-dir` | — | Directory of enriched YAML pattern files |
| `--output-dir` | — | Directory to write clustering output |
| `--field` | `solution` | Pattern field to embed and cluster |
| `--batch-size` | `32` | Embedding batch size |
| `--n-clusters` | `5` | Number of KMeans clusters |

**Output:**

- `clusters.png` — scatter plot of the 2-D UMAP projection
- `clustered_patterns.json` — all patterns with a `cluster` ID field

**Example:**
```bash
pattern-miner cluster \
  --input-dir ./enriched \
  --output-dir ./clusters \
  --n-clusters 8
```

---

## `generate-sentences`

Convert enriched YAML pattern files into human-readable sentences.

```bash
pattern-miner generate-sentences \
  --input-dir <path>    \
  --output-path <path>  \
  [--format TEXT]
```

| Option | Default | Description |
|---|---|---|
| `--input-dir` | — | Directory of enriched YAML pattern files |
| `--output-path` | — | Destination file for generated output |
| `--format` | `text` | Output format: `text`, `markdown`, `html` |

**Example:**
```bash
pattern-miner generate-sentences \
  --input-dir ./enriched \
  --output-path ./patterns.md \
  --format markdown
```

---

## `summarize-clusters`

Generate a Markdown summary of all clusters from `clustered_patterns.json`.

```bash
pattern-miner summarize-clusters \
  --input-json <path>   \
  --output-path <path>
```

| Option | Required | Description |
|---|---|---|
| `--input-json` | Yes | Path to the `clustered_patterns.json` file |
| `--output-path` | Yes | Destination Markdown file |

**Example:**
```bash
pattern-miner summarize-clusters \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./cluster-summary.md
```

---

## `export-graph`

Export enriched pattern data as a knowledge graph in one of four formats.

```bash
pattern-miner export-graph \
  --input-json <path>   \
  --output-path <path>  \
  [--format TEXT]
```

| Option | Default | Description |
|---|---|---|
| `--input-json` | — | Path to `clustered_patterns.json` |
| `--output-path` | — | Destination file |
| `--format` | `graphml` | Format: `graphml`, `mermaid`, `neo4j`, `json` |

**Format details:**

| Format | Use Case |
|---|---|
| `graphml` | Import into Gephi, yEd, or other graph tools |
| `mermaid` | Embed diagrams directly in Markdown files |
| `neo4j` | Import into a Neo4j database via Cypher |
| `json` | Machine-readable node-link JSON |

**Example:**
```bash
pattern-miner export-graph \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./graph.mmd \
  --format mermaid
```
