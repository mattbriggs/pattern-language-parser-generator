"""Semantic pattern clustering module.

Uses :class:`~sentence_transformers.SentenceTransformer` embeddings,
KMeans clustering, and UMAP dimensionality reduction to group similar
patterns and visualise the results.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import umap
import yaml
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


class PatternClusterer:
    """Cluster semantic-embedding vectors of pattern texts.

    The full pipeline:

    1. Load patterns from YAML files (:meth:`load_patterns`).
    2. Encode field values with a sentence transformer (:meth:`embed_patterns`).
    3. Cluster with KMeans and reduce dimensions with UMAP
       (:meth:`cluster_and_reduce`).
    4. Visualise the 2-D projection (:meth:`visualize_clusters`).
    5. Save a JSON report with cluster assignments
       (:meth:`generate_cluster_report`).

    Args:
        input_dir: Directory of ``*.yaml`` pattern files to load.
        field: Pattern field to embed (e.g. ``"solution"``).
        model_name: Sentence-transformer model identifier.
        batch_size: Number of sentences encoded per batch.

    Example:
        >>> clusterer = PatternClusterer("./enriched", field="solution")
        >>> clusterer.load_patterns()
        >>> embeddings = clusterer.embed_patterns()
        >>> reduced, cluster_ids = clusterer.cluster_and_reduce(embeddings)
    """

    def __init__(
        self,
        input_dir: str | Path,
        field: str,
        model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 64,
    ) -> None:
        self.input_dir = Path(input_dir)
        self.field = field
        self.model_name = model_name
        self.batch_size = batch_size
        self.patterns: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray | None = None
        self.model = SentenceTransformer(model_name)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_patterns(self) -> None:
        """Load all YAML pattern files that contain :attr:`field`.

        Files that cannot be parsed are skipped with a WARNING log entry.
        The loaded patterns are stored in :attr:`patterns`.
        """
        files = sorted(self.input_dir.glob("*.yaml"))
        logger.info("Scanning %d YAML file(s) in %s", len(files), self.input_dir)

        loaded: List[Dict[str, Any]] = []
        for file_path in files:
            try:
                with file_path.open("r", encoding="utf-8") as fh:
                    pattern = yaml.safe_load(fh)
                if pattern and self.field in pattern:
                    loaded.append(pattern)
            except yaml.YAMLError as exc:
                logger.warning("Skipping %s: %s", file_path.name, exc)

        self.patterns = loaded
        logger.info("Loaded %d valid pattern(s).", len(self.patterns))

    def embed_patterns(self, batch_size: int | None = None) -> np.ndarray:
        """Encode pattern field values as sentence embeddings.

        Args:
            batch_size: Override the instance-level :attr:`batch_size`.

        Returns:
            A NumPy array of shape ``(n_patterns, embedding_dim)``.
        """
        bs = batch_size or self.batch_size
        texts = [p[self.field] for p in self.patterns]
        total = len(texts)
        logger.info("Encoding %d pattern(s) in batches of %d.", total, bs)

        all_embeddings: list = []
        for start in range(0, total, bs):
            end = min(start + bs, total)
            batch = texts[start:end]
            logger.debug(
                "Encoding batch %d: items %d-%d",
                start // bs + 1,
                start,
                end - 1,
            )
            batch_embs = self.model.encode(batch, show_progress_bar=False)
            all_embeddings.extend(batch_embs)

        self.embeddings = np.array(all_embeddings)
        logger.info("All embeddings generated. Shape: %s", self.embeddings.shape)
        return self.embeddings

    def cluster_and_reduce(
        self,
        embeddings: np.ndarray,
        n_clusters: int = 5,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Run KMeans clustering and UMAP 2-D reduction.

        If *n_clusters* exceeds the sample count it is clamped automatically.

        Args:
            embeddings: Array of shape ``(n_samples, dim)`` from
                :meth:`embed_patterns`.
            n_clusters: Number of KMeans clusters.

        Returns:
            A 2-tuple of ``(reduced_2d, cluster_ids)`` where *reduced_2d*
            has shape ``(n_samples, 2)`` and *cluster_ids* is a 1-D integer
            array of length *n_samples*.
        """
        n_samples = embeddings.shape[0]
        if n_clusters > n_samples:
            logger.warning(
                "Requested %d clusters but only %d samples; reducing to %d.",
                n_clusters,
                n_samples,
                n_samples,
            )
            n_clusters = n_samples

        logger.info("Clustering with KMeans (k=%d).", n_clusters)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        cluster_ids: np.ndarray = kmeans.fit_predict(embeddings)
        logger.info("KMeans clustering finished.")

        logger.info("Reducing dimensions with UMAP for 2-D projection.")
        reducer = umap.UMAP(
            n_neighbors=min(15, n_samples - 1), random_state=42
        )
        reduced: np.ndarray = reducer.fit_transform(embeddings)
        logger.info("Dimensionality reduction complete.")
        return reduced, cluster_ids

    def visualize_clusters(
        self,
        reduced: np.ndarray,
        cluster_ids: np.ndarray,
        output_path: Path,
    ) -> None:
        """Save a scatter-plot PNG of the 2-D cluster projection.

        Args:
            reduced: 2-D coordinates from :meth:`cluster_and_reduce`.
            cluster_ids: Cluster label for each point.
            output_path: Destination path for the PNG file.
        """
        logger.info("Rendering cluster plot to %s.", output_path)
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(
            reduced[:, 0],
            reduced[:, 1],
            c=cluster_ids,
            cmap="tab10",
            s=50,
        )
        fig.colorbar(scatter, ax=ax, label="Cluster ID")
        ax.set_title("Pattern Clusters (UMAP Reduced)")
        ax.set_xlabel("UMAP-1")
        ax.set_ylabel("UMAP-2")
        fig.tight_layout()
        fig.savefig(output_path)
        plt.close(fig)
        logger.info("Cluster plot saved to %s.", output_path)

    def generate_cluster_report(
        self,
        cluster_ids: np.ndarray,
        output_path: Path,
    ) -> None:
        """Write a JSON file mapping each pattern to its cluster ID.

        Args:
            cluster_ids: Cluster labels from :meth:`cluster_and_reduce`.
            output_path: Destination path for the JSON report.
        """
        logger.info("Generating cluster report to %s.", output_path)
        report = []
        for pattern, cluster_id in zip(self.patterns, cluster_ids):
            entry = dict(pattern)
            entry["cluster"] = int(cluster_id)
            report.append(entry)

        with output_path.open("w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
        logger.info("Cluster report written (%d entries).", len(report))
