import logging
import click
from pathlib import Path

from pattern_language_miner.extractor.pattern_extractor import PatternExtractor
from pattern_language_miner.writer.yaml_writer import YamlWriter
from pattern_language_miner.generator.generate_sentences import SentenceGenerator
from pattern_language_miner.cluster.pattern_cluster import PatternClusterer


@click.group()
@click.option("--log-level", default="INFO", help="Set the logging level.")
def cli(log_level):
    """Pattern Language Miner CLI."""
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s %(levelname)s: %(message)s",
    )


@cli.command()
@click.option("--input-dir", required=True, type=click.Path(exists=True))
@click.option("--output-dir", required=True, type=click.Path())
@click.option(
    "--file-types", default="md,txt", help="Comma-separated list of file extensions."
)
def analyze(input_dir, output_dir, file_types):
    """Analyze a directory of Markdown/Text and extract structured patterns."""
    logging.info("🚀 Starting analysis...")

    extractor = PatternExtractor(input_dir=input_dir, file_types=file_types.split(","))
    patterns = extractor.run()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    writer = YamlWriter(output_path)
    writer.write(patterns)

    logging.info(f"✅ Wrote {len(patterns)} patterns to {output_path}")


@cli.command()
@click.option("--input-dir", required=True, type=click.Path(exists=True))
@click.option("--output-dir", required=True, type=click.Path())
@click.option("--field", default="solution", help="Field to cluster on.")
def cluster(input_dir, output_dir, field):
    """Cluster patterns using semantic similarity."""
    logging.info("🚀 Starting pattern clustering...")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clusterer = PatternClusterer(input_dir=input_dir, field=field)
    clusterer.load_patterns()
    if not clusterer.patterns:
        logging.warning("❌ No patterns loaded. Exiting.")
        return

    embeddings = clusterer.embed_patterns()
    reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    clusterer.visualize_clusters(
        reduced, cluster_ids, output_dir / "clusters.png"
    )
    clusterer.generate_cluster_report(
        cluster_ids, output_dir / "clustered_patterns.json"
    )

    logging.info("✅ Clustering complete.")


@cli.command(name="generate-sentences")
@click.option("--input-dir", required=True, type=click.Path(exists=True))
@click.option("--output-path", required=True, type=click.Path())
@click.option(
    "--format",
    type=click.Choice(["text", "markdown", "html"], case_sensitive=False),
    default="text",
    help="Output format (text, markdown, html).",
)
def generate_sentences(input_dir, output_path, format):
    """Generate sentences from pattern YAML using Chomsky-style template."""
    logging.info("🧠 Generating sentences...")

    generator = SentenceGenerator(
        input_dir=input_dir, output_path=output_path, format_=format
    )
    generator.run()

    logging.info(f"✅ Sentences written to {output_path}")


if __name__ == "__main__":
    cli()
