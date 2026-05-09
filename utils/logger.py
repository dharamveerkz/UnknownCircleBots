import logging
import os

# =========================================================
# CREATE LOGS FOLDER
# =========================================================

os.makedirs(
    "logs",
    exist_ok=True
)

# =========================================================
# LOGGER SETUP
# =========================================================


def setup_logger(
    name,
    log_file
):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    )

    # File Handler
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    # Console Handler
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger
