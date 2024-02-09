

import os
import polars as pl
from multiprocessing import Process, shared_memory

def create_shared_df():
    # Create a DataFrame
    df = pl.DataFrame({
        "A": range(1, 6),
        "B": ["A", "B", "C", "D", "E"],
        "C": [1.1, 2.2, 3.3, 4.4, 5.5]
    })

    # Create a new shared memory block
    shm = shared_memory.SharedMemory(create=True, size=df.buffer.byte_size)

    # Write the DataFrame to shared memory
    df.buffer.copy_to(shm.buf)

    # Return the name of the shared memory block
    return shm.name

def read_shared_df(shm_name):
    # Attach to the existing shared memory block
    shm = shared_memory.SharedMemory(name=shm_name)

    # Create a new DataFrame from the shared memory
    df = pl.DataFrame.from_buffer(shm.buf)

    # Print the DataFrame
    print(df)

if __name__ == "__main__":
    # Create a DataFrame in shared memory in a new process
    p1 = Process(target=create_shared_df)
    p1.start()
    p1.join()

    # Read the DataFrame from shared memory in another new process
    p2 = Process(target=read_shared_df, args=(p1,))
    p2.start()
    p2.join()
