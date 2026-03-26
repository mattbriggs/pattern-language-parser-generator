"""Unit tests for the graph export module."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import pytest

from pattern_language_miner.graph.graph_export import GraphExporter, export_graph


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_digraph() -> nx.DiGraph:
    g = nx.DiGraph()
    g.add_node("pattern_a", label="Pattern A", type="pattern")
    g.add_node("tag_x", label="Tag X", type="tag")
    g.add_edge("pattern_a", "tag_x", relationship="has_tag")
    return g


# ---------------------------------------------------------------------------
# GraphExporter
# ---------------------------------------------------------------------------


class TestGraphExporter:
    def test_build_graph_adds_nodes(self):
        patterns = [
            {"title": "Install Package", "tags": ["setup"], "concepts": [], "related": []}
        ]
        exporter = GraphExporter(patterns)
        exporter.build_graph()
        assert exporter.graph.number_of_nodes() > 0

    def test_build_graph_adds_tag_edge(self):
        patterns = [{"title": "P", "tags": ["t1"], "concepts": [], "related": []}]
        exporter = GraphExporter(patterns)
        exporter.build_graph()
        edges = list(exporter.graph.edges(data=True))
        assert any(d.get("relationship") == "has_tag" for _, _, d in edges)

    def test_build_graph_adds_concept_edge(self):
        patterns = [{"title": "P", "tags": [], "concepts": ["c1"], "related": []}]
        exporter = GraphExporter(patterns)
        exporter.build_graph()
        edges = list(exporter.graph.edges(data=True))
        assert any(d.get("relationship") == "about" for _, _, d in edges)

    def test_build_graph_adds_related_edge(self):
        patterns = [{"title": "P", "tags": [], "concepts": [], "related": ["Q"]}]
        exporter = GraphExporter(patterns)
        exporter.build_graph()
        edges = list(exporter.graph.edges(data=True))
        assert any(d.get("relationship") == "related_to" for _, _, d in edges)

    def test_export_graphml_creates_file(self, tmp_path):
        exporter = GraphExporter([])
        exporter.graph = make_digraph()
        out = tmp_path / "out.graphml"
        exporter.export_graphml(out)
        assert out.exists()
        assert "graphml" in out.read_text(encoding="utf-8").lower()

    def test_export_mermaid_creates_file(self, tmp_path):
        exporter = GraphExporter([])
        exporter.graph = make_digraph()
        out = tmp_path / "out.mmd"
        exporter.export_mermaid(out)
        content = out.read_text(encoding="utf-8")
        assert content.startswith("graph TD")
        assert "has_tag" in content

    def test_export_neo4j_creates_file(self, tmp_path):
        exporter = GraphExporter([])
        exporter.graph = make_digraph()
        out = tmp_path / "out.cypher"
        exporter.export_neo4j(out)
        content = out.read_text(encoding="utf-8")
        assert "MERGE" in content

    def test_export_json_creates_valid_json(self, tmp_path):
        exporter = GraphExporter([])
        exporter.graph = make_digraph()
        out = tmp_path / "out.json"
        exporter.export_json(out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert "nodes" in data
        assert "links" in data


# ---------------------------------------------------------------------------
# export_graph facade
# ---------------------------------------------------------------------------


class TestExportGraphFacade:
    def test_graphml_format(self, tmp_path):
        g = make_digraph()
        out = tmp_path / "out.graphml"
        export_graph(g, out, "graphml")
        assert out.exists()

    def test_mermaid_format(self, tmp_path):
        g = make_digraph()
        out = tmp_path / "out.mmd"
        export_graph(g, out, "mermaid")
        assert "graph TD" in out.read_text(encoding="utf-8")

    def test_neo4j_format(self, tmp_path):
        g = make_digraph()
        out = tmp_path / "out.cypher"
        export_graph(g, out, "neo4j")
        assert out.exists()

    def test_json_format(self, tmp_path):
        g = make_digraph()
        out = tmp_path / "out.json"
        export_graph(g, out, "json")
        assert out.exists()

    def test_invalid_format_raises(self, tmp_path):
        g = make_digraph()
        with pytest.raises(ValueError, match="Unsupported"):
            export_graph(g, tmp_path / "out.xyz", "invalid_format")

    def test_case_insensitive_format(self, tmp_path):
        g = make_digraph()
        out = tmp_path / "out.graphml"
        export_graph(g, out, "GRAPHML")
        assert out.exists()
