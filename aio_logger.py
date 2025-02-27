import os
import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name, filename):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)

    formatter = '%(asctime)s -<>- %(filename)s -<>- [line]:%(lineno)d -<>- %(levelname)s -<>- %(message)s'

    if not os.path.exists((filepath:=os.path.split(filename)[0])):
        os.makedirs(filepath)

    time_rotate_file = TimedRotatingFileHandler(filename=filename, when='MIDNIGHT', interval=1, backupCount=365) # MIDNIGHT S
    time_rotate_file.setFormatter(logging.Formatter(formatter))
    time_rotate_file.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=logging.INFO)
    console_handler.setFormatter(logging.Formatter(formatter))

    logger.addHandler(time_rotate_file)
    logger.addHandler(console_handler)

    return logger
