
# Patter Miner CookBook

This is a "cook‑book" style guide that pulls together everything you have built so far and shows, step‑by‑step, how to run a **complete pattern‑mining cycle** on a fresh corpus, enrich the results, explore them, and finally generate new material from your pattern language.

## 1  | Overview & Purpose

| Stage            | Why it exists                                                                | Key CLI command(s)      | Typical artefacts                         |
| ---------------- | ---------------------------------------------------------------------------- | ----------------------- | ----------------------------------------- |
| **Analyse**      | Parse source files and discover raw patterns (chunks, sections, documents).  | `analyze`               | `*.yaml` pattern files                    |
| **Enrich**       | Add missing metadata (problem, title, summary, keywords, info‑type, etc.).   | `enrich`                | enriched `*.yaml` files                   |
| **Cluster**      | Group semantically similar patterns to reveal structural themes.             | `cluster`               | `clustered_patterns.json`, `clusters.png` |
| **Summarise**    | Produce a human‑readable tour of each cluster.                               | `summarize-clusters`    | `cluster_summary.md`                      |
| **Graph**        | Visualise links (related, tags, concepts) as a graph.                        | `export-graph`          | `graph.graphml` / `graph.mmd`…            |
| **Sentence‑Gen** | Turn patterns into reusable Chomsky‑style templates.                         | `generate-sentences`    | sentences in `.md`, `.txt` or `.html`     |
| **(Optional)**   | **Extend / plug‑ins**: classifiers, new enrichers, new graph exporters, etc. | any plug‑in entry‑point | custom artefacts                          |



## 2  | End‑to‑End Workflow (Concrete Example)

> **Corpus location:** `/data/corpora/azure‑docs`
> **Results base folder:** `/data/pattern01`

```bash
# 1. Mine raw patterns
PYTHONPATH=src python -m pattern_language_miner.cli analyze \
  --input-dir   /data/corpora/azure-docs \
  --output-dir  /data/pattern01/raw \
  --file-types  md,txt,html

# 2. Enrich patterns with titles, problems, summaries, keywords …
PYTHONPATH=src python -m pattern_language_miner.cli enrich \
  --input-dir   /data/pattern01/raw \
  --output-dir  /data/pattern01/enriched

# 3. Cluster on the "solution" field using 32‑batch SBERT embeddings
PYTHONPATH=src python -m pattern_language_miner.cli cluster \
  --input-dir   /data/pattern01/enriched \
  --output-dir  /data/pattern01 \
  --field       solution \
  --batch-size  32

# 4. Human‑friendly cluster report
PYTHONPATH=src python -m pattern_language_miner.cli summarize-clusters \
  --input-json  /data/pattern01/clustered_patterns.json \
  --output-path /data/pattern01/cluster_summary.md

# 5. Graph export (GraphML view of patterns ↔ tags / concepts / related)
PYTHONPATH=src python -m pattern_language_miner.cli export-graph \
  --input-json  /data/pattern01/clustered_patterns.json \
  --format      graphml \
  --output-path /data/pattern01/graph.graphml

# 6. Auto‑generate sentences in Markdown
PYTHONPATH=src python -m pattern_language_miner.cli generate-sentences \
  --input-dir   /data/pattern01/enriched \
  --output-path /data/pattern01/generated_sentences.md \
  --format      markdown
```

After these six commands you will have:

```text
/data/pattern01/
├── raw/                       # raw *.yaml mined patterns
├── enriched/                  # richer *.yaml with problem/title/keywords
├── clustered_patterns.json    # list[dict] with "cluster" field
├── clusters.png               # UMAP scatter plot
├── cluster_summary.md         # quick narrative of each cluster
├── graph.graphml              # import into yEd, Gephi, Neo4j Desktop…
└── generated_sentences.md     # ready‑to‑use sentence templates
```

## 3  | Process Walk‑Through

1. **Analyse**
   *Parser ➜ Extractor ➜ YAML Writer*

   * Runs structural & NLP parsing (sentences, headings, sections).
   * Detects repeated n‑grams, structural templates, semantic clusters.
   * Emits *minimal* pattern YAML (often only `solution`, `example`, `frequency`).

