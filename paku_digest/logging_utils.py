import logging
from .config import AppConfig


def get_logger(config:AppConfig) -> logging.Logger:
    logger = logging.getLogger("paku-digest")
    if logger.handlers:
        return logger
    
    level = getattr(logging, config.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)

    return logger
