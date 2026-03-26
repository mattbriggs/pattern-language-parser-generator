"""Knowledge-graph export module.

Builds a directed graph (``networkx.DiGraph``) from enriched pattern data
and exports it in one of four formats:

- **GraphML** — portable XML graph format.
- **Mermaid** — Markdown-embeddable diagram syntax.
- **Neo4j** — Cypher script ready to import into a Neo4j database.
- **JSON** — node-link JSON (``networkx`` node-link format).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import networkx as nx

logger = logging.getLogger(__name__)


class GraphExporter:
    """Build and export a directed graph from enriched pattern dictionaries.

    The graph nodes represent patterns, tags, and concepts.  Edges carry a
    ``relationship`` attribute describing the semantic link.

    Args:
        patterns: List of enriched pattern dictionaries.

    Example:
        >>> exporter = GraphExporter(patterns)
        >>> exporter.build_graph()
        >>> exporter.export_graphml(Path("output.graphml"))
    """

    def __init__(self, patterns: List[Dict[str, Any]]) -> None:
        self.patterns = patterns
        self.graph: nx.DiGraph = nx.DiGraph()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_graph(self) -> None:
        """Populate :attr:`graph` from :attr:`patterns`.

        Each pattern becomes a node.  Tags, concepts, and related patterns
        each generate additional nodes connected by typed edges.
        """
        for pattern in self.patterns:
            title = pattern.get("title", "Untitled").strip()
            node_id = self._sanitize_id(title)
            self.graph.add_node(node_id, label=title, type="pattern")

            for tag in pattern.get("tags", []):
                tag_id = self._sanitize_id(tag)
                self.graph.add_node(tag_id, label=tag, type="tag")
                self.graph.add_edge(node_id, tag_id, relationship="has_tag")

            for concept in pattern.get("concepts", []):
                concept_id = self._sanitize_id(concept)
                self.graph.add_node(concept_id, label=concept, type="concept")
                self.graph.add_edge(node_id, concept_id, relationship="about")

            for related in pattern.get("related", []):
                related_id = self._sanitize_id(related)
                self.graph.add_node(related_id, label=related, type="pattern")
                self.graph.add_edge(
                    node_id, related_id, relationship="related_to"
                )

        logger.debug(
            "Graph built: %d nodes, %d edges.",
            self.graph.number_of_nodes(),
            self.graph.number_of_edges(),
        )

    def export_graphml(self, output_path: Path) -> None:
        """Write the graph in GraphML format.

        Args:
            output_path: Destination path for the ``.graphml`` file.
        """
        logger.info("Exporting GraphML to %s.", output_path)
        nx.write_graphml(self.graph, output_path)
        logger.info("GraphML export complete.")

    def export_mermaid(self, output_path: Path) -> None:
        """Write the graph as a Mermaid ``graph TD`` diagram.

        Args:
            output_path: Destination path for the Mermaid file.
        """
        logger.info("Exporting Mermaid diagram to %s.", output_path)
        lines = ["graph TD"]
        for source, target, data in self.graph.edges(data=True):
            label = data.get("relationship", "")
            lines.append(f"    {source} -->|{label}| {target}")
        output_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Mermaid export complete.")

    def export_neo4j(self, output_path: Path) -> None:
        """Write a Cypher script that recreates the graph in Neo4j.

        Args:
            output_path: Destination path for the ``.cypher`` file.
        """
        logger.info("Exporting Neo4j Cypher script to %s.", output_path)
        lines: List[str] = []

        for node_id, attrs in self.graph.nodes(data=True):
            props = ", ".join(
                f'{k}: "{str(v).replace(chr(34), chr(92) + chr(34))}"'
                for k, v in attrs.items()
                if isinstance(v, (str, int, float))
            )
            node_type = attrs.get("type", "Node")
            lines.append(
                f'MERGE (n:{node_type} {{ id: "{node_id}", {props} }});'
            )

        for source, target, attrs in self.graph.edges(data=True):
            rel_type = attrs.get("relationship", "RELATED_TO").upper()
            lines.append(
                f'MATCH (a {{ id: "{source}" }}), (b {{ id: "{target}" }}) '
                f"CREATE (a)-[:{rel_type}]->(b);"
            )

        output_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Neo4j export complete.")

    def export_json(self, output_path: Path) -> None:
        """Write the graph in node-link JSON format.

        Args:
            output_path: Destination path for the ``.json`` file.
        """
        logger.info("Exporting JSON graph to %s.", output_path)
        data = nx.readwrite.json_graph.node_link_data(self.graph)
        with output_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        logger.info("JSON export complete.")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize_id(text: str) -> str:
        """Normalise *text* for use as a graph node identifier.

        Args:
            text: Raw label text.

        Returns:
            A string with spaces, hyphens, and dots replaced by underscores.
        """
        return text.strip().replace(" ", "_").replace("-", "_").replace(".", "_")


def export_graph(graph: nx.DiGraph, output_path: Path, format_: str) -> None:
    """Export *graph* to *output_path* in the requested *format_*.

    This function acts as a *Facade* over :class:`GraphExporter` for
    callers that have already built the graph externally (e.g. the CLI).

    Args:
        graph: A pre-built :class:`~networkx.DiGraph`.
        output_path: Destination file path.
        format_: One of ``"graphml"``, ``"mermaid"``, ``"neo4j"``,
            or ``"json"`` (case-insensitive).

    Raises:
        ValueError: If *format_* is not recognised.
    """
    exporter = GraphExporter([])
    exporter.graph = graph

    dispatch = {
        "graphml": exporter.export_graphml,
        "mermaid": exporter.export_mermaid,
        "neo4j": exporter.export_neo4j,
        "json": exporter.export_json,
    }
    fmt = format_.lower()
    if fmt not in dispatch:
        raise ValueError(
            f"Unsupported graph format {format_!r}. "
            f"Choose from: {', '.join(sorted(dispatch))}"
        )
    dispatch[fmt](output_path)
