# Configuration Reference

Full reference for all fields in `config.yaml`, validated against
`src/pattern_language_miner/schema/config_schema.json`.

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["pattern_extraction"],
  "properties": {
    "pattern_extraction": {
      "type": "object",
      "required": [
        "file_type",
        "frequency_threshold",
        "minimum_token_count",
        "scope"
      ]
    }
  }
}
```

## Fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_type` | string | Yes | — | `md`, `txt`, or `html` |
| `frequency_threshold` | integer | Yes | — | Min occurrences for inclusion |
| `minimum_token_count` | integer | Yes | — | Min tokens per sentence |
| `scope` | string | Yes | — | `line`, `sentence`, or `block` |
| `ngram_min` | integer | No | `2` | Minimum n-gram size |
| `ngram_max` | integer | No | `5` | Maximum n-gram size |
| `pos_filtering` | boolean | No | `false` | Enable POS-tag filtering |
| `allowed_pos_tags` | array | No | `[]` | Permitted Penn Treebank POS tags |
| `block_elements` | array | No | `[]` | Elements for block scoping |

## Complete Example

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
