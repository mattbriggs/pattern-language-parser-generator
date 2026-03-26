"""Command-line interface for the Pattern Language Miner.

Entry-point: ``pattern-miner`` (or ``python -m pattern_language_miner.cli``).

Commands
--------
analyze
    Extract lexical n-gram patterns from a directory of documents.
enrich
    Add inferred metadata to raw extracted patterns.
cluster
    Cluster enriched patterns by semantic similarity.
generate-sentences
    Convert pattern YAML files to readable sentences.
summarize-clusters
    Produce a Markdown summary of clustered patterns.
export-graph
    Export enriched patterns as a knowledge graph.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import click
import networkx as nx

from pattern_language_miner.cluster.pattern_cluster import PatternClusterer
from pattern_language_miner.enricher.pattern_enricher import PatternEnricher
from pattern_language_miner.extractor.pattern_extractor import PatternExtractor
from pattern_language_miner.generator.generate_sentences import SentenceGenerator
from pattern_language_miner.graph.graph_export import export_graph
from pattern_language_miner.writer.yaml_writer import YamlWriter

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------


@click.group()
@click.option(
    "--log-level",
    default="INFO",
    show_default=True,
    help="Python logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
)
@click.pass_context
def cli(ctx: click.Context, log_level: str) -> None:
    """Pattern Language Miner — corpus-driven pattern extraction and generation."""
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s  %(name)-30s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    # Ensure the logs directory exists and add a file handler.
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "pattern_miner.log")
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s  %(name)-30s  %(levelname)-8s  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logging.getLogger().addHandler(file_handler)

    ctx.ensure_object(dict)
    ctx.obj["LOG_LEVEL"] = log_level


# ---------------------------------------------------------------------------
# analyze
# ---------------------------------------------------------------------------


@cli.command(name="analyze")
@click.option(
    "--config",
    required=True,
    type=click.Path(exists=True),
    help="YAML config file defining pattern extraction settings.",
)
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True),
    help="Input directory of documents to analyse.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(),
    help="Directory to write extracted pattern YAML files.",
)
@click.pass_context
def analyze(
    ctx: click.Context, config: str, input_dir: str, output_dir: str
) -> None:
    """Analyse a directory of documents and extract structured patterns."""
    logger.info("Starting analysis of %s.", input_dir)
    extractor = PatternExtractor(
        config_path=Path(config),
        input_dir=Path(input_dir),
        output_dir=Path(output_dir),
    )
    extractor.run()
    logger.info("Extracted patterns written to %s.", output_dir)


# ---------------------------------------------------------------------------
# enrich
# ---------------------------------------------------------------------------


@cli.command(name="enrich")
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True),
    help="Directory of raw extracted pattern YAML files.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(),
    help="Directory to write enriched pattern files.",
)
def enrich(input_dir: str, output_dir: str) -> None:
    """Enrich patterns with inferred fields: problem, title, summary, keywords."""
    logger.info("Enriching patterns in %s.", input_dir)
    enricher = PatternEnricher(input_dir=input_dir, output_dir=output_dir)
    enricher.run()
    logger.info("Enriched patterns written to %s.", output_dir)


# ---------------------------------------------------------------------------
# cluster
# ---------------------------------------------------------------------------


@cli.command(name="cluster")
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True),
    help="Directory of enriched YAML pattern files.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(),
    help="Directory to write clustering results.",
)
@click.option(
    "--field",
    default="solution",
    show_default=True,
    help="Pattern field to cluster on.",
)
@click.option(
    "--batch-size",
    default=32,
    show_default=True,
    help="Batch size for embedding processing.",
)
@click.option(
    "--n-clusters",
    default=5,
    show_default=True,
    help="Number of KMeans clusters.",
)
def cluster(
    input_dir: str,
    output_dir: str,
    field: str,
    batch_size: int,
    n_clusters: int,
) -> None:
    """Cluster patterns using semantic similarity."""
    logger.info("Starting pattern clustering.")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    clusterer = PatternClusterer(input_dir=input_dir, field=field)
    clusterer.load_patterns()
    if not clusterer.patterns:
        logger.warning("No patterns loaded. Exiting.")
        return

    embeddings = clusterer.embed_patterns(batch_size=batch_size)
    reduced, cluster_ids = clusterer.cluster_and_reduce(
        embeddings, n_clusters=n_clusters
    )
    clusterer.visualize_clusters(reduced, cluster_ids, out / "clusters.png")
    clusterer.generate_cluster_report(cluster_ids, out / "clustered_patterns.json")
    logger.info("Clustering complete. Results in %s.", out)


# ---------------------------------------------------------------------------
# generate-sentences
# ---------------------------------------------------------------------------


@cli.command(name="generate-sentences")
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True),
    help="Directory of enriched YAML pattern files.",
)
@click.option(
    "--output-path",
    required=True,
    type=click.Path(),
    help="Path to write the generated sentences.",
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "markdown", "html"], case_sensitive=False),
    default="text",
    show_default=True,
    help="Output format for generated sentences.",
)
def generate_sentences(input_dir: str, output_path: str, fmt: str) -> None:
    """Generate human-readable sentences from pattern YAML files."""
    logger.info("Generating sentences from %s.", input_dir)
    generator = SentenceGenerator(
        input_dir=input_dir, output_path=output_path, format_=fmt
    )
    generator.run()
    logger.info("Sentences written to %s.", output_path)


# ---------------------------------------------------------------------------
# summarize-clusters
# ---------------------------------------------------------------------------


@cli.command(name="summarize-clusters")
@click.option(
    "--input-json",
    required=True,
    type=click.Path(exists=True),
    help="Path to clustered_patterns.json file.",
)
@click.option(
    "--output-path",
    required=True,
    type=click.Path(),
    help="Path to write the Markdown summary.",
)
def summarize_clusters(input_json: str, output_path: str) -> None:
    """Generate a Markdown summary of clustered patterns."""
    logger.info("Summarising clustered patterns from %s.", input_json)

    with open(input_json, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    clusters: dict = {}
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
            lines.append(f"- **{title}**")
            if problem:
                lines.append(f"  - Problem: {problem}")
            if summary:
                lines.append(f"  - Summary: {summary}")
            if tags:
                lines.append(f"  - Tags: {tags}")
            if concepts:
                lines.append(f"  - Concepts: {concepts}")
        lines.append("")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    logger.info("Summary written to %s.", output_path)


# ---------------------------------------------------------------------------
# export-graph
# ---------------------------------------------------------------------------


@cli.command(name="export-graph")
@click.option(
    "--input-json",
    required=True,
    type=click.Path(exists=True),
    help="Path to enriched patterns JSON file.",
)
@click.option(
    "--output-path",
    required=True,
    type=click.Path(),
    help="Path to write the graph output file.",
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["graphml", "neo4j", "mermaid", "json"], case_sensitive=False),
    default="graphml",
    show_default=True,
    help="Graph output format.",
)
def export_graph_cmd(input_json: str, output_path: str, fmt: str) -> None:
    """Export enriched pattern data as a knowledge graph."""
    logger.info("Exporting graph from %s as %s.", input_json, fmt)

    with open(input_json, "r", encoding="utf-8") as fh:
        patterns = json.load(fh)

    def _sanitize(text: str) -> str:
        return text.strip().replace(" ", "_").replace("-", "_").replace(".", "_")

    graph = nx.DiGraph()
    for pattern in patterns:
        title = pattern.get("title", "Untitled").strip()
        node_id = _sanitize(title)
        graph.add_node(node_id, label=title, type="pattern")

        for tag in pattern.get("tags", []):
            tag_id = _sanitize(tag)
            graph.add_node(tag_id, label=tag, type="tag")
            graph.add_edge(node_id, tag_id, relationship="has_tag")

        for concept in pattern.get("concepts", []):
            concept_id = _sanitize(concept)
            graph.add_node(concept_id, label=concept, type="concept")
            graph.add_edge(node_id, concept_id, relationship="about")

        for related in pattern.get("related", []):
            related_id = _sanitize(related)
            graph.add_node(related_id, label=related, type="pattern")
            graph.add_edge(node_id, related_id, relationship="related_to")

    export_graph(graph, Path(output_path), fmt)
    logger.info("Graph export complete.")


if __name__ == "__main__":
    cli()
