import click
import logging
from .utils.logging import setup_logging
from .walker import DirectoryWalker
from .extractor.pattern_extractor import PatternExtractor
from .output.yaml_writer import YAMLWriter


@click.command()
@click.option("--input-dir", "-i", required=True, type=click.Path(exists=True),
              help="Directory containing text, markdown, or HTML files.")
@click.option("--output-dir", "-o", required=True, type=click.Path(),
              help="Directory to save extracted pattern YAML files.")
@click.option("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR).")
def analyze(input_dir: str, output_dir: str, log_level: str):
    """
    Analyze a directory of documents and extract recurring lexical patterns,
    saving the results as individual YAML files.
    """
    setup_logging(getattr(logging, log_level.upper(), logging.INFO))
    logging.info("Starting pattern analysis.")
    logging.debug(f"Input directory: {input_dir}")
    logging.debug(f"Output directory: {output_dir}")

    walker = DirectoryWalker(input_dir)
    extractor = PatternExtractor()
    writer = YAMLWriter(output_dir)

    all_texts = []
    for file_path, content, parser in walker.walk():
        parsed = parser.parse(content)
        logging.info(f"Parsed: {file_path}")
        if parsed["type"] == "text":
            all_texts.extend(parsed["lines"])
        elif parsed["type"] in {"markdown", "html"}:
            all_texts.append(parsed["html"])

    patterns = extractor.extract_lexical_patterns(all_texts)

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

    logging.info(f"Extracted {len(patterns)} patterns.")
    logging.info("Pattern analysis complete.")