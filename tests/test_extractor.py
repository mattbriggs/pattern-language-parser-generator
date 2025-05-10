import pytest
from pattern_language_miner.extractor.pattern_extractor import PatternExtractor


def test_extract_lexical_patterns_minimal_input():
    extractor = PatternExtractor()
    documents = ["This is a test sentence. Another test sentence is here."]
    patterns = extractor.extract_lexical_patterns(documents)

    assert isinstance(patterns, list)
    assert all("pattern" in p and "frequency" in p for p in patterns)
    assert any("test sentence" in p["pattern"] for p in patterns)


def test_extract_lexical_patterns_multiple_documents():
    extractor = PatternExtractor()
    documents = [
        "Pattern recognition is key to understanding.",
        "Pattern recognition involves identifying repeated elements.",
        "Repeated elements can form a structure."
    ]
    patterns = extractor.extract_lexical_patterns(documents)

    assert isinstance(patterns, list)
    assert all(isinstance(p["pattern"], str) for p in patterns)
    assert all(isinstance(p["frequency"], int) for p in patterns)


def test_extract_lexical_patterns_empty_input():
    extractor = PatternExtractor()
    patterns = extractor.extract_lexical_patterns([])

    assert isinstance(patterns, list)
    assert len(patterns) == 0