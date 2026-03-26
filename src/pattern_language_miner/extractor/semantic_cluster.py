"""Sentence-level semantic clustering using cosine similarity.

Provides :class:`SemanticCluster`, which groups a list of sentences into
clusters based on pairwise cosine similarity of sentence-transformer
embeddings.
"""

from __future__ import annotations

import logging
from typing import List

from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)


class SemanticCluster:
    """Group semantically similar sentences into clusters.

    This class uses a sentence-transformer model to embed each sentence and
    then performs greedy single-pass clustering: a sentence is added to the
    first existing cluster whose centroid-representative it is sufficiently
    similar to.

    Args:
        model_name: Identifier of the sentence-transformer model to load.
        similarity_threshold: Minimum cosine similarity (0–1) required for
            two sentences to belong to the same cluster.

    Example:
        >>> sc = SemanticCluster(similarity_threshold=0.8)
        >>> clusters = sc.cluster_sentences(["Install nginx", "Setup nginx"])
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.75,
    ) -> None:
        self.similarity_threshold = similarity_threshold
        self.model = SentenceTransformer(model_name)
        logger.debug(
            "SemanticCluster initialised: model=%s, threshold=%.2f",
            model_name,
            similarity_threshold,
        )

    def cluster_sentences(self, sentences: List[str]) -> List[List[str]]:
        """Group *sentences* by semantic similarity.

        Args:
            sentences: List of sentences to cluster.

        Returns:
            A list of clusters.  Each cluster is a non-empty list of
            sentences that are mutually above the similarity threshold
            relative to the first (representative) sentence.

        Example:
            >>> sc = SemanticCluster()
            >>> clusters = sc.cluster_sentences(["a", "b", "c"])
            >>> len(clusters) >= 1
            True
        """
        if not sentences:
            return []

        embeddings = self.model.encode(sentences, convert_to_tensor=True)
        clusters: List[List[str]] = []
        used: set[int] = set()

        for i, emb in enumerate(embeddings):
            if i in used:
                continue
            cluster = [sentences[i]]
            used.add(i)

            for j in range(i + 1, len(sentences)):
                if j in used:
                    continue
                sim: float = util.pytorch_cos_sim(emb, embeddings[j]).item()
                if sim >= self.similarity_threshold:
                    cluster.append(sentences[j])
                    used.add(j)

            clusters.append(cluster)

        logger.debug(
            "Clustered %d sentences into %d group(s).",
            len(sentences),
            len(clusters),
        )
        return clusters
