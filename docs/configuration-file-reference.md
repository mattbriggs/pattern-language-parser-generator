## `config.yml` Reference and Usage Guide

The `config.yml` file provides granular control over the pattern extraction process, enabling precise definition of "raw patterns". Here's a detailed guide covering each setting, its implications, and how you can use them effectively.


### 📌 `pattern_extraction` Settings

#### 🔹 `frequency_threshold`

* **Description:** Sets the minimum number of occurrences a pattern must have across the corpus to be considered significant.
* **Type:** Integer
* **Default Recommendation:** `3`
* **Usage:**

  * Lower values (`1` or `2`) include more patterns, possibly capturing noise or trivial repetition.
  * Higher values (`5+`) result in fewer, more significant patterns.

#### 🔹 `minimum_token_count`

* **Description:** Defines the minimum number of words (tokens) in a pattern for inclusion.
* **Type:** Integer
* **Recommended Range:** `2` to `5`
* **Usage:**

  * Lower numbers (`1` or `2`) may capture very short and less meaningful patterns.
  * Higher numbers (`4+`) yield patterns that are more contextually meaningful.

#### 🔹 `scope`

* **Description:** Determines the textual boundaries used to identify patterns.
* **Allowed Values:**

  * `line`: Patterns confined to single lines of text.
  * `sentence`: Patterns confined to grammatical sentences.
  * `block`: Patterns confined to structural units (e.g., paragraphs, lists, tables).
* **Recommended Usage:**

  * Use `sentence` for natural language processing and semantic analysis.
  * Use `block` for technical documents or structured content.

#### 🔹 `pos_filtering`

* **Description:** Toggles Part-of-Speech (POS) filtering.
* **Type:** Boolean (`true` or `false`)
* **Recommended Default:** `true`
* **Implications:**

  * `true`: Enables filtering based on grammatical roles (verbs, nouns, adjectives).
  * `false`: Includes all word forms, potentially introducing noise.

#### 🔹 `allowed_pos_tags`

* **Description:** Specifies grammatical tags allowed in patterns (effective only if `pos_filtering: true`).
* **Common Tags:**

  * `VB`: Verb, base form ("run")
  * `VBD`: Verb, past tense ("ran")
  * `VBG`: Verb, gerund or present participle ("running")
  * `VBN`: Verb, past participle ("run")
  * `VBP`: Verb, non-3rd person singular present ("run")
  * `VBZ`: Verb, 3rd person singular present ("runs")
  * `NN`: Noun, singular ("cat")
  * `NNS`: Noun, plural ("cats")
  * `JJ`: Adjective ("quick")
  * `RB`: Adverb ("quickly")
* **Recommended Usage:**

  * For action-oriented content, focus on verbs (`VB`, `VBD`, `VBG`, `VBN`).
  * For descriptive or technical content, include nouns and adjectives (`NN`, `NNS`, `JJ`).

#### 🔹 `block_elements`

* **Description:** Defines what structural elements constitute a "block".
* **Allowed Values:**

  * `paragraph`
  * `list`
  * `ordered_list`
  * `table`
  * `heading`
  * `blockquote`
* **Recommended Usage:**

  * For technical documentation, focus on `list`, `ordered_list`, and `table`.
  * For prose or narrative, primarily use `paragraph` and `blockquote`.



### 🧑‍💻 Example Complete Configuration

```yaml
pattern_extraction:
  frequency_threshold: 3
  minimum_token_count: 3
  scope: block
  pos_filtering: true
  allowed_pos_tags:
    - VB
    - VBD
    - VBG
    - VBN
    - VBP
    - VBZ
    - NN
    - NNS
    - JJ
  block_elements:
    - paragraph
    - list
    - ordered_list
    - table
```



## 🎯 Applying Configuration in Different Discourse Domains

### 1. **Technical Writing**

* **Goal:** Identify clear, reusable procedures or actions.
* **Recommended Settings:**

  * **Scope:** `block` (focus on structural units)
  * **POS Filtering:** Enable (`true`)
  * **Allowed POS Tags:** Primarily verbs (`VB`, `VBG`, `VBN`) and nouns (`NN`, `NNS`).
  * **Block Elements:** Lists, tables, and ordered lists

### 2. **Fiction/Narrative Writing**

* **Goal:** Discover frequently used phrases, stylistic patterns, or dialogue rhythms.
* **Recommended Settings:**

  * **Scope:** `sentence`
  * **POS Filtering:** Enable (`true`)
  * **Allowed POS Tags:** Verbs (`VBD`, `VBZ`), nouns (`NN`, `NNS`), adjectives (`JJ`)
  * **Block Elements:** Paragraph

### 3. **Hybrid Content**

* **Goal:** Analyze content mixing narrative and technical elements (e.g., instructional storytelling).
* **Recommended Settings:**

  * **Scope:** `sentence`
  * **POS Filtering:** Enable (`true`)
  * **Allowed POS Tags:** Comprehensive list of verbs, nouns, adjectives
  * **Block Elements:** Paragraph, list, table



## 🗒️ Discussion on Defining Raw Patterns

### **Technical Documentation:**

* Patterns emerge around tasks and procedures ("configure network settings").
* Useful for creating consistent, reusable instructional content.

### **Narrative Writing:**

* Patterns reveal character speech patterns or stylistic traits ("he said quietly", "she glanced briefly").
* Helpful for maintaining stylistic coherence or identifying clichés.

### **Hybrid or Multi-genre Writing:**

* Patterns assist in identifying successful blending techniques ("illustrate the scenario by...", "consider the implications...").
* Supports creating novel structures or unique storytelling formats.



## ✅ Practical Workflow Example

1. **Edit `config.yml`** based on your corpus and goal.
2. Run the analyze command:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli analyze \
  --input-dir './your_corpus' \
  --output-dir './patterns_output' \
  --file-types md \
  --config './config.yml'
```

3. Review generated YAML patterns to refine or enrich further.
