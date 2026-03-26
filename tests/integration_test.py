"""End-to-end integration tests for the Pattern Language Miner pipeline."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest
import yaml

from pattern_language_miner.enricher.pattern_enricher import PatternEnricher
from pattern_language_miner.extractor.pattern_extractor import PatternExtractor
from pattern_language_miner.generator.generate_sentences import SentenceGenerator
from pattern_language_miner.output.yaml_writer import YAMLWriter
from pattern_language_miner.walker import DirectoryWalker


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_directory_with_files():
    """Temporary directory with text, Markdown, and HTML sample files."""
    temp_dir = Path(tempfile.mkdtemp())

    files = {
        "example.txt": (
            "This is a sample sentence. This is another sample sentence."
        ),
        "example.md": (
            "# Heading\n\nSome repeated text here. Some repeated text here."
        ),
        "example.html": (
            "<html><body><p>HTML content repeated. "
            "HTML content repeated.</p></body></html>"
        ),
    }
    for filename, content in files.items():
        (temp_dir / filename).write_text(content, encoding="utf-8")

    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture()
def extraction_config(tmp_path: Path) -> Path:
    config = tmp_path / "config.yaml"
    config.write_text(
        """
pattern_extraction:
  file_type: md
  frequency_threshold: 1
  minimum_token_count: 1
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  ngram_min: 2
  ngram_max: 4
""",
        encoding="utf-8",
    )
    return config


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_integration_extraction_and_yaml(
    sample_directory_with_files, extraction_config, tmp_path
):
    """Full extraction pipeline: documents → YAML patterns."""
    output_dir = tmp_path / "patterns"

    extractor = PatternExtractor(
        config_path=extraction_config,
        input_dir=sample_directory_with_files,
        output_dir=output_dir,
    )
    extractor.run()

    output_files = list(output_dir.glob("*.yaml"))
    assert output_files, "Expected at least one extracted pattern YAML file."

    for path in output_files:
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        assert "pattern" in data
        assert "frequency" in data


def test_integration_extraction_and_enrichment(extraction_config, tmp_path):
    """Extraction → enrichment pipeline produces enriched YAML with metadata."""
    input_dir = tmp_path / "docs"
    input_dir.mkdir()
    (input_dir / "guide.md").write_text(
        "Install the package to begin. Install the package now.",
        encoding="utf-8",
    )
    raw_dir = tmp_path / "raw"
    enriched_dir = tmp_path / "enriched"

    PatternExtractor(extraction_config, input_dir, raw_dir).run()
    assert list(raw_dir.glob("*.yaml")), "No patterns extracted."

    PatternEnricher(raw_dir, enriched_dir).run()

    for path in enriched_dir.glob("*.yaml"):
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        assert "keywords" in data


def test_integration_walker_finds_files(sample_directory_with_files):
    """DirectoryWalker correctly discovers and parses all supported file types."""
    results = list(DirectoryWalker(sample_directory_with_files).walk())
    extensions = {r[0].suffix.lower() for r in results}
    assert ".txt" in extensions
    assert ".md" in extensions
    assert ".html" in extensions


def test_integration_sentence_generation(tmp_path):
    """Enriched YAML → readable sentences pipeline."""
    patterns_dir = tmp_path / "patterns"
    patterns_dir.mkdir()

    pattern_data = [
        {
            "problem": "remove orphaned containers",
            "context": "container cleanup",
            "solution": "restart with Docker Compose",
            "example": "docker compose down -v",
        },
        {
            "problem": "rebuild image",
            "context": "development",
            "solution": "run docker compose build",
            "example": "docker compose build",
        },
    ]
    for i, p in enumerate(pattern_data, start=1):
        (patterns_dir / f"pattern-{i}.yaml").write_text(
            yaml.dump(p), encoding="utf-8"
        )

    out_md = tmp_path / "output.md"
    SentenceGenerator(patterns_dir, out_md, "markdown").run()

    assert out_md.exists()
    content = out_md.read_text(encoding="utf-8")
    assert "1." in content
    assert "restart with Docker Compose" in content


def test_integration_yaml_writer_round_trip(tmp_path):
    """YAMLWriter writes patterns that can be loaded back correctly."""
    patterns = {
        "p001.yaml": {"id": "P-001", "solution": "install package"},
        "p002.yaml": {"id": "P-002", "solution": "restart service"},
    }
    writer = YAMLWriter(output_dir=str(tmp_path))
    writer.write_patterns(patterns)

    for filename, expected in patterns.items():
        loaded = yaml.safe_load((tmp_path / filename).read_text(encoding="utf-8"))
        assert loaded["id"] == expected["id"]
        assert loaded["solution"] == expected["solution"]
