import logging
from logging.handlers import TimedRotatingFileHandler
import time
 
 
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
 
formatter = '%(asctime)s -<>- %(filename)s -<>- [line]:%(lineno)d -<>- %(levelname)s -<>- %(message)s'
time_rotate_file = TimedRotatingFileHandler(filename='time_rotate', when='S', interval=5, backupCount=3) # MIDNIGHT
time_rotate_file.setFormatter(logging.Formatter(formatter))
time_rotate_file.setLevel(logging.INFO)
 
console_handler = logging.StreamHandler()
console_handler.setLevel(level=logging.INFO)
console_handler.setFormatter(logging.Formatter(formatter))
 
logger.addHandler(time_rotate_file)
logger.addHandler(console_handler)
 
while True:
    logger.info('info')
    logger.error('error')
    time.sleep(1)
