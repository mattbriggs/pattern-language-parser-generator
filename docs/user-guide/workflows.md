# Workflows

This page describes common usage workflows, from simple single-step operations to a complete end-to-end pipeline.

---

## Workflow 1: Quick Pattern Survey

Use this workflow to get a rapid overview of the recurring language in a corpus.

```bash
# Extract patterns with a low threshold
pattern-miner analyze \
  --config config.yaml \
  --input-dir ./docs \
  --output-dir ./raw

# Enrich with readable metadata
pattern-miner enrich \
  --input-dir ./raw \
  --output-dir ./enriched

# Generate a readable Markdown list
pattern-miner generate-sentences \
  --input-dir ./enriched \
  --output-path ./overview.md \
  --format markdown
```

---

## Workflow 2: Semantic Clustering & Visualisation

Use this workflow to discover thematic groups within your pattern library.

```bash
pattern-miner analyze  --config config.yaml --input-dir ./docs  --output-dir ./raw
pattern-miner enrich   --input-dir ./raw    --output-dir ./enriched

# Cluster with 8 groups, embedding the 'solution' field
pattern-miner cluster \
  --input-dir ./enriched \
  --output-dir ./clusters \
  --field solution \
  --n-clusters 8

# Produce a Markdown summary grouped by cluster
pattern-miner summarize-clusters \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./cluster-report.md
```

The `clusters/clusters.png` scatter plot gives a visual overview of how patterns group together.

---

## Workflow 3: Knowledge Graph Export

Use this workflow to export your pattern library as a linked knowledge graph.

```bash
pattern-miner analyze  --config config.yaml --input-dir ./docs  --output-dir ./raw
pattern-miner enrich   --input-dir ./raw    --output-dir ./enriched
pattern-miner cluster  --input-dir ./enriched --output-dir ./clusters

# Mermaid diagram for documentation
pattern-miner export-graph \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./graph.mmd \
  --format mermaid

# Neo4j Cypher for database import
pattern-miner export-graph \
  --input-json ./clusters/clustered_patterns.json \
  --output-path ./graph.cypher \
  --format neo4j
```

---

## Workflow 4: Full Automation Script

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT="./docs"
CONFIG="./config.yaml"
RAW="./output/raw"
ENRICHED="./output/enriched"
CLUSTERS="./output/clusters"
REPORT="./output/report"

mkdir -p "$RAW" "$ENRICHED" "$CLUSTERS" "$REPORT"

echo "==> Extracting patterns..."
pattern-miner --log-level INFO analyze \
  --config "$CONFIG" \
  --input-dir "$INPUT" \
  --output-dir "$RAW"

echo "==> Enriching patterns..."
pattern-miner enrich \
  --input-dir "$RAW" \
  --output-dir "$ENRICHED"

echo "==> Clustering..."
pattern-miner cluster \
  --input-dir "$ENRICHED" \
  --output-dir "$CLUSTERS" \
  --n-clusters 10

echo "==> Generating sentences..."
pattern-miner generate-sentences \
  --input-dir "$ENRICHED" \
  --output-path "$REPORT/sentences.md" \
  --format markdown

echo "==> Summarising clusters..."
pattern-miner summarize-clusters \
  --input-json "$CLUSTERS/clustered_patterns.json" \
  --output-path "$REPORT/cluster-summary.md"

echo "==> Exporting graph..."
pattern-miner export-graph \
  --input-json "$CLUSTERS/clustered_patterns.json" \
  --output-path "$REPORT/graph.mmd" \
  --format mermaid

echo "Done! Results in $REPORT"
```

---

## Workflow 5: Incremental Updates

If your document corpus grows, you can re-run only the steps that need updating:

```bash
# Only re-extract from new documents (add them to ./docs)
pattern-miner analyze --config config.yaml --input-dir ./docs --output-dir ./raw

# Re-enrich and re-cluster
pattern-miner enrich  --input-dir ./raw     --output-dir ./enriched
pattern-miner cluster --input-dir ./enriched --output-dir ./clusters
```

!!! note
    Each run **overwrites** the output directory. Archive previous results
    before re-running if you need to compare outputs.

---

## Tips

- Use `--log-level DEBUG` on any command for verbose diagnostic output.
- All output directories are created automatically — no need to `mkdir` first.
- Tune `frequency_threshold` and `ngram_min`/`ngram_max` in `config.yaml` if the number of extracted patterns is too high or too low.
