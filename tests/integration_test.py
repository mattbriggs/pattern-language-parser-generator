import os
import shutil
import tempfile
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
        "example.html": "<html><body><p>HTML content repeated. HTML content repeated.</p></body></html>"
    }

    for filename, content in files.items():
        with open(os.path.join(temp_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)

    yield temp_dir

    shutil.rmtree(temp_dir)


def test_integration_extraction_and_yaml(sample_directory_with_files):
    output_dir = tempfile.mkdtemp()

    walker = DirectoryWalker(sample_directory_with_files)
    extractor = PatternExtractor()
    writer = YAMLWriter(output_dir)

    all_texts = []
    for _, content, parser in walker.walk():
        parsed = parser.parse(content)
        if parsed["type"] == "text":
            all_texts.extend(parsed["lines"])
        else:
            all_texts.append(parsed["html"])

    patterns = extractor.extract_lexical_patterns(all_texts)

    assert isinstance(patterns, list)
    assert all("pattern" in p and "frequency" in p for p in patterns)

    for i, pattern in enumerate(patterns):
        yaml_data = {
            "id": f"pattern-{i+1}",
            "name": pattern["pattern"],
            "level": "chunk",
            "context": "Discovered through frequency analysis.",
            "problem": "Frequent phrasing may signal reusable content.",
            "solution": pattern["pattern"],
            "example": pattern["pattern"],
            "sources": [{"document": "test"}],
            "frequency": pattern["frequency"]
        }
        writer.write_pattern(yaml_data, f"pattern-{i+1}.yaml")

    output_files = os.listdir(output_dir)
    assert any(f.startswith("pattern-") and f.endswith(".yaml") for f in output_files)

    shutil.rmtree(output_dir)