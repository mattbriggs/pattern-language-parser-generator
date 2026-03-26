"""Progress-bar helpers backed by ``tqdm``."""

from __future__ import annotations

from typing import Iterable, Iterator

from tqdm import tqdm


def show_progress(items: Iterable, description: str = "Processing") -> Iterator:
    """Wrap an iterable with a ``tqdm`` progress bar.

    Args:
        items: Any iterable to wrap.
        description: Short label displayed to the left of the progress bar.

    Returns:
        A ``tqdm``-wrapped iterator that displays progress to the terminal.

    Example:
        >>> for item in show_progress(range(10), "Counting"):
        ...     pass
    """
    return tqdm(items, desc=description, unit="item")
