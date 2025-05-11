import os
import yaml
import pytest
from pathlib import Path
from pattern_language_miner.writer.yaml_writer import YamlWriter


@pytest.fixture
def sample_patterns():
    return [
        {"title": "Install Docker", "solution": "Use apt-get install docker"},
        {"solution": "Use Docker Compose", "context": "Development"},
        {"title": "Restart Container", "example": "docker restart container"},
    ]


def test_yaml_writer_creates_files(tmp_path, sample_patterns):
    writer = YamlWriter(output_dir=tmp_path)
    writer.write(sample_patterns)

    files = list(tmp_path.glob("*.yaml"))
    assert len(files) == len(sample_patterns)

    for file_path in files:
        assert file_path.exists()
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            assert isinstance(data, dict)
            assert any(key in data for key in ["title", "solution", "context", "example"])


def test_yaml_writer_sanitizes_filenames(tmp_path):
    patterns = [
        {"title": "Hello: World!@#"},
        {"title": "  Multiple     Spaces  "},
        {"title": ""},
        {"solution": "fallback-name"}
    ]

    writer = YamlWriter(output_dir=tmp_path)
    writer.write(patterns)

    filenames = [f.name for f in tmp_path.glob("*.yaml")]
    assert "001-hello-world.yaml" in filenames
    assert "002-multiple-spaces.yaml" in filenames
    assert "003-pattern.yaml" in filenames  # fallback for empty title
    assert "004-fallback-name.yaml" in filenames
