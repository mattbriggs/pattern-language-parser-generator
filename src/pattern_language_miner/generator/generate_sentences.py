import os
import re
import logging
import yaml
from pathlib import Path
from typing import List, Dict


class SentenceGenerator:
    """
    Generate sentences from YAML pattern files using a grammar-based template.
    """

    def __init__(self, input_dir: str, output_path: str, format_: str = "markdown"):
        self.input_dir = Path(input_dir)
        self.output_path = Path(output_path)
        self.format = format_.lower()
        self.supported_formats = {"markdown", "html", "text"}

        if self.format not in self.supported_formats:
            raise ValueError(
                f"Unsupported format '{self.format}'. "
                f"Choose from: {', '.join(self.supported_formats)}"
            )

    def load_patterns(self) -> List[Dict]:
        """
        Load all YAML pattern files from the input directory.
        """
        patterns = []
        for file_path in sorted(self.input_dir.glob("*.yaml")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    pattern = yaml.safe_load(f)
                    if pattern:
                        patterns.append(pattern)
            except Exception as e:
                logging.warning(f"Could not parse {file_path.name}: {e}")
        return patterns

    def generate_sentence(self, pattern: Dict) -> str:
        """
        Apply the grammar template to a single pattern dictionary.
        """
        solution = pattern.get("solution", "solve the problem")
        context = pattern.get("context", "a general scenario")
        example = pattern.get("example", "no example provided")

        return (
            f"To {solution} in the context of {context}, use {solution}. "
            f"For example, {example}."
        )

    def format_sentences(self, sentences: List[str]) -> str:
        """
        Format a list of sentences in the requested output format.
        """
        if self.format == "markdown":
            return "\n\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))
        elif self.format == "html":
            items = "".join(f"<li>{s}</li>" for s in sentences)
            return f"<ul data-type='generated-patterns'>\n{items}\n</ul>"
        elif self.format == "text":
            return "\n".join(sentences)
        return ""

    def write_output(self, content: str) -> None:
        """
        Write formatted sentences to the output file.
        """
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(
            f"✅ {len(content.splitlines())} sentence(s) written to {self.output_path} as {self.format.upper()}."
        )

    def run(self) -> None:
        """
        Execute the full sentence generation pipeline.
        """
        logging.info("📄 Loading patterns...")
        patterns = self.load_patterns()
        if not patterns:
            logging.warning("⚠️ No patterns found.")
            return

        logging.info(f"🧠 Generating {len(patterns)} sentence(s)...")
        sentences = [self.generate_sentence(p) for p in patterns]
        formatted = self.format_sentences(sentences)
        self.write_output(formatted)
