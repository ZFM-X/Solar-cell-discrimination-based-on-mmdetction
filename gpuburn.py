import numpy as np
import cupy as cp
import time


### Numpy and CPU
s = time.time()
x_cpu = np.ones((100,100,100))
e = time.time()
print(e - s)
### CuPy and GPU
s = time.time()
for i in range(10000):
    x_gpu = cp.random.randn(1000000).reshape((1000, 1000))
    x2 =  cp.random.randn(1000000).reshape((1000, 1000))
    y = x_gpu * x_gpu
    y *= y
    y *= y
    y *= y
    y *= y

e = time.time()
print(e - s)
