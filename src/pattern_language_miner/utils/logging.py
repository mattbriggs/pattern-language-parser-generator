import logging
import sys


def setup_logging(level: int = logging.INFO):
    """
    Configures logging for the application.

    Args:
        level (int): Logging level. Defaults to logging.INFO.
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []  # Clear existing handlers
    root_logger.addHandler(handler)

    logging.debug("Logging initialized at level %s", logging.getLevelName(level))