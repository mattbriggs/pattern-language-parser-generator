"""Unit tests for the pattern extractor."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pattern_language_miner.extractor.pattern_extractor import PatternExtractor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_config(tmp_path: Path, **overrides) -> Path:
    """Write an extraction config with optional field overrides."""
    defaults = dict(
        file_type="txt",
        frequency_threshold=1,
        minimum_token_count=1,
        scope="sentence",
        pos_filtering=False,
        allowed_pos_tags=[],
        block_elements=[],
        ngram_min=2,
        ngram_max=3,
    )
    defaults.update(overrides)
    config = tmp_path / "config.yaml"
    config.write_text(
        yaml.dump({"pattern_extraction": defaults}), encoding="utf-8"
    )
    return config


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPatternExtractor:
    def test_extraction_produces_yaml_files(self, tmp_path):
        config = make_config(tmp_path)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        (input_dir / "a.txt").write_text(
            "Install the package to get started. "
            "Install the package before continuing.",
            encoding="utf-8",
        )

        extractor = PatternExtractor(config, input_dir, output_dir)
        extractor.run()

        files = list(output_dir.glob("*.yaml"))
        assert files, "Expected at least one YAML output file."

    def test_yaml_files_have_pattern_and_frequency(self, tmp_path):
        config = make_config(tmp_path)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        (input_dir / "a.txt").write_text(
            "Install the package. Install the package.", encoding="utf-8"
        )

        PatternExtractor(config, input_dir, output_dir).run()

        for path in output_dir.glob("*.yaml"):
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            assert "pattern" in data
            assert "frequency" in data

    def test_empty_input_dir_produces_no_files(self, tmp_path):
        config = make_config(tmp_path)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"

        PatternExtractor(config, input_dir, output_dir).run()

        assert list(output_dir.glob("*.yaml")) == []

    def test_frequency_threshold_respected(self, tmp_path):
        config = make_config(tmp_path, frequency_threshold=3)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        # Phrase appears only twice → should be filtered out.
        (input_dir / "a.txt").write_text(
            "install package. install package.", encoding="utf-8"
        )

        PatternExtractor(config, input_dir, output_dir).run()

        assert list(output_dir.glob("*.yaml")) == []

    def test_minimum_token_count_respected(self, tmp_path):
        # minimum_token_count=5 means sentences shorter than 5 tokens are skipped.
        config = make_config(tmp_path, minimum_token_count=5, frequency_threshold=1)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        # Very short sentences — all below 5 tokens.
        (input_dir / "a.txt").write_text("Hi. Ok. Yes.", encoding="utf-8")

        PatternExtractor(config, input_dir, output_dir).run()

        assert list(output_dir.glob("*.yaml")) == []

    def test_scope_line(self, tmp_path):
        config = make_config(tmp_path, scope="line", frequency_threshold=1)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        (input_dir / "a.txt").write_text(
            "install the package here\ninstall the package there",
            encoding="utf-8",
        )

        PatternExtractor(config, input_dir, output_dir).run()

        assert list(output_dir.glob("*.yaml")), "Expected patterns from line scope."

    def test_output_dir_created_automatically(self, tmp_path):
        config = make_config(tmp_path)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "deep" / "nested" / "output"

        extractor = PatternExtractor(config, input_dir, output_dir)
        assert output_dir.exists()

    def test_markdown_file_type(self, tmp_path):
        config = make_config(tmp_path, file_type="md")
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        (input_dir / "doc.md").write_text(
            "Install the package here. Install the package there.",
            encoding="utf-8",
        )

        PatternExtractor(config, input_dir, output_dir).run()

        assert list(output_dir.glob("*.yaml"))

    def test_extract_patterns_returns_sorted_list(self, tmp_path):
        config = make_config(tmp_path, frequency_threshold=1)
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        # "install package" appears 3x, "delete file" appears 1x.
        (input_dir / "a.txt").write_text(
            "install package install package install package delete file.",
            encoding="utf-8",
        )

        extractor = PatternExtractor(config, input_dir, output_dir)
        docs = extractor._load_documents()
        patterns = extractor.extract_patterns(docs)

        freqs = [p["frequency"] for p in patterns]
        assert freqs == sorted(freqs, reverse=True)
