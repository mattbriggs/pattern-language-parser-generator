import tempfile
import shutil
from pathlib import Path
import yaml
import pytest

from pattern_language_miner.enricher.pattern_enricher import (
    enrich_pattern,
    PatternEnricher,
)


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
        "summary": "This is already here."
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


@pytest.fixture
def temp_dirs():
    input_dir = Path(tempfile.mkdtemp())
    output_dir = Path(tempfile.mkdtemp())
    yield input_dir, output_dir
    shutil.rmtree(input_dir)
    shutil.rmtree(output_dir)


def create_yaml_file(directory, filename, content):
    file_path = directory / filename
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(content, f, sort_keys=False, allow_unicode=True)
    return file_path


def test_enricher_adds_problem_field(temp_dirs):
    input_dir, output_dir = temp_dirs
    create_yaml_file(input_dir, "pattern1.yaml", {"solution": "Install Docker."})

    enricher = PatternEnricher(input_dir, output_dir)
    enricher.run()

    enriched_file = output_dir / "pattern1.yaml"
    assert enriched_file.exists()

    with open(enriched_file, "r", encoding="utf-8") as f:
        enriched_data = yaml.safe_load(f)

    assert "problem" in enriched_data
    assert enriched_data["problem"] == "Software is not installed."


def test_enricher_preserves_existing_problem(temp_dirs):
    input_dir, output_dir = temp_dirs
    create_yaml_file(input_dir, "pattern2.yaml", {
        "solution": "Restart the service.",
        "problem": "The service needs to be restarted manually."
    })

    enricher = PatternEnricher(input_dir, output_dir)
    enricher.run()

    enriched_file = output_dir / "pattern2.yaml"
    with open(enriched_file, "r", encoding="utf-8") as f:
        enriched_data = yaml.safe_load(f)

    assert enriched_data["problem"] == "The service needs to be restarted manually."