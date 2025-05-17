import os
import shutil
import tempfile
from pathlib import Path

import pytest

from pattern_language_miner.walker import DirectoryWalker
from pattern_language_miner.extractor.pattern_extractor import PatternExtractor
from pattern_language_miner.output.yaml_writer import YAMLWriter


@pytest.fixture
def sample_directory_with_files():
    """
    Creates a temporary directory with sample text, markdown, and HTML files.
    """
    temp_dir = tempfile.mkdtemp()

    files = {
        "example.txt": "This is a sample sentence. This is another sample sentence.",
        "example.md": "# Heading\n\nSome repeated text here. Some repeated text here.",
        "example.html": (
            "<html><body><p>HTML content repeated. HTML content repeated.</p></body></html>"
        ),
    }

    for filename, content in files.items():
        with open(os.path.join(temp_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)

    yield temp_dir

    shutil.rmtree(temp_dir)


def test_integration_extraction_and_yaml(sample_directory_with_files):
    """
    Runs end-to-end test from extraction to YAML output using valid config.
    """
    output_dir = Path(tempfile.mkdtemp())
    input_dir = Path(sample_directory_with_files)
    config_path = Path("tests/data/config_valid.yaml")

    extractor = PatternExtractor(
        config_path=config_path,
        input_dir=input_dir,
        output_dir=output_dir,
    )
    extractor.run()

    # Check that YAML files were generated
    output_files = list(output_dir.glob("*.yaml"))
    assert output_files, "No patterns were extracted and saved."

    # Clean up after test
    shutil.rmtree(output_dir)