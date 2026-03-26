"""Extractor sub-package.

Provides :class:`~pattern_language_miner.extractor.pattern_extractor.PatternExtractor`
for lexical n-gram extraction and
:class:`~pattern_language_miner.extractor.semantic_cluster.SemanticCluster`
for sentence-level semantic grouping.
"""

from .pattern_extractor import PatternExtractor
from .semantic_cluster import SemanticCluster

__all__ = ["PatternExtractor", "SemanticCluster"]
