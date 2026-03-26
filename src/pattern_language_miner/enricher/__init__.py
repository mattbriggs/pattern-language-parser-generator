"""Enricher sub-package.

Provides :class:`~pattern_language_miner.enricher.pattern_enricher.PatternEnricher`
and the standalone :func:`~pattern_language_miner.enricher.pattern_enricher.enrich_pattern`
helper.
"""

from .pattern_enricher import PatternEnricher, enrich_pattern

__all__ = ["PatternEnricher", "enrich_pattern"]
