

from multiprocessing import Process, Manager
import numpy as np
import pandas as pd

def add_random_numbers(df, lock):
    while True:
        with lock:
            random_number = np.random.random()
            df.loc[:, :] += random_number

manager = Manager()
lock = manager.Lock()
df = manager.dict()
df['data'] = pd.DataFrame(np.random.random(size=(1000, 5000)))

p1 = Process(target=add_random_numbers, args=(df['data'], lock))
p2 = Process(target=add_random_numbers, args=(df['data'], lock))

p1.start()
p2.start()

p1.join()
p2.join()

