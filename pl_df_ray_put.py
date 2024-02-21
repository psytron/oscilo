

import ray
import polars as pl

# Initialize Ray
ray.init()

# Create a Polars DataFrame to share
df = pl.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

# Put the DataFrame in shared memory with Ray
shared_df = ray.put(df)

# Define a function to update the DataFrame 
@ray.remote
def update_df(row):
    global shared_df
    df = shared_df # Get reference to shared DataFrame

    # Make update        
    df = df.append({"A": [row], "B": [row**2]})  

# Update from several processes simultaneously
refs = [update_df.remote(i) for i in range(10, 15)]
ray.get(refs)

# Retrieve updated DataFrame
df = ray.get(shared_df)
print(df)