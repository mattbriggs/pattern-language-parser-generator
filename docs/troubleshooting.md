# 🛠️ Logging and Troubleshooting Guide

All command-line operations in the Pattern Language Miner tool automatically generate logs to help users understand execution flow and diagnose issues.



## 📁 Where Logs Are Saved

Logs are written to a file named:

```

pattern\_miner.log

```

This file is created in the same directory where you run the CLI command unless you've configured a different logging path.



## 📋 What's Included in the Log

Each log entry contains:

- **Timestamp** - when the event occurred  
- **Log level** - severity (`INFO`, `WARNING`, `ERROR`)  
- **Message** - description of the action or issue  

### Example Log Output

```

2025-05-16 18:26:20,178 INFO: 🚀 Starting analysis...
2025-05-16 18:26:21,001 WARNING: ⚠️ Skipping malformed file: intro.md
2025-05-16 18:26:22,512 INFO: ✅ Wrote 135 patterns to /path/to/output

````



## 🔍 Viewing Logs

You can open the log file in your preferred text editor:

### macOS

```bash
open pattern_miner.log
````

### Windows

```bash
notepad pattern_miner.log
```

### Linux

```bash
xdg-open pattern_miner.log
```

### Live Tailing (all systems with `tail`)

```bash
tail -f pattern_miner.log
```

This command allows you to view logs in real-time as the tool runs.



## ✅ When to Check Logs

* If a command appears to hang or exit unexpectedly
* If you suspect a file is being skipped or malformed
* To confirm which patterns were processed or skipped
* To trace enrichment, clustering, or graph export progress



## 📌 Tip

Use the `--log-level DEBUG` flag on any CLI command for more verbose logs:

```bash
PYTHONPATH=src python -m pattern_language_miner.cli analyze \
  --input-dir ./corpus \
  --output-dir ./patterns \
  --file-types md \
  --log-level DEBUG
```

This setting will include detailed diagnostics in `pattern_miner.log`.

## Related content

* [Command Reference](command-reference.md)
* [config.yml Reference and Usage Guide](configuration-file-reference.md)
* [Instructions for Docker and Weaviate Integration](instructions_for_docker.md)
* [Pattern Language Miner: A Corpus-Driven Pattern Extraction and Generation Tool](application-design.md)
* [Pattern Language Miner: How-To Manual](application-guide.md)
* [Set up and installation of the Pattern Language Miner](set-up-and-installation.md)
* [Workflow](workflow.md)