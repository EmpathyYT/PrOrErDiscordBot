import logging

def setup_logging():
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='logs.log', level=logging.INFO)


def log_message(message):
    logger.info(message)
    print(message)