"""Shared pytest fixtures for the Pattern Language Miner test suite."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Config fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def base_config(tmp_path: Path) -> Path:
    """Write a minimal valid extraction config and return its path."""
    config = tmp_path / "config.yaml"
    config.write_text(
        """
pattern_extraction:
  file_type: txt
  frequency_threshold: 1
  minimum_token_count: 1
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  ngram_min: 2
  ngram_max: 3
""",
        encoding="utf-8",
    )
    return config


# ---------------------------------------------------------------------------
# Directory / file fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_input_dir(tmp_path: Path) -> Path:
    """Create a directory with one .txt file containing repeated phrases."""
    d = tmp_path / "input"
    d.mkdir()
    (d / "doc1.txt").write_text(
        "Install the package to get started. "
        "Install the package before continuing. "
        "Always install the package first.",
        encoding="utf-8",
    )
    return d


@pytest.fixture()
def sample_yaml_patterns(tmp_path: Path) -> Path:
    """Create a directory with three enriched YAML pattern files."""
    d = tmp_path / "patterns"
    d.mkdir()

    patterns = [
        {
            "solution": "install the package",
            "context": "software setup",
            "problem": "package is missing",
            "example": "apt-get install vim",
            "title": "Install Package",
            "summary": "Guides the user through installation.",
            "keywords": ["install", "package"],
        },
        {
            "solution": "restart the service",
            "context": "service management",
            "problem": "service is unresponsive",
            "example": "systemctl restart nginx",
            "title": "Restart Service",
            "summary": "Restarts a system service.",
            "keywords": ["restart", "service"],
        },
        {
            "solution": "delete the file",
            "context": "file management",
            "problem": "file is no longer needed",
            "example": "rm -f old_file.txt",
            "title": "Delete File",
            "summary": "Removes an unwanted file.",
            "keywords": ["delete", "file"],
        },
    ]
    for i, p in enumerate(patterns, start=1):
        path = d / f"{i:03d}-pattern.yaml"
        with path.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(p, fh, sort_keys=False, allow_unicode=True)
    return d
