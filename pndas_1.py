


import multiprocessing as mp
import numpy as np
import pandas as pd
from tqdm import tqdm


rows, cols = 1000, 5000
df = pd.DataFrame(
    np.random.random(size=(rows, cols)),
    columns=[f'Col-{i}' for i in range(cols)],
    index=[f'Idx-{i}' for i in range(rows)]
)

print(f'Data size: {df.values.nbytes / 1024 / 1204:.1f} MB')
df.iloc[:5, :5]