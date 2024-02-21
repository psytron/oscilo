


import numpy as np
from time import time
from multiprocessing.pool import ThreadPool

arr = np.ones((1024, 1024, 1024))

start = time()
for i in range(10):
    arr.sum()
print("Sequential:", time() - start)

expected = arr.sum()
start = time()
with ThreadPool(4) as pool:
    result = pool.map(np.sum, [arr] * 10)
    assert result == [expected] * 10
print("4 threads:", time() - start)