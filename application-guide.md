# 📘 Pattern Language Miner: How-To Manual

This guide explains how to **use Pattern Language Miner** for its primary tasks: extracting reusable content patterns from a corpus, inspecting the results, and managing the system. Each procedure answers a common question and walks through the task step-by-step.

## 🔍 HOW DO I PREPARE MY DOCUMENTS FOR ANALYSIS?

**Goal**: Ensure your files are in a format compatible with the application.

### ✅ Supported formats:

* `.txt`: plain text
* `.md`: Markdown using CommonMark syntax
* `.html`: simplified HTML (no scripts/styles)

### 📁 Organize your corpus:

1. Create a folder called `docs/`
2. Place all source files there (each file = 1 unit of content)

## ▶️ HOW DO I RUN THE PATTERN MINER?

**Goal**: Extract lexical patterns and write them to YAML files.

### 🧾 Command:

```bash
python -m pattern_language_miner.cli analyze \\
  --input-dir ./docs \\
  --output-dir ./patterns_output \\
  --log-level INFO
```

### 📝 What this does:

* Parses every document in `./docs`
* Extracts recurring n-gram patterns using NLTK
* Outputs YAML pattern files to `./patterns_output`

## 📂 HOW DO I VIEW OR USE THE PATTERN FILES?

**Goal**: Understand and apply the structured patterns.

### 🔄 Output format:

Each pattern is saved as a `.yaml` file, e.g., `pattern-3.yaml`:

```yaml
id: pattern-3
name: manage container
level: chunk
context: Docker commands for managing Weaviate
problem: Running multiple commands manually is error-prone
solution: Use Docker Compose lifecycle commands
example: docker compose up -d
frequency: 4
sources:
  - document: getting_started.md
```

### ✅ Uses:

* Build documentation templates
* Feed into authoring systems
* Index for retrieval and reuse

## 🤖 HOW DO I ENABLE SEMANTIC SEARCH WITH WEAVIATE?

**Goal**: Cluster or retrieve similar patterns using embeddings.

### 🛠️ Steps:

1. Export your OpenAI key:

   ```bash
   export OPENAI_APIKEY=your-key
   ```

2. Start Weaviate:

   ```bash
   docker compose up -d
   ```

3. Use the `WeaviateStore` class in Python to:

   * `upsert_pattern(pattern_dict)`
   * `query_similar_patterns("your search text")`

## 📊 HOW DO I RUN TESTS?

**Goal**: Confirm the system works end-to-end.

### 🧪 Run all unit and integration tests:

```bash
pytest tests/
```

## 🧹 HOW DO I CLEAN UP WEAVIATE?

**Goal**: Remove data or restart from scratch.

### 🔧 Commands:

```bash
# Stop container but keep data
docker compose down

# Stop container and delete all data
docker compose down -v

# Restart clean instance
docker compose down -v && docker compose up -d
```

## 🧱 HOW DO I EXTEND THE SYSTEM?

### 🔧 Add a new file format:

1. Create a new parser in `parser/` that subclasses `BaseParser`.
2. Update `ParserFactory.get_parser()` in `walker.py`.

### 🔎 Change n-gram size:

Modify the `PatternExtractor` configuration:

```python
extractor = PatternExtractor()
extractor.ngram_min = 3
extractor.ngram_max = 5
```

## 🧠 HOW DO I USE PATTERNS TO GENERATE NEW CONTENT?

Use the output YAML and apply Chomsky-style grammar rules:

```text
Template: 
  "To [solve] in the context of [situation], use [method]. For example, [example]."

Input pattern: 
  solution: Restart with Docker Compose
  context: Cleaning Weaviate
  example: docker compose down -v

Generated:
  "To clean Weaviate in the context of Docker container resets, use Restart with Docker Compose. For example, docker compose down -v."
```

This enables AI-based pattern generation and reuse.

## 🧭 Final Notes

* All logs are written to console; set `--log-level DEBUG` for more detail
* You can safely re-run `analyze` without affecting existing YAML files
* Always validate your YAML using JSON Schema for structure compliance

Would you like this linked in your main `README.md` or added to a published docs site?
