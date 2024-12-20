import logging


def setup_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Предотвращение дублирования обработчиков
        handler = logging.FileHandler("test.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
