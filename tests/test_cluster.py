"""Unit tests for PatternClusterer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from pattern_language_miner.cluster.pattern_cluster import PatternClusterer


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def temp_pattern_dir(tmp_path: Path) -> Path:
    """Create six YAML pattern files with a 'solution' field."""
    for i in range(1, 7):
        (tmp_path / f"pattern-{i}.yaml").write_text(
            yaml.dump({"id": f"pattern-{i}", "solution": f"Use docker pattern {i}"}),
            encoding="utf-8",
        )
    return tmp_path


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_load_patterns(temp_pattern_dir):
    """All six patterns are loaded and each has a 'solution' field."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    assert len(clusterer.patterns) == 6
    assert all("solution" in p for p in clusterer.patterns)


def test_load_patterns_skips_missing_field(tmp_path):
    """Patterns that lack the target field are not loaded."""
    (tmp_path / "p.yaml").write_text(
        yaml.dump({"id": "x", "context": "no solution here"}), encoding="utf-8"
    )
    clusterer = PatternClusterer(input_dir=tmp_path, field="solution")
    clusterer.load_patterns()
    assert clusterer.patterns == []


def test_embedding_and_clustering(temp_pattern_dir):
    """Embeddings have correct shape and clustering returns expected arrays."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    assert embeddings.shape[0] == 6
    assert reduced.shape == (6, 2)
    assert len(cluster_ids) == 6


def test_cluster_count_clamped_when_exceeds_samples(temp_pattern_dir):
    """n_clusters is automatically reduced when it exceeds sample count."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    # Request more clusters than samples.
    _, cluster_ids = clusterer.cluster_and_reduce(embeddings, n_clusters=100)
    assert len(set(cluster_ids.tolist())) <= 6


def test_visualize_clusters_creates_png(tmp_path, temp_pattern_dir):
    """visualize_clusters writes a PNG file."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    out = tmp_path / "clusters.png"
    clusterer.visualize_clusters(reduced, cluster_ids, out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_generate_cluster_report_creates_json(tmp_path, temp_pattern_dir):
    """generate_cluster_report writes a valid JSON file with cluster IDs."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    _, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    out = tmp_path / "report.json"
    clusterer.generate_cluster_report(cluster_ids, out)

    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 6
    assert all("cluster" in entry for entry in data)


def test_generate_cluster_report_cluster_ids_are_ints(tmp_path, temp_pattern_dir):
    """Cluster IDs in the JSON report are plain Python ints, not numpy.int64."""
    clusterer = PatternClusterer(input_dir=temp_pattern_dir, field="solution")
    clusterer.load_patterns()
    embeddings = clusterer.embed_patterns()
    _, cluster_ids = clusterer.cluster_and_reduce(embeddings)

    out = tmp_path / "report.json"
    clusterer.generate_cluster_report(cluster_ids, out)
    data = json.loads(out.read_text(encoding="utf-8"))
    for entry in data:
        assert isinstance(entry["cluster"], int)
