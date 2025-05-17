import os
import yaml
import nltk
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any
from pattern_language_miner.utils.config_validation import load_and_validate_config

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class PatternExtractor:
    def __init__(self, config_path: Path, input_dir: Path, output_dir: Path):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load and validate config using JSON Schema
        from pattern_language_miner.utils.config_validation import load_and_validate_config

        schema_path = Path(__file__).parent.parent / "schema" / "config_schema.json"
        config = load_and_validate_config(config_path, schema_path)["pattern_extraction"]

        self.file_type = config.get("file_type", "md")
        self.frequency_threshold = config.get("frequency_threshold", 3)
        self.minimum_token_count = config.get("minimum_token_count", 2)
        self.scope = config.get("scope", "sentence")
        self.pos_filtering = config.get("pos_filtering", False)
        self.allowed_pos_tags = set(config.get("allowed_pos_tags", []))
        self.block_elements = set(config.get("block_elements", []))
        self.ngram_min = config.get("ngram_min", 2)
        self.ngram_max = config.get("ngram_max", 5)

    def run(self) -> None:
        print(f"🚀 Extracting patterns from {self.input_dir}")
        documents = self._load_documents()
        patterns = self.extract_patterns(documents)
        self._write_patterns(patterns)

    def _load_documents(self) -> List[str]:
        docs = []
        for root, _, files in os.walk(self.input_dir):
            for fname in files:
                if not fname.endswith(f".{self.file_type}"):
                    continue
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        docs.append(f.read())
                except Exception as e:
                    print(f"⚠️ Could not read {fname}: {e}")
        return docs

    def extract_patterns(self, documents: List[str]) -> List[Dict[str, Any]]:
        """
        Extract frequent lexical n-grams from a list of documents.

        Returns:
            List[Dict[str, Any]]: A list of detected lexical patterns with frequency.
        """
        ngrams_counter = Counter()

        for doc in documents:
            scopes = self._split_scope(doc)

            for scope_text in scopes:
                sentences = nltk.sent_tokenize(scope_text)

                for sentence in sentences:
                    tokens = nltk.word_tokenize(sentence.lower())

                    # ✅ Enforce both minimum_token_count and ngram_min
                    if len(tokens) < max(self.ngram_min, self.minimum_token_count):
                        continue

                    # ✅ Optional POS filtering
                    if self.pos_filtering:
                        pos_tags = nltk.pos_tag(tokens)
                        if not all(tag in self.allowed_pos_tags for _, tag in pos_tags):
                            continue

                    # ✅ Extract only n-grams within bounds
                    max_n = min(len(tokens), self.ngram_max)
                    for n in range(self.ngram_min, max_n + 1):
                        for gram in nltk.ngrams(tokens, n):
                            ngrams_counter[" ".join(gram)] += 1

        patterns = [
            {"pattern": ngram, "frequency": freq}
            for ngram, freq in ngrams_counter.items()
            if freq >= self.frequency_threshold
        ]

        return sorted(patterns, key=lambda x: -x["frequency"])

    def _split_scope(self, doc: str) -> List[str]:
        if self.scope == "line":
            return [line for line in doc.splitlines() if line.strip()]

        elif self.scope == "sentence":
            return nltk.sent_tokenize(doc)

        elif self.scope == "block":
            return self._split_blocks(doc)

        return [doc]

    def _split_blocks(self, doc: str) -> List[str]:
        paragraphs = [p.strip() for p in doc.split("\n\n") if p.strip()]
        return paragraphs if "paragraph" in self.block_elements else [doc]

    def _write_patterns(self, patterns: List[Dict[str, Any]]) -> None:
        for idx, pattern in enumerate(patterns, 1):
            file_path = self.output_dir / f"pattern-{idx:05}.yaml"
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(pattern, f, allow_unicode=True)
        print(f"✅ Saved {len(patterns)} patterns to {self.output_dir}")
