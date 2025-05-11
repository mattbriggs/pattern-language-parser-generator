## 🔧 Command Reference

The Pattern Language Miner provides a modular CLI interface composed of subcommands. Each subcommand represents a distinct function in the content pattern mining pipeline.

### 🔍 `analyze`

**Purpose**:
Extract recurring lexical patterns from a directory of content files and save them in structured YAML format.

**Description**:
This command parses a corpus of `.txt`, `.md`, or `.html` documents, mines common phrases (n-grams), and outputs a pattern for each one that meets a frequency threshold. It is the foundational step in discovering reusable documentation structures.

**Problem**:
Content creators often duplicate common language and formatting across files, but these patterns remain hidden and are hard to reuse or model.

**Solution**:
By mining lexical patterns across your corpus, this command transforms undocumented repetition into explicit, structured content patterns, usable in downstream authoring, templating, or retrieval systems.

#### ✅ Command Syntax

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli analyze \
  --input-dir ./docs \
  --output-dir ./patterns_output \
  --log-level INFO
```
#### 🧾 Parameters

| Parameter      | Description                                                | Required | Example             |
| -- | - | -- | - |
| `--input-dir`  | Path to folder containing source `.txt`, `.md`, or `.html` | ✅        | `./docs`            |
| `--output-dir` | Directory to write YAML pattern files and summary JSON     | ✅        | `./patterns_output` |
| `--log-level`  | Logging level: DEBUG, INFO, WARNING, ERROR                 | ❌        | `DEBUG`             |
#### 💬 When & Why to Use

Use `analyze` when:

* You want to mine a large content corpus for repeating phrasing
* You want to bootstrap a pattern library from real-world content
* You're preparing data for clustering or authoring automation

This command is ideal for the **first pass** in building a modular knowledge system and can be rerun safely as documents evolve.

#### 📄 Output Files

* YAML files in `--output-dir`, one per pattern (e.g., `pattern-1.yaml`)
* A JSON summary: `summary_report.json` with stats on processing

#### 🔄 Next Steps After `analyze`

* Use `validate` (coming soon) to ensure pattern structure compliance
* Use `cluster` (planned) to semantically group similar patterns
* Feed into a pattern-based authoring or retrieval system

## 🤝 `cluster`

**Purpose**: Cluster and visualize semantically similar patterns using vector embeddings.

**Description**:  
This command reads YAML pattern files (e.g., `pattern-*.yaml`), embeds the chosen text field (like `solution`), and groups similar entries using KMeans. It reduces embeddings to 2D using UMAP and plots them using matplotlib + seaborn.

**Problem**:  
Manual inspection of similar content is time-consuming and error-prone.

**Solution**:  
Automatically detect and visualize groups of similar content to identify redundancy, support deduplication, or reveal thematic trends.

### ✅ Command

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli cluster \
  --input-dir ./patterns_output \
  --field solution
```

### 🧾 Parameters

| Parameter     | Description                            | Required | Example             |
| ------------- | -------------------------------------- | -------- | ------------------- |
| `--input-dir` | Path to folder with YAML pattern files | ✅        | `./patterns_output` |
| `--field`     | YAML field to embed and cluster        | ❌        | `solution`          |

## 🧠 `generate-sentences`

**Purpose**: Convert structured YAML patterns into natural language summaries.

**Description**:  
This command loads patterns (e.g., `pattern-*.yaml`), applies a fixed sentence template, and outputs human-readable content in the desired format.

**Problem**:  
Pattern data is machine-readable but not easy to communicate to humans.

**Solution**:  
Generate structured summaries that are ready for reuse, training, or review.

### ✅ Command

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli generate-sentences \
  --input-dir ./patterns_output \
  --output-path ./docs/patterns.md \
  --format markdown
```

### 🧾 Parameters

| Parameter       | Description                                  | Required | Example              |
| --------------- | -------------------------------------------- | -------- | -------------------- |
| `--input-dir`   | Folder of `pattern-*.yaml` files             | ✅        | `./patterns_output`  |
| `--output-path` | Where to save generated output file          | ✅        | `./docs/patterns.md` |
| `--format`      | Output format: `text`, `markdown`, or `html` | ❌        | `markdown`           |

### 📄 Output

* A single file containing generated sentences
* Format varies by `--format` option

### 📂 Output

* `clustered_patterns.json`: Cluster assignments
* `clusters.png`: 2D UMAP plot of clustered patterns