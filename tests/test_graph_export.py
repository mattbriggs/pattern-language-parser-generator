import tempfile
import networkx as nx
import os
from pattern_language_miner.graph.graph_export import export_graph

def test_export_graph_graphml():
    G = nx.Graph()
    G.add_node("A", label="Alpha")
    G.add_node("B", label="Beta")
    G.add_edge("A", "B", relationship="linked")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".graphml") as tmp:
        output_path = tmp.name

    export_graph(G, output_path, "graphml")

    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "graphml" in content.lower()
    os.remove(output_path)
