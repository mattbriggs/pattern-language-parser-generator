"""Lexical n-gram pattern extractor.

This module provides :class:`PatternExtractor`, which scans a directory of
documents, tokenises the text with NLTK, and discovers frequently recurring
n-gram patterns.  Results are serialised as individual YAML files in the
configured output directory.
"""

from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import nltk
import yaml

from pattern_language_miner.utils.config_validation import load_and_validate_config

# Ensure required NLTK data is present at import time.
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

logger = logging.getLogger(__name__)

#: Path to the bundled JSON Schema for configuration validation.
_CONFIG_SCHEMA = Path(__file__).parent.parent / "schema" / "config_schema.json"


class PatternExtractor:
    """Extract frequent lexical n-gram patterns from a document corpus.

    Configuration is loaded from a YAML file and validated against the
    bundled JSON Schema (``schema/config_schema.json``).

    Args:
        config_path: Path to the YAML configuration file.
        input_dir: Directory containing source documents to analyse.
        output_dir: Directory where extracted pattern YAML files are written.
            Created automatically if it does not exist.

    Example:
        >>> extractor = PatternExtractor(
        ...     config_path=Path("config.yaml"),
        ...     input_dir=Path("./docs"),
        ...     output_dir=Path("./patterns"),
        ... )
        >>> extractor.run()
    """

    def __init__(
        self,
        config_path: Path,
        input_dir: Path,
        output_dir: Path,
    ) -> None:
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        config = load_and_validate_config(
            Path(config_path), _CONFIG_SCHEMA
        )["pattern_extraction"]

        self.file_type: str = config.get("file_type", "md")
        self.frequency_threshold: int = config.get("frequency_threshold", 3)
        self.minimum_token_count: int = config.get("minimum_token_count", 2)
        self.scope: str = config.get("scope", "sentence")
        self.pos_filtering: bool = config.get("pos_filtering", False)
        self.allowed_pos_tags: frozenset[str] = frozenset(
            config.get("allowed_pos_tags", [])
        )
        self.block_elements: frozenset[str] = frozenset(
            config.get("block_elements", [])
        )
        self.ngram_min: int = config.get("ngram_min", 2)
        self.ngram_max: int = config.get("ngram_max", 5)

        logger.debug(
            "PatternExtractor initialised: scope=%s, ngram=%d-%d, threshold=%d",
            self.scope,
            self.ngram_min,
            self.ngram_max,
            self.frequency_threshold,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Execute the full extraction pipeline.

        Loads documents, extracts n-gram patterns, and writes YAML output
        files to :attr:`output_dir`.
        """
        logger.info("Starting pattern extraction from %s", self.input_dir)
        documents = self._load_documents()
        patterns = self.extract_patterns(documents)
        self._write_patterns(patterns)

    def extract_patterns(self, documents: List[str]) -> List[Dict[str, Any]]:
        """Extract frequent lexical n-grams from *documents*.

        Args:
            documents: List of raw text strings to analyse.

        Returns:
            A list of pattern dictionaries, each with ``pattern`` and
            ``frequency`` keys, sorted by descending frequency.
        """
        ngrams_counter: Counter = Counter()

        for doc in documents:
            for scope_text in self._split_scope(doc):
                for sentence in nltk.sent_tokenize(scope_text):
                    tokens = nltk.word_tokenize(sentence.lower())

                    min_length = max(self.ngram_min, self.minimum_token_count)
                    if len(tokens) < min_length:
                        continue

                    if self.pos_filtering:
                        pos_tags = nltk.pos_tag(tokens)
                        if not all(
                            tag in self.allowed_pos_tags for _, tag in pos_tags
                        ):
                            continue

                    max_n = min(len(tokens), self.ngram_max)
                    for n in range(self.ngram_min, max_n + 1):
                        for gram in nltk.ngrams(tokens, n):
                            ngrams_counter[" ".join(gram)] += 1

        patterns = [
            {"pattern": ngram, "frequency": freq}
            for ngram, freq in ngrams_counter.items()
            if freq >= self.frequency_threshold
        ]

        result = sorted(patterns, key=lambda x: -x["frequency"])
        logger.info("Extracted %d pattern(s) meeting frequency threshold", len(result))
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_documents(self) -> List[str]:
        """Read all files with the configured extension from *input_dir*.

        Returns:
            A list of raw document strings.
        """
        docs: List[str] = []
        for path in sorted(self.input_dir.rglob(f"*.{self.file_type}")):
            try:
                docs.append(path.read_text(encoding="utf-8"))
            except OSError as exc:
                logger.warning("Could not read %s: %s", path.name, exc)
        logger.debug("Loaded %d document(s) from %s", len(docs), self.input_dir)
        return docs

    def _split_scope(self, doc: str) -> List[str]:
        """Divide a document into analysis units based on :attr:`scope`.

        Args:
            doc: Full document text.

        Returns:
            A list of text segments to tokenise independently.
        """
        if self.scope == "line":
            return [line for line in doc.splitlines() if line.strip()]
        if self.scope == "sentence":
            return nltk.sent_tokenize(doc)
        if self.scope == "block":
            return self._split_blocks(doc)
        return [doc]

    def _split_blocks(self, doc: str) -> List[str]:
        """Split *doc* into paragraph blocks separated by blank lines.

        Args:
            doc: Full document text.

        Returns:
            A list of non-empty paragraph strings, or the whole document
            wrapped in a list if ``"paragraph"`` is not in
            :attr:`block_elements`.
        """
        paragraphs = [p.strip() for p in doc.split("\n\n") if p.strip()]
        return paragraphs if "paragraph" in self.block_elements else [doc]

    def _write_patterns(self, patterns: List[Dict[str, Any]]) -> None:
        """Write each pattern to its own YAML file in :attr:`output_dir`.

        Files are named ``pattern-00001.yaml``, ``pattern-00002.yaml``, etc.

        Args:
            patterns: List of pattern dictionaries to serialise.
        """
        for idx, pattern in enumerate(patterns, start=1):
            file_path = self.output_dir / f"pattern-{idx:05d}.yaml"
            with file_path.open("w", encoding="utf-8") as fh:
                yaml.dump(pattern, fh, allow_unicode=True)
        logger.info("Saved %d pattern(s) to %s", len(patterns), self.output_dir)
