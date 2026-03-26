"""Unit tests for the pattern enricher."""

from __future__ import annotations

import tempfile
import shutil
from pathlib import Path

import pytest
import yaml

from pattern_language_miner.enricher.pattern_enricher import (
    PatternEnricher,
    enrich_pattern,
    extract_keywords,
    infer_problem_from_solution,
)


# ---------------------------------------------------------------------------
# extract_keywords
# ---------------------------------------------------------------------------


class TestExtractKeywords:
    def test_returns_list(self):
        assert isinstance(extract_keywords("install package"), list)

    def test_lower_case(self):
        assert extract_keywords("Install Package") == ["install", "package"]

    def test_deduplication(self):
        result = extract_keywords("install install package")
        assert result.count("install") == 1

    def test_preserves_order(self):
        assert extract_keywords("alpha beta gamma") == ["alpha", "beta", "gamma"]

    def test_hyphenated_token(self):
        assert "apt-get" in extract_keywords("run apt-get install")

    def test_empty_string(self):
        assert extract_keywords("") == []


# ---------------------------------------------------------------------------
# infer_problem_from_solution
# ---------------------------------------------------------------------------


class TestInferProblemFromSolution:
    def test_install_keyword(self):
        assert "install" in infer_problem_from_solution("install the software").lower()

    def test_restart_keyword(self):
        result = infer_problem_from_solution("restart the service")
        assert result

    def test_delete_keyword(self):
        result = infer_problem_from_solution("delete the file")
        assert result

    def test_fallback_unknown(self):
        assert infer_problem_from_solution("do something unusual") == "Unknown problem."


# ---------------------------------------------------------------------------
# enrich_pattern
# ---------------------------------------------------------------------------


def test_enrich_pattern_with_solution_only():
    pattern = {"solution": "Install Docker using apt-get."}
    enriched = enrich_pattern(pattern)
    assert enriched["title"] == "Install docker using apt-get."
    assert "summary" in enriched
    assert enriched["summary"].endswith(".")
    assert enriched["keywords"] == ["install", "docker", "using", "apt-get"]


def test_enrich_pattern_with_existing_title_and_summary():
    pattern = {
        "title": "Existing Title",
        "solution": "Install Docker.",
        "summary": "This is already here.",
    }
    enriched = enrich_pattern(pattern)
    assert enriched["title"] == "Existing Title"
    assert enriched["summary"] == "This is already here."
    assert enriched["keywords"] == ["install", "docker"]


def test_enrich_pattern_with_empty_input():
    pattern = {}
    enriched = enrich_pattern(pattern)
    assert enriched["title"] == "Untitled"
    assert enriched["summary"] == "No solution provided."
    assert enriched["keywords"] == []


def test_enrich_pattern_does_not_mutate_input():
    original = {"solution": "install the package"}
    enrich_pattern(original)
    assert "title" not in original


# ---------------------------------------------------------------------------
# PatternEnricher (batch)
# ---------------------------------------------------------------------------


@pytest.fixture()
def temp_dirs():
    input_dir = Path(tempfile.mkdtemp())
    output_dir = Path(tempfile.mkdtemp())
    yield input_dir, output_dir
    shutil.rmtree(input_dir)
    shutil.rmtree(output_dir)


def _write_yaml(directory: Path, filename: str, content: dict) -> Path:
    file_path = directory / filename
    with file_path.open("w", encoding="utf-8") as fh:
        yaml.dump(content, fh, sort_keys=False, allow_unicode=True)
    return file_path


def test_enricher_adds_problem_field(temp_dirs):
    input_dir, output_dir = temp_dirs
    _write_yaml(input_dir, "pattern1.yaml", {"solution": "Install Docker."})

    PatternEnricher(input_dir, output_dir).run()

    enriched_file = output_dir / "pattern1.yaml"
    assert enriched_file.exists()

    with enriched_file.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    assert "problem" in data
    assert data["problem"] == "Software is not installed."


def test_enricher_preserves_existing_problem(temp_dirs):
    input_dir, output_dir = temp_dirs
    _write_yaml(
        input_dir,
        "pattern2.yaml",
        {
            "solution": "Restart the service.",
            "problem": "The service needs to be restarted manually.",
        },
    )

    PatternEnricher(input_dir, output_dir).run()

    with (output_dir / "pattern2.yaml").open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    assert data["problem"] == "The service needs to be restarted manually."


def test_enricher_creates_output_dir(tmp_path):
    in_dir = tmp_path / "in"
    in_dir.mkdir()
    out = tmp_path / "deep" / "nested"

    PatternEnricher(in_dir, out).run()

    assert out.exists()
