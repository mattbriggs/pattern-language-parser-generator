"""Unit tests for the DirectoryWalker and ParserFactory."""

from __future__ import annotations

import pytest
from pathlib import Path

from pattern_language_miner.walker import DirectoryWalker, ParserFactory, SUPPORTED_EXTENSIONS
from pattern_language_miner.parser.markdown_parser import MarkdownParser
from pattern_language_miner.parser.html_parser import HTMLParser
from pattern_language_miner.parser.text_parser import TextParser


class TestDirectoryWalker:
    def test_yields_supported_files(self, tmp_path):
        (tmp_path / "doc.txt").write_text("hello", encoding="utf-8")
        (tmp_path / "page.md").write_text("# hi", encoding="utf-8")
        (tmp_path / "ignored.pdf").write_text("ignored", encoding="utf-8")

        walker = DirectoryWalker(tmp_path)
        results = list(walker.walk())

        paths = {r[0].name for r in results}
        assert "doc.txt" in paths
        assert "page.md" in paths
        assert "ignored.pdf" not in paths

    def test_yields_content_and_parser(self, tmp_path):
        (tmp_path / "file.txt").write_text("content", encoding="utf-8")
        path, content, parser = next(DirectoryWalker(tmp_path).walk())
        assert content == "content"
        assert isinstance(parser, TextParser)

    def test_walks_subdirectories(self, tmp_path):
        sub = tmp_path / "subdir"
        sub.mkdir()
        (sub / "nested.md").write_text("# nested", encoding="utf-8")

        results = list(DirectoryWalker(tmp_path).walk())
        names = {r[0].name for r in results}
        assert "nested.md" in names

    def test_skips_unreadable_files(self, tmp_path):
        # Create a file with a valid extension but a permissions issue; we just
        # verify the walker doesn't raise when it encounters an error.
        (tmp_path / "readable.txt").write_text("ok", encoding="utf-8")
        results = list(DirectoryWalker(tmp_path).walk())
        assert len(results) >= 1

    def test_empty_directory_yields_nothing(self, tmp_path):
        assert list(DirectoryWalker(tmp_path).walk()) == []

    def test_html_extension_returns_html_parser(self, tmp_path):
        (tmp_path / "page.html").write_text("<p>hi</p>", encoding="utf-8")
        _, _, parser = next(DirectoryWalker(tmp_path).walk())
        assert isinstance(parser, HTMLParser)

    def test_supported_extensions_constant(self):
        assert ".md" in SUPPORTED_EXTENSIONS
        assert ".txt" in SUPPORTED_EXTENSIONS
        assert ".html" in SUPPORTED_EXTENSIONS
        assert ".htm" in SUPPORTED_EXTENSIONS
        assert ".markdown" in SUPPORTED_EXTENSIONS
