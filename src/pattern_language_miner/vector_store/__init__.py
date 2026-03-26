"""Vector-store sub-package.

Provides :class:`~pattern_language_miner.vector_store.weaviate_store.WeaviateStore`,
a Weaviate adapter for semantic pattern search.
"""

from .weaviate_store import WeaviateStore

__all__ = ["WeaviateStore"]
