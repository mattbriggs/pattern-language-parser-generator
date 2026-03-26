"""Template-based sentence generator (transform sub-package).

Provides an alternative :class:`SentenceGenerator` that supports a
user-supplied template string with named placeholders.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

import yaml

logger = logging.getLogger(__name__)

#: Default sentence template matching the four required pattern fields.
DEFAULT_TEMPLATE = (
    "To {problem} in the context of {context}, "
    "use {solution}. For example, {example}."
)

#: Fields that every pattern must contain to be rendered with the template.
REQUIRED_FIELDS = frozenset({"problem", "context", "solution", "example"})


class SentenceGenerator:
    """Convert pattern YAML files to sentences via a configurable template.

    Unlike the generator in :mod:`pattern_language_miner.generator`, this
    implementation supports a fully customisable template string.

    Args:
        input_dir: Directory containing ``pattern-*.yaml`` files.
        output_path: Destination file for generated sentences.
        format_: Output format — ``"text"``, ``"markdown"``, or ``"html"``.
        template: Template string with ``{problem}``, ``{context}``,
            ``{solution}``, and ``{example}`` placeholders.

    Example:
        >>> gen = SentenceGenerator("./patterns", "./output.txt", "text")
        >>> gen.run()
    """

    def __init__(
        self,
        input_dir: str,
        output_path: str,
        format_: str = "text",
        template: Optional[str] = None,
    ) -> None:
        self.input_dir = Path(input_dir)
        self.output_path = Path(output_path)
        self.format = format_.lower()
        self.template = template or DEFAULT_TEMPLATE

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Execute the sentence generation pipeline.

        Loads patterns, generates sentences, and writes output.
        """
        patterns = self.load_patterns()
        sentences = self.generate_sentences(patterns)
        self.save_output(sentences)
        logger.info(
            "Wrote %d sentence(s) to %s as %s.",
            len(sentences),
            self.output_path,
            self.format.upper(),
        )

    def load_patterns(self) -> List[dict]:
        """Load pattern files that contain all required template fields.

        Returns:
            A list of pattern dicts that have all of
            :data:`REQUIRED_FIELDS`.
        """
        patterns: List[dict] = []
        for file_path in sorted(self.input_dir.glob("pattern-*.yaml")):
            try:
                with file_path.open("r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh)
                if data and REQUIRED_FIELDS.issubset(data):
                    patterns.append(data)
            except yaml.YAMLError as exc:
                logger.warning("Skipping %s: %s", file_path.name, exc)
        return patterns

    def generate_sentences(self, patterns: List[dict]) -> List[str]:
        """Apply :attr:`template` to each pattern in *patterns*.

        Args:
            patterns: List of pattern dicts containing the template fields.

        Returns:
            A list of formatted sentence strings.
        """
        return [
            self.template.format(
                problem=pat["problem"],
                context=pat["context"],
                solution=pat["solution"],
                example=pat["example"],
            )
            for pat in patterns
        ]

    def save_output(self, sentences: List[str]) -> None:
        """Write *sentences* to :attr:`output_path`.

        Args:
            sentences: Formatted sentences to write.
        """
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.format == "markdown":
            content = "".join(
                f"{i}. {s}\n\n" for i, s in enumerate(sentences, start=1)
            )
        elif self.format == "html":
            items = "".join(f"  <li>{s}</li>\n" for s in sentences)
            content = f"<ul>\n{items}</ul>\n"
        else:
            content = "".join(
                f"{i}. {s}\n" for i, s in enumerate(sentences, start=1)
            )

        self.output_path.write_text(content, encoding="utf-8")
