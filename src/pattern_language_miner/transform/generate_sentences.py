import os
import yaml
from pathlib import Path


class SentenceGenerator:
    """Generates natural language sentences from pattern YAML files."""

    def __init__(self, input_dir: str, output_path: str, format_: str = "text", template: str = None):
        self.input_dir = Path(input_dir)
        self.output_path = Path(output_path)
        self.format = format_.lower()
        self.template = template or (
            "To {problem} in the context of {context}, "
            "use {solution}. For example, {example}."
        )

    def load_patterns(self):
        """Load all pattern YAML files that include the required keys."""
        patterns = []
        for file_path in self.input_dir.glob("pattern-*.yaml"):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                    if all(k in data for k in ("problem", "context", "solution", "example")):
                        patterns.append(data)
                except yaml.YAMLError:
                    continue
        return patterns

    def generate_sentences(self, patterns):
        """Apply the template to each loaded pattern."""
        return [
            self.template.format(
                problem=pat["problem"],
                context=pat["context"],
                solution=pat["solution"],
                example=pat["example"]
            )
            for pat in patterns
        ]

    def save_output(self, sentences):
        """Write the generated sentences to the specified output format."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.format == "markdown":
            with open(self.output_path, "w", encoding="utf-8") as f:
                for i, sentence in enumerate(sentences, 1):
                    f.write(f"{i}. {sentence}\n\n")
        elif self.format == "html":
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write("<ul>\n")
                for sentence in sentences:
                    f.write(f"  <li>{sentence}</li>\n")
                f.write("</ul>\n")
        else:  # plain text
            with open(self.output_path, "w", encoding="utf-8") as f:
                for i, sentence in enumerate(sentences, 1):
                    f.write(f"{i}. {sentence}\n")

    def run(self):
        """Run the sentence generation process and save the result."""
        patterns = self.load_patterns()
        sentences = self.generate_sentences(patterns)
        self.save_output(sentences)
        print(f"✅ {len(sentences)} sentence(s) written to {self.output_path} as {self.format.upper()}.")