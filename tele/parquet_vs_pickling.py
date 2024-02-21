

import pandas as pd
import multiprocessing as mp
from pathlib import Path
from tempfile import mkdtemp
from time import time


def noop(df: pd.DataFrame):
    # real code would process the dataframe here
    pass


def noop_from_path(path: Path):
    df = pd.read_parquet(path, engine="fastparquet")
    # real code would process the dataframe here
    pass


def main():
    df = pd.DataFrame({"column": list(range(10_000_000))})
    with mp.get_context("spawn").Pool(1) as pool:
        # Pass the DataFrame to the worker process
        # directly, via pickling:
        start = time()
        pool.apply(noop, (df,))
        print("Pickling-based:", time() - start)

        # Write the DataFrame to a file, pass the path to
        # the file to the worker process:
        start = time()
        path = Path(mkdtemp()) / "temp.parquet"
        df.to_parquet(
            path,
            engine="fastparquet",
            # Run faster by skipping compression:
            compression="uncompressed",
        )
        pool.apply(noop_from_path, (path,))
        print("Parquet-based:", time() - start)


if __name__ == "__main__":
    main()