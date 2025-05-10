from typing import Iterable, Iterator
from tqdm import tqdm


def show_progress(items: Iterable, description: str = "Processing") -> Iterator:
    """
    Wrap an iterable with a progress bar using tqdm.

    Args:
        items (Iterable): The iterable to wrap.
        description (str): Description displayed with the progress bar.

    Returns:
        Iterator: Wrapped iterable with a progress bar.
    """
    return tqdm(items, desc=description, unit="item")