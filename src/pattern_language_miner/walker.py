"""Directory walker with parser-factory support.

This module provides two collaborating classes:

- :class:`ParserFactory` — a *Factory Method* that selects the right
  :class:`~pattern_language_miner.parser.base_parser.BaseParser` for a
  given file extension.
- :class:`DirectoryWalker` — recursively traverses a directory tree and
  yields ``(path, content, parser)`` tuples for every supported file.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Generator, Tuple

from .parser.base_parser import BaseParser
from .parser.html_parser import HTMLParser
from .parser.markdown_parser import MarkdownParser
from .parser.text_parser import TextParser

logger = logging.getLogger(__name__)

#: File extensions handled by this package.
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(
    {".txt", ".md", ".markdown", ".html", ".htm"}
)


class ParserFactory:
    """Select the appropriate parser for a given file extension.

    This is an implementation of the *Factory Method* pattern: callers
    ask for a parser by extension without knowing which concrete class
    will be returned.

    Example:
        >>> parser = ParserFactory.get_parser(".md")
        >>> type(parser).__name__
        'MarkdownParser'
    """

    @staticmethod
    def get_parser(file_extension: str) -> BaseParser:
        """Return a parser instance for *file_extension*.

        Args:
            file_extension: The file extension including the leading dot
                (e.g. ``".md"``).  Case is ignored.

        Returns:
            A concrete :class:`~pattern_language_miner.parser.base_parser.BaseParser`
            instance appropriate for the supplied extension.

        Raises:
            ValueError: If *file_extension* is not in
                :data:`SUPPORTED_EXTENSIONS`.
        """
        ext = file_extension.lower()
        if ext in {".md", ".markdown"}:
            return MarkdownParser()
        if ext in {".html", ".htm"}:
            return HTMLParser()
        if ext == ".txt":
            return TextParser()
        raise ValueError(f"Unsupported file extension: {file_extension!r}")


class DirectoryWalker:
    """Recursively walk a directory and yield parseable file contents.

    Only files whose suffix belongs to :data:`SUPPORTED_EXTENSIONS` are
    processed.  Files that cannot be read are logged at WARNING level and
    skipped gracefully.

    Args:
        root_dir: Path to the root directory to scan.

    Example:
        >>> walker = DirectoryWalker("./docs")
        >>> for path, content, parser in walker.walk():
        ...     result = parser.parse(content)
    """

    def __init__(self, root_dir: str | Path) -> None:
        self.root_dir = Path(root_dir)

    def walk(
        self,
    ) -> Generator[Tuple[Path, str, BaseParser], None, None]:
        """Yield ``(file_path, content, parser)`` for every supported file.

        Yields:
            A 3-tuple of:

            - :class:`~pathlib.Path` — absolute path to the file.
            - *str* — raw text content of the file.
            - :class:`~pattern_language_miner.parser.base_parser.BaseParser`
              — the parser appropriate for this file type.
        """
        for file_path in sorted(self.root_dir.rglob("*")):
            if not file_path.is_file():
                continue
            ext = file_path.suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
                parser = ParserFactory.get_parser(ext)
                yield file_path, content, parser
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to read or parse %s: %s", file_path, exc)
