"""Weaviate vector-store adapter.

Provides :class:`WeaviateStore`, which wraps the Weaviate REST client to
support upsert, semantic search, and delete operations on pattern objects.

This is an implementation of the *Adapter* pattern: the Weaviate client API
is adapted to the uniform interface expected by the pattern pipeline.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import weaviate

logger = logging.getLogger(__name__)


class WeaviateStore:
    """Adapt the Weaviate client for pattern storage and retrieval.

    Args:
        url: Base URL of the running Weaviate instance.
        class_name: Weaviate class (collection) used to store patterns.

    Example:
        >>> store = WeaviateStore()
        >>> store.upsert_pattern({"id": "P-001", "name": "Install Package"})
        >>> results = store.query_similar_patterns("software installation")
    """

    def __init__(
        self,
        url: str = "http://localhost:8080",
        class_name: str = "Pattern",
    ) -> None:
        self.client = weaviate.Client(url)
        self.class_name = class_name
        logger.debug(
            "WeaviateStore initialised: url=%s, class=%s", url, class_name
        )

    def upsert_pattern(self, pattern: Dict[str, Any]) -> None:
        """Insert or update *pattern* in the Weaviate index.

        The ``id`` field of *pattern* is used as the Weaviate object UUID.

        Args:
            pattern: Pattern dictionary.  Must contain an ``"id"`` key.
        """
        uuid = pattern["id"]
        self.client.data_object.create(
            data_object=pattern,
            class_name=self.class_name,
            uuid=uuid,
        )
        logger.debug("Upserted pattern %s.", uuid)

    def query_similar_patterns(
        self, text: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Return the *top_k* patterns semantically closest to *text*.

        Args:
            text: Natural-language query string.
            top_k: Maximum number of results to return.

        Returns:
            A list of pattern dicts from Weaviate, each containing at least
            ``id``, ``name``, ``context``, and ``solution`` fields.
        """
        results = (
            self.client.query.get(
                class_name=self.class_name,
                properties=["id", "name", "context", "solution"],
            )
            .with_near_text({"concepts": [text]})
            .with_limit(top_k)
            .do()
        )
        return results["data"]["Get"].get(self.class_name, [])

    def delete_pattern(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Remove the pattern identified by *uuid* from the index.

        Args:
            uuid: The Weaviate object UUID to delete.

        Returns:
            The raw response from the Weaviate client, or ``None``.
        """
        logger.debug("Deleting pattern %s.", uuid)
        return self.client.data_object.delete(
            uuid=uuid, class_name=self.class_name
        )
