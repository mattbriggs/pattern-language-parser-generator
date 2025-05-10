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
