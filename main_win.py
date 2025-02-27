import time
import threading
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os

from watchdog.observers import Observer

from observer_win import PNGEventHandler

pipline_name = '15A'

logger = logging.getLogger(pipline_name)
logger.setLevel(level=logging.INFO)

formatter = '%(asctime)s -<>- %(filename)s -<>- [line]:%(lineno)d -<>- %(levelname)s -<>- %(message)s'
time_rotate_file = TimedRotatingFileHandler(filename=os.path.join('log', pipline_name), when='MIDNIGHT', interval=1, backupCount=365) # MIDNIGHT S
time_rotate_file.setFormatter(logging.Formatter(formatter))
time_rotate_file.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(level=logging.INFO)
console_handler.setFormatter(logging.Formatter(formatter))

logger.addHandler(time_rotate_file)
logger.addHandler(console_handler)

config = {'folder_name': "\\EL_NG\\"}

while True:

    print('尝试重新监控', time.time())
    logger.info('尝试重新监控')

    observer = Observer()
    event_handler = PNGEventHandler(
        config=config, 
        logger=logger,
    )
    if pipline_name == '15A':
        observer.schedule(event_handler, r"\\10.23.151.196\halm\PVCTData\\", recursive=True)
        print('r"\\172.20.149.173\halm\PVCTData\\"')
    elif pipline_name == '15B':
        observer.schedule(event_handler, r"\\10.23.153.190\halm\PVCTData\2022", recursive=True)
        print('r"\\172.20.149.176\halm\PVCTData\\')


    try:
        observer.start()
        print('监控成功开启', time.time())
        logger.info('监控成功开启')
        try:
            while True:
                time.sleep(0.01)
                # print(threading.active_count(), time.time())
                if (th_count:=threading.active_count()) < 3:
                    print('监控线程数异常：', th_count, time.time())
                    logger.error('监控线程数异常：' + str(th_count))
                    break
        finally:
            # observer.stop()
            # observer.join()
            observer.stop()
            observer.join()
    except:
        print('重新监控尝试失败', threading.active_count(), time.time())
        logger.error('重新监控尝试失败，线程数：' + str(threading.active_count()))
    
    print(threading.active_count(), time.time())
    time.sleep(0.01)
