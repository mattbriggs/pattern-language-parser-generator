"""Application-wide logging helpers."""

from __future__ import annotations

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the root logger for the application.

    Sets a uniform format and ensures only one :class:`~logging.StreamHandler`
    writing to *stdout* is attached to the root logger.  Calling this
    function more than once is safe — existing handlers are cleared first.

    Args:
        level: Python logging level constant, e.g. :data:`logging.DEBUG`.
            Defaults to :data:`logging.INFO`.

    Example:
        >>> import logging
        >>> setup_logging(logging.DEBUG)
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s  %(name)-30s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    logging.debug("Logging initialised at level %s", logging.getLevelName(level))
