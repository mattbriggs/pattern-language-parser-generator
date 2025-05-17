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

### 📂 Output

* `clustered_patterns.json`: Cluster assignments
* `clusters.png`: 2D UMAP plot of clustered patterns

### 📘 Command Reference Fragment: `summarize-clusters`

| Option          | Type | Required | Description                                              |
| --------------- | ---- | -------- | -------------------------------------------------------- |
| `--input-json`  | Path | ✅        | Path to the `clustered_patterns.json` file to summarize. |
| `--output-path` | Path | ✅        | File path where the Markdown summary will be saved.      |

#### Example

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli summarize-clusters \
  --input-json ./output/clustered_patterns.json \
  --output-path ./output/summary.md
```

This will generate a summary like:

```markdown
## Cluster 0

- Restart with Docker Compose
- Use Compose to reset the container state

## Cluster 1

- Build and tag the image
- Use Dockerfile and compose.yaml


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

### 📘 Command Reference: `export-graph`

Exports patterns and their metadata into a graph representation (GraphML, Mermaid, or Neo4j Cypher).

#### Usage

```bash
python -m pattern_language_miner.cli export-graph [OPTIONS]
```

#### Options

| Option          | Required | Description                                                           |
| --------------- | -------- | --------------------------------------------------------------------- |
| `--input-dir`   | ✅        | Directory containing enriched pattern YAML files                      |
| `--format`      | ✅        | Output format: `graphml`, `mermaid`, or `neo4j`                       |
| `--output-path` | ✅        | Output file path (e.g., `graph.graphml`, `graph.cypher`, `graph.mmd`) |

#### Example

```bash
python -m pattern_language_miner.cli export-graph \
  --input-dir ./data/patterns_enriched \
  --format mermaid \
  --output-path ./docs/patterns_diagram.mmd
```

#### `classify-types`

**Description:**
Enrich clustered pattern data with `type` classifications based on content heuristics.

**Usage:**

```bash
classify-types --input-json PATH --output-json PATH
```

**Options:**

| Option          | Required | Description                                                     |
| --------------- | -------- | --------------------------------------------------------------- |
| `--input-json`  | Yes      | Path to the clustered patterns JSON file                        |
| `--output-json` | Yes      | Output path for the enriched JSON with classified pattern types |

**Example:**

```bash
classify-types --input-json clustered_patterns.json --output-json enriched_patterns.json
```

Here's a reference table and description of the **pattern types** and classification logic used in `classify-types`, suitable for documentation.

---

### 🧩 Pattern Type Reference

This table outlines the classification logic used by the `classify-types` command to categorize patterns based on heuristics applied to their content fields.

| Type         | Description                                                               | Heuristic Trigger Fields            | Example Text Snippet                            |
| ------------ | ------------------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------- |
| `how-to`     | Step-by-step procedural guidance for accomplishing a task                 | `solution`, `steps`                 | "To restart the service, run this command..."   |
| `reference`  | Describes the structure or schema of something technical                  | `example`, `fields`, `attributes`   | "The configuration file includes these keys..." |
| `conceptual` | Explains abstract ideas, principles, or background knowledge              | `context`, `description`            | "Containerization allows applications..."       |
| `why`        | Justifies or explains the rationale behind a decision or method           | `rationale`, `reason`               | "We chose Azure for its security compliance..." |
| `pitfall`    | Warns against common mistakes or known failure scenarios                  | `warning`, `caveat`, `anti-pattern` | "Don’t forget to update your SSL cert..."       |
| `other`      | Does not match known categories or lacks sufficient structure to classify | (none matched)                      |                                                 |


### 🧠 Classification Logic (Simplified)

```python
if "steps" in pattern or "solution" in pattern:
    type_ = "how-to"
elif "fields" in pattern or "example" in pattern:
    type_ = "reference"
elif "context" in pattern or "description" in pattern:
    type_ = "conceptual"
elif "rationale" in pattern or "reason" in pattern:
    type_ = "why"
elif "warning" in pattern or "caveat" in pattern or "anti-pattern" in pattern:
    type_ = "pitfall"
else:
    type_ = "other"
```

This logic is intentionally straightforward to make enrichment fast and explainable. It can be refined or replaced with ML classification or rule tuning based on real-world corpora.

The enrich command outputs a directory of enriched YAML files where each file corresponds to a pattern with additional inferred or normalized metadata fields. These enriched files are structured to support downstream clustering, graph export, and generative tasks.

## Notes on the puput fo the enriched 

The `enrich` command outputs a **directory of enriched YAML files** where each file corresponds to a pattern with additional inferred or normalized metadata fields. These enriched files are structured to support downstream clustering, graph export, and generative tasks.

### ✅ Specifically, each YAML file in the output directory will contain:

| Field       | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| `title`     | Inferred or normalized title (from `solution` or fallback text) |
| `summary`   | Auto-generated or fallback summary string                       |
| `keywords`  | Tokenized keywords extracted from the solution                  |
| `problem`   | Inferred problem statement based on heuristics or rules         |
| `solution`  | The original solution field from the input pattern              |
| *\[others]* | Any other original fields present in the source pattern YAML    |

### 📁 Output folder contents (example):

```
enriched/
├── 001-install-docker.yaml
├── 002-restart-service.yaml
├── 003-remove-resource.yaml
...
```

### 🔧 Purpose:

This output becomes the canonical enriched dataset used for:

* `cluster`: semantic clustering
* `generate-sentences`: creating prose summaries
* `export-graph`: generating GraphML, Mermaid, Neo4j views
* future inference/classification extensions (e.g., Bloom’s taxonomy, DITA)

