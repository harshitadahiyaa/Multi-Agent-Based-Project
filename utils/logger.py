"""Shared logging setup used by every agent."""

import logging
import os
import sys


def setup_logger(name: str) -> logging.Logger:
    """Create (or fetch) a logger with consistent formatting.

    Log level can be controlled via the LOG_LEVEL env var (DEBUG/INFO/WARNING/ERROR).
    Safe to call multiple times for the same name (won't duplicate handlers).
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
