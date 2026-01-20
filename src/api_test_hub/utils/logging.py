from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


def configure_logging(
    log_dir: str | Path,
    name: str = "api_test_hub",
    level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path / "api_test_hub.log", encoding="utf-8")

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def get_logger(name: str = "api_test_hub") -> Optional[logging.Logger]:
    logger = logging.getLogger(name)
    return logger if logger.handlers else None
