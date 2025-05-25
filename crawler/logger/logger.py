import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def setup_logger(name: str = "crawler") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
