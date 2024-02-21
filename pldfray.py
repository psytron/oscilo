







import ray
import random
import time


import polars as pl

# Create a Polars DataFrame
df = pl.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "B": ["a", "b", "c", "d", "e"],
        "C": [1.1, 2.2, 3.3, 4.4, 5.5]
    }
)

print(df)


@ray.remote
def update_df(df):
    while True:
        new_row = {"A": random.randint(1, 100), "B": chr(random.randint(97, 122)), "C": round(random.uniform(1.1, 5.5), 2)}
        df = df.append(pl.DataFrame(new_row))
        time.sleep(1)
        print(' in ray ', end="")
        print(df, end="")
ray.init()

process1 = update_df.remote(df)
process2 = update_df.remote(df)
process3 = update_df.remote(df)
