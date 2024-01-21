




import pandas as pd
import numpy as np

from joblib import Parallel, delayed, parallel_backend
from numpy.random import choice
import pkg_resources
import platform
import argparse
import time

def compute_sum_df(df,col,dummy)->float:
    t=0.0
    for n in range(50):
        t+=df[col].sum()
    return t
    
def sys_info(huge_dict:bool)->str:
    uname=platform.uname()
    
    versions=''
    for package in 'pandas joblib'.split():
        versions+=f"{package}: {pkg_resources.get_distribution(package).version} "
        
    print(f"Running with huge_dict={huge_dict} on {uname.system} {uname.release} {uname.processor} ({versions})")

if __name__ == "__main__":          

        
    parser = argparse.ArgumentParser()
    parser.add_argument('--huge_dict', type=int, default=False, help='Pass huge dict along with big dataframe') 
    args = parser.parse_args()
    print(args.huge_dict)    
    
    sys_info(args.huge_dict)

    ncols=10
    cols_names=np.array(list(map(str,range(ncols))))
    
    df = pd.DataFrame(np.random.randn(10_000_000, ncols), columns=cols_names)
    
    n_jobs=20
    
    k=100_000
    huge_dict=dict(zip(np.arange(k),np.random.rand(k,1)))

    start = time.time()
    
    results = Parallel(n_jobs=n_jobs, backend='loky', prefer='processes', temp_folder=r"R:/Temp/")(
        delayed(compute_sum_df)(
            df=df,col=col,dummy=huge_dict if args.huge_dict==1 else None
        )
        for col in cols_names[choice(ncols,n_jobs)])        
    
    end = time.time()
    print(f"Done! Time spent={end - start:.1f}s.")