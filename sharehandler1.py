#You can share a pandas dataframe between processes without any memory overhead by creating a data_handler child process. This process receives calls from the other children with specific data requests (i.e. a row, a specific cell, a slice etc..) from your very large dataframe object. Only the data_handler process keeps your dataframe in memory unlike a Manager like Namespace which causes the dataframe to be copied to all child processes. See below for a working example. This can be converted to pool.


import time
import queue
import numpy as np
import pandas as pd
import multiprocessing
from random import randint

#==========================================================
# DATA HANDLER
#==========================================================
def data_handler( queue_c, queue_r, queue_d, n_processes ):

    # Create a big dataframe
    big_df = pd.DataFrame(np.random.randint(
        0,100,size=(100, 4)), columns=list('ABCD'))

    # Handle data requests
    finished = 0
    while finished < n_processes:

        try:
            # Get the index we sent in
            idx = queue_c.get(False)

        except queue.Empty:
            continue
        else:
            if idx == 'finished':
                finished += 1
            else:
                try:
                    # Use the big_df here!
                    B_data = big_df.loc[ idx, 'B' ]

                    # Send back some data
                    queue_r.put(B_data)
                except:
                    pass    

# big_df may need to be deleted at the end. 
#import gc; del big_df; gc.collect()

#==========================================================
# PROCESS DATA
#==========================================================

def process_data( queue_c, queue_r, queue_d):

    data = []

    # Save computer memory with a generator
    generator = ( randint(0,x) for x in range(100) )

    for g in generator:

        """
        Lets make a request by sending
        in the index of the data we want. 
        Keep in mind you may receive another 
        child processes return call, which is
        fine if order isnt important.
        """

        #print(g)

        # Send an index value
        queue_c.put(g)

        # Handle the return call
        while True:
            try:
                return_call = queue_r.get(False)
            except queue.Empty:
                continue
            else:
                data.append(return_call)
                break

    queue_c.put('finished')
    queue_d.put(data)   

#==========================================================
# START MULTIPROCESSING
#==========================================================

def multiprocess( n_processes ):

    combined  = []
    processes = []

    # Create queues
    queue_data = multiprocessing.Queue()
    queue_call = multiprocessing.Queue()
    queue_receive = multiprocessing.Queue()

    for process in range(n_processes): 

        if process == 0:

                # Load your data_handler once here
                p = multiprocessing.Process( target = data_handler, args=(queue_call, queue_receive, queue_data, n_processes))
                processes.append(p)
                p.start()

        p = multiprocessing.Process(target = process_data,
        args=(queue_call, queue_receive, queue_data))
        processes.append(p)
        p.start()

    for i in range(n_processes):
        data_list = queue_data.get()    
        combined += data_list

    for p in processes:
        p.join()    

    # Your B values
    print(combined)


if __name__ == "__main__":

    multiprocess( n_processes = 4 )