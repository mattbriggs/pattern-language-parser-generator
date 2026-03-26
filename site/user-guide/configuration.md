# Configuration

The `analyze` command reads a YAML configuration file that controls every aspect of the extraction process.

---

## Minimal Config

```yaml
pattern_extraction:
  file_type: md
  frequency_threshold: 2
  minimum_token_count: 3
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  ngram_min: 2
  ngram_max: 5
```

---

## Reference

### `file_type`

**Type:** `string` — one of `md`, `txt`, `html`
**Default:** `md`

The file extension of documents to process. Only files matching this extension inside `--input-dir` will be read.

```yaml
file_type: md
```

---

### `frequency_threshold`

**Type:** `integer` ≥ 1
**Default:** `3`

An n-gram must appear at least this many times across all analysed documents to be included in the output. Increase this value to reduce noise; decrease it to capture rarer patterns.

```yaml
frequency_threshold: 2
```

---

### `minimum_token_count`

**Type:** `integer` ≥ 1
**Default:** `2`

Sentences with fewer tokens than this value are skipped entirely before n-gram extraction. Useful for filtering out headings, labels, and other very short lines.

```yaml
minimum_token_count: 5
```

---

### `scope`

**Type:** `string` — one of `line`, `sentence`, `block`
**Default:** `sentence`

Determines how each document is split into analysis units before tokenisation:

| Value | Behaviour |
|---|---|
| `line` | Each non-empty line is a unit |
| `sentence` | NLTK sentence tokeniser splits the document |
| `block` | Blank-line-separated paragraphs are units |

```yaml
scope: sentence
```

---

### `ngram_min` / `ngram_max`

**Type:** `integer`
**Defaults:** `ngram_min: 2`, `ngram_max: 5`

The minimum and maximum number of tokens in an extracted n-gram.

```yaml
ngram_min: 2
ngram_max: 5
```

---

### `pos_filtering`

**Type:** `boolean`
**Default:** `false`

When `true`, only sentences in which **every token** has an allowed POS tag (see `allowed_pos_tags`) will be processed.

```yaml
pos_filtering: true
```

---

### `allowed_pos_tags`

**Type:** `array` of strings
**Default:** `[]`

Penn Treebank POS tag codes that are permitted when `pos_filtering` is enabled. Leave empty to allow all tags.

```yaml
allowed_pos_tags:
  - NN    # Noun, singular
  - NNS   # Noun, plural
  - VB    # Verb, base form
  - VBZ   # Verb, 3rd person singular present
```

---

### `block_elements`

**Type:** `array` of strings
**Default:** `[]`

When `scope` is `block`, include `paragraph` to split on blank lines.

```yaml
block_elements:
  - paragraph
```

---

## Full Example Config

```yaml
pattern_extraction:
  file_type: md
  frequency_threshold: 3
  minimum_token_count: 4
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  ngram_min: 2
  ngram_max: 6
```

---

## Validation

The configuration is validated at start-up against the JSON Schema in
`src/pattern_language_miner/schema/config_schema.json`.
An informative error is raised if a required field is missing or a value is out of range.
