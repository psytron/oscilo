
import multiprocessing as mp
import time
import polars as pl
import random
from multiprocessing import Manager

# Create a Polars DataFrame
df = pl.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "B": ["a", "b", "c", "d", "e"],
        "C": [1.1, 2.2, 3.3, 4.4, 5.5]
    }
)

def update_df(mn, write_count):
    df = mn[0]
    while True:
        new_row = pl.DataFrame({"A": [random.randint(1, 100)], "B": [chr(random.randint(97, 122))], "C": [round(random.uniform(1.1, 5.5), 2)]})
        mn[0] = pl.concat([mn[0], new_row])
        with write_count.get_lock():
            write_count.value += 1

# measure writes per second
def measure_wps(mn, write_count):
    while True:
        time.sleep(1)
        with write_count.get_lock():
            print( mn[0]  , mn[0].shape )
            print(f"Writes per second: {write_count.value}")
            write_count.value = 0

if __name__ == "__main__":

    write_count = mp.Value('i', 0)

    # shared state
    manager = Manager()

    # shared DataFrame using the Manager
    shared_df = manager.list([df])

    p1 = mp.Process(target=update_df, args=(shared_df, write_count))
    p2 = mp.Process(target=update_df, args=(shared_df, write_count))
    p3 = mp.Process(target=update_df, args=(shared_df, write_count))

    # measuring process 
    p4 = mp.Process(target=measure_wps, args=(shared_df , write_count,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
