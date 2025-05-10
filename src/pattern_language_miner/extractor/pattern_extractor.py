import nltk
from collections import Counter
from typing import List, Dict

nltk.download('punkt', quiet=True)


class PatternExtractor:
    def __init__(self):
        self.ngram_min = 2
        self.ngram_max = 5
        self.min_frequency = 2

    def extract_lexical_patterns(self, documents: List[str]) -> List[Dict[str, object]]:
        """
        Extracts frequent lexical n-grams from a list of documents.

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