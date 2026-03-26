# CLI Reference

Complete reference for the `pattern-miner` command-line interface.

## Invocation

```bash
# Via installed entry-point
pattern-miner [--log-level LEVEL] COMMAND [OPTIONS]

# Via Python module
python -m pattern_language_miner.cli [--log-level LEVEL] COMMAND [OPTIONS]
```

## Global Options

| Flag | Default | Description |
|---|---|---|
| `--log-level` | `INFO` | Logging verbosity: `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `--help` | — | Show help and exit |

---

## `analyze`

```
pattern-miner analyze --config PATH --input-dir PATH --output-dir PATH
```

Reads all files matching `file_type` in `--input-dir`, tokenises them with NLTK, counts n-gram frequencies, and writes one YAML file per pattern meeting the frequency threshold.

**Options:**

| Flag | Type | Required | Description |
|---|---|---|---|
| `--config` | PATH | Yes | YAML extraction configuration file |
| `--input-dir` | PATH | Yes | Directory of source documents |
| `--output-dir` | PATH | Yes | Directory for output YAML patterns |

---

## `enrich`

```
pattern-miner enrich --input-dir PATH --output-dir PATH
```

Reads each `*.yaml` / `*.yml` file in `--input-dir` and adds inferred fields.

| Flag | Type | Required | Description |
|---|---|---|---|
| `--input-dir` | PATH | Yes | Raw pattern YAML directory |
| `--output-dir` | PATH | Yes | Enriched output directory |

---

## `cluster`

```
pattern-miner cluster --input-dir PATH --output-dir PATH [OPTIONS]
```

| Flag | Type | Default | Description |
|---|---|---|---|
| `--input-dir` | PATH | — | Enriched pattern directory |
| `--output-dir` | PATH | — | Output directory for PNG + JSON |
| `--field` | TEXT | `solution` | Pattern field to embed |
| `--batch-size` | INT | `32` | Embedding batch size |
| `--n-clusters` | INT | `5` | KMeans cluster count |

---

## `generate-sentences`

```
pattern-miner generate-sentences --input-dir PATH --output-path PATH [--format FORMAT]
```

| Flag | Type | Default | Description |
|---|---|---|---|
| `--input-dir` | PATH | — | Enriched pattern directory |
| `--output-path` | PATH | — | Output file path |
| `--format` | CHOICE | `text` | `text`, `markdown`, or `html` |

---

## `summarize-clusters`

```
pattern-miner summarize-clusters --input-json PATH --output-path PATH
```

| Flag | Type | Required | Description |
|---|---|---|---|
| `--input-json` | PATH | Yes | `clustered_patterns.json` from `cluster` |
| `--output-path` | PATH | Yes | Markdown summary output file |

---

## `export-graph`

```
pattern-miner export-graph --input-json PATH --output-path PATH [--format FORMAT]
```

| Flag | Type | Default | Description |
|---|---|---|---|
| `--input-json` | PATH | — | `clustered_patterns.json` |
| `--output-path` | PATH | — | Output graph file |
| `--format` | CHOICE | `graphml` | `graphml`, `mermaid`, `neo4j`, or `json` |
