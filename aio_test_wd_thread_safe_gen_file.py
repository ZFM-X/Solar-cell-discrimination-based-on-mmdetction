# 验证watchdog线程安全与否

# 试验思路：A线程为主进程线程，B为监控线程，C线程负责处理事件，A中的变量v传到C中使用，看看v是否线程安全。

# 本文件生成文件以触发watchdog
import os
import time
import threading
import random

fo = 'test_wd'
if not os.path.exists:
    os.mkdir(fo)

for i in os.listdir(fo):
    os.remove(os.path.join(fo, i))

def cre(index):
    fo = 'test_wd'
    with open(os.path.join(fo, str(random.random())+str(index)), 'w') as f:
        f.write(str(index))

ts = []

for i in range(1000):
    thread_beating = threading.Thread(target=cre, args=(i,))
    ts.append(thread_beating)

for i in ts:
    i.start()

for i in ts:
    i.join()


# for i in range(10):
#     with open(os.path.join(fo, str(time.time())), 'w') as f:
#         f.write(str(i))
#     print('gen: ', i)
