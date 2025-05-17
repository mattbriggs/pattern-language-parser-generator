import os
import nltk
from pathlib import Path
from collections import Counter
from typing import List, Dict

nltk.download('punkt', quiet=True)


class PatternExtractor:
    def __init__(self, input_dir: Path, file_types: list[str]):
        self.input_dir = Path(input_dir)
        self.file_types = file_types
        self.ngram_min = 2
        self.ngram_max = 5
        self.min_frequency = 2

    def run(self) -> List[Dict[str, object]]:
        """Scan files and extract frequent lexical patterns."""
        documents = self._load_documents()
        return self.extract_lexical_patterns(documents)

    def _load_documents(self) -> List[str]:
        """Load all matching files from the input directory."""
        documents = []
        for root, _, files in os.walk(self.input_dir):
            for fname in files:
                if any(fname.endswith(ext) for ext in self.file_types):
                    path = os.path.join(root, fname)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            documents.append(f.read())
                    except Exception as e:
                        print(f"⚠️ Failed to read {fname}: {e}")
        return documents

    def extract_lexical_patterns(self, documents: List[str]) -> List[Dict[str, object]]:
        """
        Extract frequent lexical n-grams from a list of documents.

        Args:
            documents (List[str]): List of raw text strings.

        Returns:
            List[Dict]: A list of detected lexical patterns with frequency.
        """
        all_ngrams = []

        for doc in documents:
            sentences = nltk.sent_tokenize(doc)
            for sentence in sentences:
                words = nltk.word_tokenize(sentence.lower())
                for n in range(self.ngram_min, self.ngram_max + 1):
                    ngrams = nltk.ngrams(words, n)
                    all_ngrams.extend([' '.join(gram) for gram in ngrams])

        freq_dist = Counter(all_ngrams)
        patterns = [
            {"pattern": ngram, "frequency": count}
            for ngram, count in freq_dist.items()
            if count >= self.min_frequency
        ]

        return sorted(patterns, key=lambda x: x["frequency"], reverse=True)