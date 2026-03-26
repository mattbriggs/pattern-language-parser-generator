"""Natural-language sentence generator for pattern YAML files.

Converts structured YAML patterns into human-readable sentences using a
simple grammar template, and writes the result in text, Markdown, or HTML
format.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

import yaml

logger = logging.getLogger(__name__)

#: Output formats supported by :class:`SentenceGenerator`.
SUPPORTED_FORMATS: frozenset[str] = frozenset({"markdown", "html", "text"})


class SentenceGenerator:
    """Convert YAML pattern files into formatted, human-readable sentences.

    The generator applies a simple grammar template of the form::

        To <solution> in the context of <context>, use <solution>.
        For example, <example>.

    Output can be written as plain text, Markdown numbered lists, or an
    HTML unordered list.

    Args:
        input_dir: Directory containing ``*.yaml`` pattern files.
        output_path: File path where the formatted output is written.
        format_: Output format — one of ``"text"``, ``"markdown"``,
            or ``"html"``.

    Raises:
        ValueError: If *format_* is not in :data:`SUPPORTED_FORMATS`.

    Example:
        >>> gen = SentenceGenerator("./enriched", "./output.md", "markdown")
        >>> gen.run()
    """

    def __init__(
        self,
        input_dir: str | Path,
        output_path: str | Path,
        format_: str = "markdown",
    ) -> None:
        self.input_dir = Path(input_dir)
        self.output_path = Path(output_path)
        self.format = format_.lower()

        if self.format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format {self.format!r}. "
                f"Choose from: {', '.join(sorted(SUPPORTED_FORMATS))}"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Execute the full sentence-generation pipeline.

        Loads patterns, generates sentences, formats them, and writes
        the result to :attr:`output_path`.
        """
        logger.info("Loading patterns from %s.", self.input_dir)
        patterns = self.load_patterns()
        if not patterns:
            logger.warning("No patterns found in %s.", self.input_dir)
            return

        logger.info("Generating %d sentence(s).", len(patterns))
        sentences = [self.generate_sentence(p) for p in patterns]
        formatted = self.format_sentences(sentences)
        self.write_output(formatted)

    def load_patterns(self) -> List[Dict]:
        """Load all ``*.yaml`` pattern files from :attr:`input_dir`.

        Returns:
            A list of non-empty pattern dictionaries.
        """
        patterns: List[Dict] = []
        for file_path in sorted(self.input_dir.glob("*.yaml")):
            try:
                with file_path.open("r", encoding="utf-8") as fh:
                    pattern = yaml.safe_load(fh)
                if pattern:
                    patterns.append(pattern)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not parse %s: %s", file_path.name, exc)
        return patterns

    def generate_sentence(self, pattern: Dict) -> str:
        """Apply the grammar template to a single pattern dictionary.

        Args:
            pattern: A pattern dictionary with optional keys ``solution``,
                ``context``, and ``example``.

        Returns:
            A single formatted sentence string.
        """
        solution = pattern.get("solution", "solve the problem")
        context = pattern.get("context", "a general scenario")
        example = pattern.get("example", "no example provided")
        return (
            f"To {solution} in the context of {context}, use {solution}. "
            f"For example, {example}."
        )

    def format_sentences(self, sentences: List[str]) -> str:
        """Format a list of sentences in the configured output format.

        Args:
            sentences: Plain-text sentences to format.

        Returns:
            A single formatted string ready to be written to a file.
        """
        if self.format == "markdown":
            return "\n\n".join(
                f"{i + 1}. {s}" for i, s in enumerate(sentences)
            )
        if self.format == "html":
            items = "".join(f"<li>{s}</li>\n" for s in sentences)
            return f"<ul data-type='generated-patterns'>\n{items}</ul>"
        # Plain text fallback
        return "\n".join(sentences)

    def write_output(self, content: str) -> None:
        """Write *content* to :attr:`output_path`.

        The parent directory is created automatically if it does not exist.

        Args:
            content: Formatted string content to write.
        """
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(content, encoding="utf-8")
        logger.info(
            "Wrote %d line(s) to %s as %s.",
            len(content.splitlines()),
            self.output_path,
            self.format.upper(),
        )