2. **Enrich**
   *PatternEnricher* infers:

   * `problem` (via simple heuristics right now; replace with spaCy or LLM).
   * `title` (slugified first sentence if missing).
   * `summary` (single‑sentence abstractive summary baseline).
   * `keywords` (top‑k TF‑IDF tokens).
   * `info_type` (classifier stub).
     ✔ Saves enriched YAML next to raw so the raw is preserved.

3. **Cluster**

   * SBERT "all‑MiniLM‑L6‑v2" embeddings on `solution` or any chosen field.
   * K‑Means (auto‑reduces `k` if fewer samples).
   * UMAP 2‑D reduction for pretty plots.
   * Stores cluster id back into each pattern JSON record.

4. **Summarise**

   * Groups by `cluster` → Markdown bulleted list.
   * Easy for SMEs to eyeball what each cluster represents.

5. **Graph Export**

   * Reads JSON records, builds DiGraph:

     * `related` ⇒ edges *pattern* → *pattern* (`RELATED_TO`)
     * `tags`    ⇒ edges *pattern* → *tag*     (`HAS_TAG`)
     * `concepts`⇒ edges *pattern* → *concept* (`ABOUT`)
   * Choose GraphML (for yEd/Gephi), Mermaid (Markdown diagrams), Neo4j Cypher.

6. **Generate Sentences**

   * Chomsky‑style template:

     ```
     To <problem> in the context of <context>, use <solution>. For example, <example>.
     ```
   * Output in plain text, Markdown list or HTML `<ol>` depending on `--format`.

## 4  | Discussion - Interpreting the Findings

| Artifact                 | How to read it                                                  | Typical insights                                                           |
| ------------------------ | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `clusters.png`           | Dense blobs = high repetition; sparse points = unique patterns. | Identify canonical procedures vs ad‑hoc snippets.                          |
| `cluster_summary.md`     | Scan headings to name clusters; drill into YAML for detail.     | Quickly spot "installation", "troubleshooting", "definition" buckets.      |
| `graph.graphml`          | Load in yEd → layout hierarchy. Colours by node type.           | Shows which tags/concepts span multiple patterns; highlights orphan nodes. |
| `generated_sentences.md` | Ready prompts for LLM few‑shot or doc boiler‑plates.            | Feed into ChatGPT to draft new docs; use in static site generators.        |

## 5  | Using the Outputs for Content Generation

1. **Few‑shot prompts** - paste 3‑5 generated sentences into ChatGPT, ask "write a new troubleshooting article using the same pattern language but about Azure VMs."
2. **Programmatic** - feed YAML + assembly rules into a small Python script that randomly picks patterns per cluster to create novel documents (fun for fiction mash‑ups).
3. **Authoring aid** - writers open `graph.graphml`, navigate patterns, drag nodes into an outline, copy corresponding `solution` text.
4. **LLM fine‑tuning** - convert YAML to JSONL where each entry is a `<pattern>` pair; fine‑tune a model to output "problem → solution" style.

## 6  | Extending the CLI (Plug‑in Road‑Map)

| Gap                                 | Quick plug‑in idea                                                                                                |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Better **info‑type** classification | Add `classify-types` sub‑command that calls a BERT or OpenAI "classification" endpoint, writes `info_type` field. |
| Multi‑genre mixing                  | Introduce a `genre` field in YAML, cluster per‑genre first, then blend clusters with `mix-genres` plug‑in.        |
| Rich graphs                         | Support `--format d3` to export `.json` ready for interactive D3 visualisation.                                   |
| Advanced summariser                 | Plug‑in that uses LLM to produce "Cluster abstracts" and "Top 5 representative examples".                         |

All new features can live under `src/pattern_language_miner/plugins/<plugin_name>/` and register their CLI via `cli.add_command()` in a light entry‑point loader.

## 7  | Key Take‑aways

* **Linear workflow** keeps the mental model simple → each artefact feeds the next.
* **Artificats are incremental** - you can re‑run just `enrich` or `cluster` without repeating mining.
* **Outputs are multi‑purpose** - human review, LLM prompts, graph analysis, content generation.
* The project is fully **extensible** via plug‑ins: new enrichers, classifiers, exporters, or even alternative clustering algorithms.

Enjoy mining, exploring - and *creating* new documents with your custom pattern language.
