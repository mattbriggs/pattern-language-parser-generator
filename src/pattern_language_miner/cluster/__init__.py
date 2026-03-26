"""Cluster sub-package.

Provides :class:`~pattern_language_miner.cluster.pattern_cluster.PatternClusterer`
for KMeans/UMAP-based semantic clustering.
"""

from .pattern_cluster import PatternClusterer

__all__ = ["PatternClusterer"]
