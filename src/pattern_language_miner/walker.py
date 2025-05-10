import logging
from pathlib import Path
from typing import Generator, Tuple

from .parser.base_parser import BaseParser
from .parser.text_parser import TextParser
from .parser.markdown_parser import MarkdownParser
from .parser.html_parser import HTMLParser

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {'.txt', '.md', '.markdown', '.html', '.htm'}


class ParserFactory:
    @staticmethod
    def get_parser(file_extension: str) -> BaseParser:
        """
        Return the appropriate parser for the given file extension.

        Args:
            file_extension (str): The file extension including dot (e.g., '.md').

        Returns:
            BaseParser: An instance of the appropriate parser.

        Raises:
            ValueError: If the file extension is not supported.
        """
        if file_extension in {'.md', '.markdown'}:
            return MarkdownParser()
        elif file_extension in {'.html', '.htm'}:
            return HTMLParser()
        elif file_extension == '.txt':
            return TextParser()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")


class DirectoryWalker:
    def __init__(self, root_dir: str):
        """
        Initialize the directory walker.

        Args:
            root_dir (str): Path to the directory to walk through.
        """
        self.root_dir = Path(root_dir)

    def walk(self) -> Generator[Tuple[Path, str, BaseParser], None, None]:
        """
        Recursively walk through the directory, reading supported files and yielding their content.

        Yields:
            Tuple[Path, str, BaseParser]: The file path, content, and appropriate parser.
        """
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in SUPPORTED_EXTENSIONS:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        parser = ParserFactory.get_parser(ext)
                        yield (file_path, content, parser)
                    except Exception as e:
                        logger.warning(f"Failed to read or parse {file_path}: {e}")