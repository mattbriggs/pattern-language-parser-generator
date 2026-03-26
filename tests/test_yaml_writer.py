"""Unit tests for YamlWriter."""

from __future__ import annotations

import yaml
import pytest
from pathlib import Path

from pattern_language_miner.writer.yaml_writer import YamlWriter


@pytest.fixture()
def sample_patterns():
    return [
        {"title": "Install Docker", "solution": "Use apt-get install docker"},
        {"solution": "Use Docker Compose", "context": "Development"},
        {"title": "Restart Container", "example": "docker restart container"},
    ]


class TestYamlWriter:
    def test_creates_correct_number_of_files(self, tmp_path, sample_patterns):
        YamlWriter(tmp_path).write(sample_patterns)
        assert len(list(tmp_path.glob("*.yaml"))) == len(sample_patterns)

    def test_files_are_valid_yaml(self, tmp_path, sample_patterns):
        YamlWriter(tmp_path).write(sample_patterns)
        for path in sorted(tmp_path.glob("*.yaml")):
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            assert isinstance(data, dict)

    def test_files_contain_original_keys(self, tmp_path, sample_patterns):
        YamlWriter(tmp_path).write(sample_patterns)
        for path in sorted(tmp_path.glob("*.yaml")):
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            assert any(
                k in data for k in ("title", "solution", "context", "example")
            )

    def test_sanitizes_special_chars(self, tmp_path):
        writer = YamlWriter(tmp_path)
        writer.write([{"title": "Hello: World!@#"}])
        filenames = [f.name for f in tmp_path.glob("*.yaml")]
        assert "001-hello-world.yaml" in filenames

    def test_sanitizes_multiple_spaces(self, tmp_path):
        YamlWriter(tmp_path).write([{"title": "  Multiple     Spaces  "}])
        filenames = [f.name for f in tmp_path.glob("*.yaml")]
        assert "001-multiple-spaces.yaml" in filenames

    def test_fallback_filename_for_empty_title(self, tmp_path):
        YamlWriter(tmp_path).write([{"title": ""}])
        filenames = [f.name for f in tmp_path.glob("*.yaml")]
        assert "001-pattern.yaml" in filenames

    def test_fallback_to_solution_when_no_title(self, tmp_path):
        YamlWriter(tmp_path).write([{"solution": "fallback-name"}])
        filenames = [f.name for f in tmp_path.glob("*.yaml")]
        assert "001-fallback-name.yaml" in filenames

    def test_sequential_numbering(self, tmp_path):
        patterns = [{"title": f"Pattern {i}"} for i in range(1, 4)]
        YamlWriter(tmp_path).write(patterns)
        names = sorted(f.name for f in tmp_path.glob("*.yaml"))
        assert names[0].startswith("001-")
        assert names[1].startswith("002-")
        assert names[2].startswith("003-")

    def test_output_dir_created_automatically(self, tmp_path):
        out = tmp_path / "new" / "nested" / "dir"
        YamlWriter(out).write([{"title": "x"}])
        assert out.exists()

    def test_sanitize_filename_method(self, tmp_path):
        writer = YamlWriter(tmp_path)
        assert writer.sanitize_filename("Hello World!") == "hello-world"
        assert writer.sanitize_filename("") == "pattern"
        assert writer.sanitize_filename("  ") == "pattern"
