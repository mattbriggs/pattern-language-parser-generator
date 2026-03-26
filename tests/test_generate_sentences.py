"""Unit tests for sentence generators (both generator and transform modules)."""

from __future__ import annotations

import yaml
import pytest
from pathlib import Path

from pattern_language_miner.generator.generate_sentences import SentenceGenerator
from pattern_language_miner.transform.generate_sentences import (
    SentenceGenerator as TransformSentenceGenerator,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def pattern_files(tmp_path: Path) -> Path:
    """Create two YAML pattern files with all required fields."""
    data = [
        {
            "id": "pattern-1",
            "problem": "remove orphaned containers",
            "context": "container cleanup",
            "solution": "Restart with Docker Compose",
            "example": "docker compose down -v",
        },
        {
            "id": "pattern-2",
            "problem": "rebuild container image",
            "context": "development environment",
            "solution": "Run docker compose build",
            "example": "docker compose build",
        },
    ]
    for i, pattern in enumerate(data, start=1):
        path = tmp_path / f"pattern-{i}.yaml"
        with path.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(pattern, fh)
    return tmp_path


# ---------------------------------------------------------------------------
# generator.SentenceGenerator
# ---------------------------------------------------------------------------


class TestGeneratorSentenceGenerator:
    def test_text_output_exists(self, tmp_path, pattern_files):
        out = tmp_path / "sentences.txt"
        SentenceGenerator(pattern_files, out, "text").run()
        assert out.exists()

    def test_text_output_has_content(self, tmp_path, pattern_files):
        out = tmp_path / "sentences.txt"
        SentenceGenerator(pattern_files, out, "text").run()
        assert out.read_text(encoding="utf-8").strip()

    def test_markdown_output_numbered(self, tmp_path, pattern_files):
        out = tmp_path / "sentences.md"
        SentenceGenerator(pattern_files, out, "markdown").run()
        content = out.read_text(encoding="utf-8")
        assert "1." in content
        assert "2." in content

    def test_html_output_structure(self, tmp_path, pattern_files):
        out = tmp_path / "sentences.html"
        SentenceGenerator(pattern_files, out, "html").run()
        html = out.read_text(encoding="utf-8")
        assert "<ul" in html
        assert "<li>" in html

    def test_invalid_format_raises(self, tmp_path, pattern_files):
        with pytest.raises(ValueError, match="Unsupported"):
            SentenceGenerator(pattern_files, tmp_path / "x", "pdf")

    def test_empty_input_dir_writes_nothing(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        out = tmp_path / "out.txt"
        SentenceGenerator(empty, out, "text").run()
        assert not out.exists()

    def test_load_patterns_returns_list(self, tmp_path, pattern_files):
        gen = SentenceGenerator(pattern_files, tmp_path / "x.txt", "text")
        patterns = gen.load_patterns()
        assert isinstance(patterns, list)
        assert len(patterns) == 2

    def test_generate_sentence_uses_solution(self, tmp_path):
        gen = SentenceGenerator(tmp_path, tmp_path / "x.txt", "text")
        sentence = gen.generate_sentence({"solution": "do the thing", "context": "ctx"})
        assert "do the thing" in sentence


# ---------------------------------------------------------------------------
# transform.SentenceGenerator
# ---------------------------------------------------------------------------


class TestTransformSentenceGenerator:
    def test_text_output_has_sentences(self, tmp_path, pattern_files):
        out = tmp_path / "out.txt"
        TransformSentenceGenerator(str(pattern_files), str(out), "text").run()
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "remove orphaned containers" in content

    def test_markdown_output(self, tmp_path, pattern_files):
        out = tmp_path / "out.md"
        TransformSentenceGenerator(str(pattern_files), str(out), "markdown").run()
        content = out.read_text(encoding="utf-8")
        assert content.startswith("1.")

    def test_html_output(self, tmp_path, pattern_files):
        out = tmp_path / "out.html"
        TransformSentenceGenerator(str(pattern_files), str(out), "html").run()
        html = out.read_text(encoding="utf-8")
        assert "<ul>" in html
        assert "<li>" in html

    def test_custom_template(self, tmp_path, pattern_files):
        tpl = "Solution: {solution}"
        out = tmp_path / "out.txt"
        TransformSentenceGenerator(
            str(pattern_files), str(out), "text", template=tpl
        ).run()
        content = out.read_text(encoding="utf-8")
        assert "Solution: Restart with Docker Compose" in content
