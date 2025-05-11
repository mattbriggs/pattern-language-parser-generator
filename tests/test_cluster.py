import os
import json
import yaml
import pytest
from pathlib import Path
from pattern_language_miner.cluster.pattern_cluster import PatternClusterer


@pytest.fixture
def temp_pattern_dir(tmp_path):
    """Create temporary YAML pattern files for testing."""
    pattern_data = [
        {"id": f"pattern-{i}", "solution": f"Use docker pattern {i}"}
        for i in range(1, 7)  # 6 patterns
    ]
    for i, data in enumerate(pattern_data, 1):
        file_path = tmp_path / f"pattern-{i}.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)
    return tmp_path


def test_load_patterns(temp_pattern_dir):
    """Test that patterns are loaded from YAML files."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    assert len(clusterer.patterns) == 6
    assert all("solution" in p for p in clusterer.patterns)


def test_embedding_and_clustering(temp_pattern_dir):
    """Test that embeddings and clustering run without error."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)
    assert embeddings.shape[0] == 6
    assert reduced.shape[1] == 2
    assert len(cluster_ids) == 6


def test_outputs(tmp_path, temp_pattern_dir):
    """Test output generation: PNG and JSON files."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    os.chdir(output_dir)

    clusterer.visualize_clusters(reduced, cluster_ids, "clusters.png")
    clusterer.generate_cluster_report(cluster_ids, "clustered_patterns.json")

    assert Path("clusters.png").exists()
    assert Path("clustered_patterns.json").exists()

    with open("clustered_patterns.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 6
        assert "cluster" in data[0]
