import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger():
    BASE_DIR = Path(__file__).resolve().parent

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Verifica se já existe handler de arquivo
    error_handler_exists = any(
        isinstance(h, RotatingFileHandler)
        for h in logger.handlers
    )

    # Verifica se já existe handler de console
    console_handler_exists = any(
        isinstance(h, logging.StreamHandler)
        and not isinstance(h, RotatingFileHandler)
        for h in logger.handlers
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console (INFO+)
    if not console_handler_exists:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    # Arquivo de erros na raiz do projeto
    if not error_handler_exists:
        error_handler = RotatingFileHandler(
            BASE_DIR / "erros.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        logger.addHandler(error_handler)

    return logger
