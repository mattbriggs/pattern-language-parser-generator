import json
import logging
from pathlib import Path
import networkx as nx


class GraphExporter:
    def __init__(self, patterns):
        self.patterns = patterns
        self.graph = nx.DiGraph()

    def _sanitize_id(self, text: str) -> str:
        return text.strip().replace(" ", "_").replace("-", "_").replace(".", "_")

    def build_graph(self):
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
                self.graph.add_edge(node_id, related_id, relationship="related_to")

    def export_graphml(self, output_path: Path):
        logging.info(f"📤 Exporting GraphML to {output_path}")
        nx.write_graphml(self.graph, output_path)
        logging.info("✅ GraphML export complete.")

    def export_mermaid(self, output_path: Path):
        logging.info(f"📤 Exporting Mermaid to {output_path}")
        lines = ["graph TD"]
        for source, target, data in self.graph.edges(data=True):
            label = data.get("relationship", "")
            lines.append(f"    {source} -->|{label}| {target}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logging.info("✅ Mermaid export complete.")

    def export_neo4j(self, output_path: Path):
        logging.info(f"📤 Exporting Neo4j Cypher script to {output_path}")
        lines = []
        for node_id, attrs in self.graph.nodes(data=True):
            props = ", ".join(
                f'{k}: "{str(v).replace(chr(34), "\\\"")}"'
                for k, v in attrs.items()
                if isinstance(v, (str, int, float))
            )
            lines.append(f'MERGE (n:{attrs.get("type", "Node")} {{ id: "{node_id}", {props} }});')

        for source, target, attrs in self.graph.edges(data=True):
            rel_type = attrs.get("relationship", "RELATED_TO").upper()
            lines.append(
                f'MATCH (a {{ id: "{source}" }}), (b {{ id: "{target}" }}) '
                f'CREATE (a)-[:{rel_type}]->(b);'
            )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logging.info("✅ Neo4j export complete.")

    def export_json(self, output_path: Path):
        logging.info(f"📤 Exporting graph as JSON to {output_path}")
        data = nx.readwrite.json_graph.node_link_data(self.graph)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info("✅ JSON export complete.")


def export_graph(graph: nx.DiGraph, output_path: Path, format_: str):
    format_ = format_.lower()
    exporter = GraphExporter([])  # graph already built externally
    exporter.graph = graph

    if format_ == "graphml":
        exporter.export_graphml(output_path)
    elif format_ == "mermaid":
        exporter.export_mermaid(output_path)
    elif format_ == "neo4j":
        exporter.export_neo4j(output_path)
    elif format_ == "json":
        exporter.export_json(output_path)
    else:
        raise ValueError(f"Unsupported format: {format_}")