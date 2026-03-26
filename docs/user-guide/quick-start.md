# Quick Start

This walkthrough takes you from a folder of documents to a fully enriched, clustered, and exported pattern library in five commands.

---

## Step 1: Prepare Your Documents

Collect the files you want to mine. Supported formats:

- `.txt` — plain text
- `.md` / `.markdown` — Markdown
- `.html` / `.htm` — HTML

Place them in a directory, for example `./my-docs/`.

---

## Step 2: Create a Configuration File

Create `config.yaml` in your working directory:

```yaml
pattern_extraction:
  file_type: md           # md, txt, or html
  frequency_threshold: 2  # minimum occurrences to count as a pattern
  minimum_token_count: 3  # minimum tokens per sentence to analyse
  scope: sentence         # line | sentence | block
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  ngram_min: 2
  ngram_max: 5
```

See [Configuration](configuration.md) for all options and their effects.

---

## Step 3: Extract Patterns

```bash
pattern-miner analyze \
  --config config.yaml \
  --input-dir ./my-docs \
  --output-dir ./raw-patterns
```

This produces one YAML file per detected pattern in `./raw-patterns/`.

**Example output file** (`raw-patterns/pattern-00001.yaml`):

```yaml
pattern: install the package
frequency: 7
```

---

## Step 4: Enrich Patterns

```bash
pattern-miner enrich \
  --input-dir ./raw-patterns \
  --output-dir ./enriched
```

The enricher adds `title`, `summary`, `problem`, and `keywords` fields to each pattern.

---

## Step 5: Cluster Patterns

```bash
pattern-miner cluster \
  --input-dir ./enriched \
  --output-dir ./clusters
```

Outputs:
- `clusters/clusters.png` — scatter-plot of the 2-D UMAP projection
- `clusters/clustered_patterns.json` — patterns with cluster IDs assigned

---

## Step 6: Generate Readable Sentences

```bash
pattern-miner generate-sentences \
  --input-dir ./enriched \
  --output-path ./patterns.md \
  --format markdown
```

---

## Step 7: Export a Knowledge Graph

```bash
pattern-miner export-graph \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./graph.mmd \
  --format mermaid
```

The resulting Mermaid diagram can be embedded directly in any Markdown file.

---

## Summarise Clusters

```bash
pattern-miner summarize-clusters \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./cluster-summary.md
```

---

## Full Pipeline Script

```bash
#!/usr/bin/env bash
set -euo pipefail

pattern-miner analyze    --config config.yaml --input-dir ./docs --output-dir ./raw
pattern-miner enrich     --input-dir ./raw    --output-dir ./enriched
pattern-miner cluster    --input-dir ./enriched --output-dir ./clusters
pattern-miner generate-sentences \
  --input-dir ./enriched --output-path ./output.md --format markdown
pattern-miner export-graph \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./graph.mmd --format mermaid
```

---

!!! tip "Logging"
    Add `--log-level DEBUG` to any command for verbose output:
    ```bash
    pattern-miner --log-level DEBUG analyze --config config.yaml ...
    ```
