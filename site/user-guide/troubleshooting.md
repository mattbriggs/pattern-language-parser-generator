# Troubleshooting

## Log Files

Every command writes to `logs/pattern_miner.log` in your working directory. Use this as your first debugging resource.

```bash
# Tail the log in real time
tail -f logs/pattern_miner.log

# View on macOS
open logs/pattern_miner.log
```

Enable verbose output with:

```bash
pattern-miner --log-level DEBUG analyze ...
```

---

## Common Issues

### No patterns extracted

**Symptom:** The output directory is empty after running `analyze`.

**Causes and fixes:**

| Cause | Fix |
|---|---|
| `file_type` in config doesn't match your files | Set `file_type: md` (or `txt`, `html`) to match your documents |
| `frequency_threshold` too high | Lower it to `1` or `2` to capture rarer patterns |
| Documents are very short | Lower `minimum_token_count` to `1` or `2` |
| Wrong `--input-dir` | Verify the path contains files with the expected extension |

---

### NLTK resource errors

**Symptom:**
```
LookupError: Resource punkt not found.
```

**Fix:**
```bash
python setup_resources.py
```

Or manually inside Python:
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
```

---

### Sentence-transformer model download fails

**Symptom:** `ConnectionError` or `OSError` when running `cluster`.

**Fix:** Ensure you have internet access on first run. Models are cached in `~/.cache/huggingface/` after the initial download.

---

### Config validation error

**Symptom:**
```
ValidationError: Config validation error: 'frequency_threshold' is a required property
```

**Fix:** Compare your `config.yaml` against the [Configuration Reference](configuration.md). All required fields must be present.

---

### Weaviate connection refused

**Symptom:**
```
weaviate.exceptions.UnexpectedStatusCodeException: ... refused
```

**Fix:** Start Weaviate with Docker Compose:
```bash
docker compose up -d
```

Then wait ~10 seconds for the service to become healthy before retrying.

---

### `pattern-miner: command not found`

**Fix:** Activate your virtual environment and ensure the package is installed:
```bash
source ENV/bin/activate
pip install -e ".[dev]"
```

Or run directly:
```bash
python -m pattern_language_miner.cli --help
```

---

### Cluster scatter plot is empty or unreadable

**Symptom:** `clusters.png` shows only one or two points.

**Cause:** Too few patterns were loaded (UMAP and KMeans require at least as many samples as clusters).

**Fix:** Lower `--n-clusters` to match the number of patterns you have, or lower `frequency_threshold` to extract more patterns.

---

## Getting Help

If none of the above resolves your issue, please open a GitHub issue with:

1. The exact command you ran
2. The contents of `logs/pattern_miner.log`
3. Your Python version (`python --version`)
4. Your OS and package versions (`pip freeze`)
