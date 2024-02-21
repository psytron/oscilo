
import ray
import time
import polars as pl
import random

# Create a Polars DataFrame
df = pl.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "B": ["a", "b", "c", "d", "e"],
        "C": [1.1, 2.2, 3.3, 4.4, 5.5]
    }
)

@ray.remote
class DataFrameActor:
    def __init__(self, df):
        self.df = df
        self.write_count = 0
        print(' ray actor hereha')

    def update_df(self):
        new_row = pl.DataFrame({"A": [random.randint(1, 100)], "B": [chr(random.randint(97, 122))], "C": [round(random.uniform(1.1, 5.5), 2)]})
        
        self.write_count += 1

    def get_df(self):
        return self.df

    def get_write_count(self):
        return self.write_count

    def reset_write_count(self):
        self.write_count = 0

if __name__ == "__main__":
    ray.init()

    # shared DataFrame using the Ray actor
    shared_df_actor = DataFrameActor.remote(df)

    # update processes
    update_refs = [shared_df_actor.update_df.remote() for _ in range(3)]

    # measuring process
    while True:
        time.sleep(1)
        df, write_count = ray.get([shared_df_actor.get_df.remote(), shared_df_actor.get_write_count.remote()])
        print(df, df.shape)
        print(f"Writes per second: {write_count}")
        shared_df_actor.reset_write_count.remote()

