import os
import yaml
import pytest
from pathlib import Path
from pattern_language_miner.transform.generate_sentences import SentenceGenerator


@pytest.fixture
def pattern_files(tmp_path):
    """Create temporary YAML pattern files with required fields."""
    data = [
        {
            "id": "pattern-1",
            "problem": "remove orphaned containers",
            "context": "container cleanup",
            "solution": "Restart with Docker Compose",
            "example": "docker compose down -v"
        },
        {
            "id": "pattern-2",
            "problem": "rebuild container image",
            "context": "development environment",
            "solution": "Run docker compose build",
            "example": "docker compose build"
        }
    ]
    for i, pattern in enumerate(data, 1):
        file_path = tmp_path / f"pattern-{i}.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(pattern, f)
    return tmp_path


def test_generate_text_file(tmp_path, pattern_files):
    output_file = tmp_path / "sentences.txt"
    generator = SentenceGenerator(
        input_dir=pattern_files,
        output_path=output_file,
        format_="text"
    )
    generator.run()

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) >= 2
        assert "To remove orphaned containers" in lines[0]


def test_generate_markdown_file(tmp_path, pattern_files):
    output_file = tmp_path / "sentences.md"
    generator = SentenceGenerator(
        input_dir=pattern_files,
        output_path=output_file,
        format_="markdown"
    )
    generator.run()

    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.startswith("1. To remove orphaned containers")
    assert content.count("docker compose") >= 2


def test_generate_html_file(tmp_path, pattern_files):
    output_file = tmp_path / "sentences.html"
    generator = SentenceGenerator(
        input_dir=pattern_files,
        output_path=output_file,
        format_="html"
    )
    generator.run()

    assert output_file.exists()
    html = output_file.read_text(encoding="utf-8")
    assert html.startswith("<ul>")
    assert "<li>" in html and "docker compose down -v" in html
