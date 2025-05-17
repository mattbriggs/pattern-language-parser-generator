import pytest
from pathlib import Path
import yaml
from pattern_language_miner.extractor.pattern_extractor import PatternExtractor


@pytest.fixture
def default_config(tmp_path):
    config = tmp_path / "config.yml"
    config.write_text("""
pattern_extraction:
  frequency_threshold: 1
  minimum_token_count: 1
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  file_type: txt
  ngram_min: 2
  ngram_max: 3
""")
    return config


def test_valid_config_pattern_extractor(tmp_path):
    config = tmp_path / "config.yml"
    config.write_text("""
pattern_extraction:
  frequency_threshold: 1
  minimum_token_count: 1
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  file_type: md
  ngram_min: 2
  ngram_max: 3
""")

    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    (input_dir / "test.md").write_text("Install the package to get started.")

    extractor = PatternExtractor(config_path=config, input_dir=input_dir, output_dir=output_dir)
    extractor.run()

    results = list(output_dir.glob("*.yaml"))
    assert results
    for path in results:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            assert "pattern" in data
            assert "frequency" in data


def test_extract_patterns_minimal_input(tmp_path, default_config):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    input_file = input_dir / "sample.txt"
    input_file.write_text("This is a test sentence. Another test sentence.")

    output_dir = tmp_path / "output"

    extractor = PatternExtractor(config_path=default_config, input_dir=input_dir, output_dir=output_dir)
    extractor.run()

    output_files = list(output_dir.glob("*.yaml"))
    assert len(output_files) > 0


def test_extract_patterns_empty_input(tmp_path, default_config):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    output_dir = tmp_path / "output"

    extractor = PatternExtractor(config_path=default_config, input_dir=input_dir, output_dir=output_dir)
    extractor.run()

    output_files = list(output_dir.glob("*.yaml"))
    assert len(output_files) == 0


def test_extract_patterns_with_token_threshold(tmp_path):
    config = tmp_path / "config.yml"
    config.write_text("""
pattern_extraction:
  frequency_threshold: 1
  minimum_token_count: 5
  scope: sentence
  pos_filtering: false
  allowed_pos_tags: []
  block_elements: []
  file_type: txt
  ngram_min: 2
  ngram_max: 3
""")

    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "short.txt").write_text("Short one. And another.")

    output_dir = tmp_path / "output"

    extractor = PatternExtractor(config_path=config, input_dir=input_dir, output_dir=output_dir)
    extractor.run()

    output_files = list(output_dir.glob("*.yaml"))
    assert len(output_files) == 0