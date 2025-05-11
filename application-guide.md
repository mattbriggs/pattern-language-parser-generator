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

## 🔍 How to Cluster Patterns

Clustering helps you group patterns that are semantically similar using AI-powered embeddings.

### 🧭 When to Use
- After running `analyze` to extract patterns
- When you want to find related ideas across different files
- To support deduplication or build cluster-driven navigation

### 🧪 Steps

1. **Ensure you have pattern YAML files** from the `analyze` command.
2. Run the cluster command:

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli cluster \
  --input-dir ./patterns_output \
  --field solution
```

3. **Review the outputs**:

   * `clustered_patterns.json`: Maps each pattern to a cluster ID
   * `clusters.png`: A 2D plot showing each pattern in its cluster

### 🧠 Notes

* By default, it uses the `solution` field for clustering.
* You can change this to `problem`, `example`, or any other key in your YAML files.
* Embedding is done locally using the `sentence-transformers` model `all-MiniLM-L6-v2`.

## 🧠 How to Generate Sentences from Patterns

The `generate-sentences` command creates readable instructional sentences from your pattern YAML files using a Chomsky-style generative template.

### 🧭 When to Use
- After you’ve run `analyze` and created YAML pattern files
- To produce plain language summaries
- To support reuse, training, or publishing workflows

### 🧪 Steps

1. Run the command:

```bash
PYTHONPATH=src python3 -m pattern_language_miner.cli generate-sentences \
  --input-dir ./patterns_output \
  --output-path ./docs/patterns.md \
  --format markdown
```

2. Choose an output format:

   * `text`: plain numbered list
   * `markdown`: suitable for docs or GitHub
   * `html`: structured output for web embedding

3. View the results:

   * `patterns.md`, `patterns.txt`, or `patterns.html`

### 🧠 Example Template Used

> To **{problem}** in the context of **{context}**, use **{solution}**.
> For example, **{example}**.


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
