import click
import logging
import json
import os

from .utils.logging import setup_logging
from .walker import DirectoryWalker
from .extractor.pattern_extractor import PatternExtractor
from .output.yaml_writer import YAMLWriter


@click.command()
@click.option(
    "--input-dir", "-i",
    required=True,
    type=click.Path(exists=True),
    help="Directory containing text, markdown, or HTML files."
)
@click.option(
    "--output-dir", "-o",
    required=True,
    type=click.Path(),
    help="Directory to save extracted pattern YAML files."
)
@click.option(
    "--log-level",
    default="INFO",
    help="Logging level (DEBUG, INFO, WARNING, ERROR)."
)
def analyze(input_dir: str, output_dir: str, log_level: str):
    """
    Analyze a directory of documents and extract recurring lexical patterns,
    saving the results as individual YAML files.
    """
    setup_logging(getattr(logging, log_level.upper(), logging.INFO))
    logging.info("🔍 Starting Pattern Language Miner")
    logging.info(f"📂 Scanning directory: {input_dir}")
    logging.info(f"📁 Output directory: {output_dir}")

    walker = DirectoryWalker(input_dir)
    extractor = PatternExtractor()
    writer = YAMLWriter(output_dir)

    all_texts = []
    file_count = 0
    skipped_files = []

    logging.info("🧭 Walking files...")

    for file_path, content, parser in walker.walk():
        logging.debug(f"📄 Reading file: {file_path}")
        try:
            parsed = parser.parse(content)
            file_count += 1
            if parsed["type"] == "text":
                all_texts.extend(parsed["lines"])
            elif parsed["type"] in {"markdown", "html"}:
                all_texts.append(parsed["html"])
        except Exception as e:
            logging.warning(f"⚠️ Failed to parse {file_path}: {e}")
            skipped_files.append(str(file_path))

    print(f"✅ Corpus found. {file_count} file(s) will be analyzed.")

    if file_count == 0:
        logging.warning("⚠️ No valid input files found. Exiting.")
        return

    logging.info(f"✅ Parsed {file_count} file(s).")

    patterns = extractor.extract_lexical_patterns(all_texts)

    if not patterns:
        logging.warning(
            "⚠️ No lexical patterns met frequency threshold. "
            "Try reducing min_frequency."
        )
        return

    logging.info(f"📊 Extracted {len(patterns)} pattern(s). Writing to YAML...")

    os.makedirs(output_dir, exist_ok=True)

    for i, pattern in enumerate(patterns):
        yaml_data = {
            "id": f"pattern-{i+1}",
            "name": pattern["pattern"],
            "level": "chunk",
            "context": "Discovered through frequency analysis.",
            "problem": "Frequent phrasing may signal reusable content.",
            "solution": pattern["pattern"],
            "example": pattern["pattern"],
            "sources": [{"document": "N/A"}],
            "frequency": pattern["frequency"]
        }
        writer.write_pattern(yaml_data, f"pattern-{i+1}.yaml")

    logging.info(f"📝 Wrote {len(patterns)} YAML files.")
    logging.info("✅ Pattern mining complete.")

    summary = {
        "input_directory": input_dir,
        "output_directory": output_dir,
        "files_processed": file_count,
        "patterns_found": len(patterns),
        "files_skipped": skipped_files
    }

    summary_path = os.path.join(output_dir, "summary_report.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"📄 Summary written to: {summary_path}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    analyze()