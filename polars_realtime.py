import polars as pl
import numpy as np
from datetime import datetime, timedelta
 
NUM_SAMPLES =  3
 
days = [ datetime.now() + timedelta(seconds=x) for x in range( NUM_SAMPLES )]

# Generate random data for close, bid, ask, vol columns
np.random.seed(0)
data = np.random.rand( NUM_SAMPLES , 4)

# Create a new polars dataframe
df = pl.DataFrame({
    'date': days,
    'symbol': np.random.choice( ['ETH/BTC', 'BTC/USD'] ),
    'close': data[:, 0],
    'bid': data[:, 1],
    'ask': data[:, 2],
    'vol': data[:, 3]
})

print( df )
print(  df['date'][-1:] )
print(df.tail(1))


from joblib import Parallel, delayed
import time
import os

# Function to check the last value of the dataframe
def check_last_value(df):
    while True:
        print(f'Process ID: {os.getpid()}, Last Value: {df.tail(1)}')
        time.sleep(1)

def check_first_value( df ):
    while True:
        print(f'Process ID: {os.getpid()}, First Value: {df.head(1)}')
        
        time.sleep(1)    

# Start two separate long running processes
# The following code is using the joblib library to run multiple instances of the function 'check_last_value' in parallel.
# 'Parallel' is a utility function that allows easy parallelization of simple for-loops.
# 'n_jobs' parameter specifies the maximum number of concurrently running jobs. Here, it is set to 2, meaning two processes will run concurrently.
# 'delayed' is a simple trick to specify a function to be called and arguments to be used, without calling the function. It is used here to delay the execution of 'check_last_value' function.
# 'delayed' is a function provided by the joblib library. It is a simple and clever way to specify a function to be called and arguments to be used, without actually calling the function immediately. This is particularly useful when we want to parallelize the execution of a function across multiple cores or processors. By using 'delayed', we can specify all the function calls we want to make in advance, and then let joblib handle the parallelization for us. This can lead to significant performance improvements, especially for computationally intensive tasks.

# The 'check_last_value' function is called with the argument 'df' (our dataframe).
# The for loop '_ in range(2)' is used to specify the number of times the function should be called, in this case, twice.
Parallel(n_jobs=2)( delayed(func)(df) for func in [check_first_value, check_last_value] )
