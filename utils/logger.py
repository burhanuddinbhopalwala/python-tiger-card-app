import logging


def logger(level, handler):
    """Generates logger."""
    if level.upper() == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif level.upper() == 'INFO':
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(handler)

    return logger
