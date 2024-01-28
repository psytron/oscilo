

import multiprocessing as mp
import pandas as pd
import numpy as np
from multiprocessing import shared_memory

class Worker:
    def __init__(self, name, shared_df):
        self.name = name
        self.shared_df = shared_df

    def run(self):
        print(f"Worker {self.name} is running")
        # Perform operations on shared_df here
        #while True:
        #    print(' worker', self.name )

# Create a pandas DataFrame
df = pd.DataFrame(np.random.rand(100, 100))

# Create a shared memory block
shm = shared_memory.SharedMemory(create=True, size=df.size * df.dtypes[0].itemsize)

# Now create a NumPy array backed by shared memory
shared_df = np.ndarray(df.shape, dtype=df.dtypes[0], buffer=shm.buf)

# Copy the original DataFrame into shared memory
np.copyto(shared_df, df.to_numpy())

# Create worker instances
worker1 = Worker("1", shared_df)
worker2 = Worker("2", shared_df)
worker3 = Worker("3", shared_df)

# Create processes
p1 = mp.Process(target=worker1.run)
p2 = mp.Process(target=worker2.run)
p3 = mp.Process(target=worker3.run)

# Start processes
p1.start()
p2.start()
p3.start()

# Join processes
p1.join()
p2.join()
p3.join()

# Cleanup the shared memory block
shm.close()
shm.unlink()
