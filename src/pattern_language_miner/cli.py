import logging
import json
import click
import networkx as nx
from pathlib import Path

from pattern_language_miner.extractor.pattern_extractor import PatternExtractor
from pattern_language_miner.writer.yaml_writer import YamlWriter
from pattern_language_miner.generator.generate_sentences import SentenceGenerator
from pattern_language_miner.cluster.pattern_cluster import PatternClusterer
from pattern_language_miner.enricher.pattern_enricher import PatternEnricher
from pattern_language_miner.graph.graph_export import export_graph


@click.group()
@click.option("--log-level", default="INFO", help="Set the logging level.")
@click.pass_context
def cli(ctx, log_level):
    """Pattern Language Miner CLI."""
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/pattern_miner.log"),
            logging.StreamHandler()
        ]
    )
    ctx.ensure_object(dict)
    ctx.obj["LOG_LEVEL"] = log_level


@cli.command(name="analyze")
@click.option("--config", required=True, type=click.Path(exists=True), help="YAML config file defining pattern extraction settings.")
@click.option("--input-dir", required=True, type=click.Path(exists=True), help="Input directory of documents to analyze.")
@click.option("--output-dir", required=True, type=click.Path(), help="Directory to write extracted pattern YAML files.")
@click.pass_context
def analyze(ctx, config, input_dir, output_dir):
    """Analyze a directory of Markdown/Text and extract structured patterns."""
    logging.info("🚀 Starting analysis...")

    extractor = PatternExtractor(
        config_path=Path(config),
        input_dir=Path(input_dir),
        output_dir=Path(output_dir)
    )

    extractor.run()

    logging.info(f"✅ Wrote extracted patterns to {output_dir}")


@cli.command()
@click.option("--input-dir", required=True, type=click.Path(exists=True), help="Directory of enriched YAML pattern files.")
@click.option("--output-dir", required=True, type=click.Path(), help="Directory to write clustering results.")
@click.option("--field", default="solution", help="Field to cluster on (e.g., solution).")
@click.option("--batch-size", default=32, help="Batch size for embedding processing.")
def cluster(input_dir, output_dir, field, batch_size):
    """Cluster patterns using semantic similarity."""
    logging.info("🚀 Starting pattern clustering...")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clusterer = PatternClusterer(input_dir=input_dir, field=field)
    clusterer.load_patterns()
    if not clusterer.patterns:
        logging.warning("❌ No patterns loaded. Exiting.")
        return

    embeddings = clusterer.embed_patterns(batch_size=batch_size)
    reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    clusterer.visualize_clusters(
        reduced, cluster_ids, output_dir / "clusters.png"
    )
    clusterer.generate_cluster_report(
        cluster_ids, output_dir / "clustered_patterns.json"
    )

    logging.info("✅ Clustering complete.")


@cli.command(name="generate-sentences")
@click.option("--input-dir", required=True, type=click.Path(exists=True), help="Directory of enriched YAML pattern files.")
@click.option("--output-path", required=True, type=click.Path(), help="Path to write the generated sentences.")
@click.option(
    "--format",
    type=click.Choice(["text", "markdown", "html"], case_sensitive=False),
    default="text",
    help="Output format for generated sentences.",
)
def generate_sentences(input_dir, output_path, format):
    """Generate sentences from pattern YAML using Chomsky-style template."""
    logging.info("🧠 Generating sentences...")

    generator = SentenceGenerator(
        input_dir=input_dir, output_path=output_path, format_=format
    )
    generator.run()

    logging.info(f"✅ Sentences written to {output_path}")


@cli.command(name="summarize-clusters")
@click.option("--input-json", required=True, type=click.Path(exists=True), help="Path to clustered_patterns.json file.")
@click.option("--output-path", required=True, type=click.Path(), help="Path to write Markdown summary.")
def summarize_clusters(input_json, output_path):
    """Generate a Markdown summary of clustered patterns."""
    logging.info("📖 Summarizing clustered patterns...")

    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    clusters = {}
    for pattern in data:
        cid = pattern.get("cluster", "unassigned")
        clusters.setdefault(cid, []).append(pattern)

    lines = ["# Cluster Summary\n"]
    for cid in sorted(clusters):
        lines.append(f"## Cluster {cid}\n")
        for p in clusters[cid]:
            title = p.get("title", "Untitled").strip()
            problem = p.get("problem", "")
            summary = p.get("summary", "")
            tags = ", ".join(p.get("tags", []))
            concepts = ", ".join(p.get("concepts", []))
            lines.append(f"- **Title**: {title}")
            if problem:
                lines.append(f"  - Problem: {problem}")
            if summary:
                lines.append(f"  - Summary: {summary}")
            if tags:
                lines.append(f"  - Tags: {tags}")
            if concepts:
                lines.append(f"  - Concepts: {concepts}")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logging.info(f"✅ Summary written to {output_path}")


@cli.command(name="enrich")
@click.option("--input-dir", required=True, type=click.Path(exists=True), help="Directory of raw extracted patterns.")
@click.option("--output-dir", required=True, type=click.Path(), help="Directory to write enriched pattern files.")
def enrich(input_dir, output_dir):
    """Enrich patterns with inferred fields like problem, title, summary, and keywords."""
    logging.info("🧠 Enriching patterns...")

    enricher = PatternEnricher(input_dir=input_dir, output_dir=output_dir)
    enricher.run()

    logging.info(f"✅ Enriched patterns written to {output_dir}")


@cli.command(name="export-graph")
@click.option("--input-json", required=True, type=click.Path(exists=True), help="Path to enriched patterns JSON file.")
@click.option("--output-path", required=True, type=click.Path(), help="Path to write the graph output file.")
@click.option(
    "--format",
    type=click.Choice(["graphml", "neo4j", "mermaid", "json"], case_sensitive=False),
    default="graphml",
    help="Graph output format (graphml, neo4j, mermaid, json)."
)
def export_graph_cmd(input_json, output_path, format):
    """Export enriched pattern data as a graph."""
    logging.info(f"🌐 Exporting graph from {input_json} to {output_path} as {format}...")

    def sanitize_id(text):
        return text.strip().replace(" ", "_").replace("-", "_").replace(".", "_")

    with open(input_json, "r", encoding="utf-8") as f:
        patterns = json.load(f)

    G = nx.DiGraph()

    for pattern in patterns:
        title = pattern.get("title", "Untitled").strip()
        node_id = sanitize_id(title)
        G.add_node(node_id, label=title, type="pattern")

        for tag in pattern.get("tags", []):
            tag_id = sanitize_id(tag)
            G.add_node(tag_id, label=tag, type="tag")
            G.add_edge(node_id, tag_id, relationship="has_tag")

        for concept in pattern.get("concepts", []):
            concept_id = sanitize_id(concept)
            G.add_node(concept_id, label=concept, type="concept")
            G.add_edge(node_id, concept_id, relationship="about")

        for related in pattern.get("related", []):
            related_id = sanitize_id(related)
            G.add_node(related_id, label=related, type="pattern")
            G.add_edge(node_id, related_id, relationship="related_to")

    export_graph(G, Path(output_path), format)
    logging.info("✅ Graph export complete.")


if __name__ == "__main__":
    cli()