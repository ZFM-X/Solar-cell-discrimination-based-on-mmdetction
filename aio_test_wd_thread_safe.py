# 验证watchdog线程安全与否

# 试验思路：A线程为主进程线程，B为监控线程，C线程负责处理事件，A中的变量v传到C中使用，看看v是否线程安全。


import sys
import time
import random
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


class PngHandle(FileSystemEventHandler):

    def __init__(self, myWife):
        self.myWife = myWife

    
    def on_created(self, event):
        super().on_created(event)
        # assert self.myWife[0] == 0

        # time.sleep(random.random())

        self.myWife[0] += 1
        print(self.myWife)
        # assert myWife[0] == 1

        # # myWife[0] -= 1

        # assert myWife[0] == 0



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else './test_wd'

    myWife = [0]  # 全局变量   

    # event_handler = LoggingEventHandler()
    event_handler = PngHandle(myWife)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            print(myWife[0])
            
    finally:
        observer.stop()
        observer.join()
