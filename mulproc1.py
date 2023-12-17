


# importing Python multiprocessing module

import multiprocessing

def prnt_cu(n):
    for x in range( 1000000 ):
        print("Cube: {}".format(n * n * n))

def prnt_squ(n):
    for x in range( 1000000 ):
        print("Square: {}".format(n * n))


cores = 2 
if( cores > 1 ):
    # creating multiple processes
    proc1 = multiprocessing.Process(target=prnt_squ, args=(5, ))
    proc2 = multiprocessing.Process(target=prnt_cu, args=(5, ))

    # Initiating process 1
    proc1.start()

    # Initiating process 2
    proc2.start()

    # Waiting until proc1 finishes
    proc1.join()

    # Waiting until proc2 finishes
    proc2.join()

else:
    prnt_squ(5)
    prnt_cu(5)

    # Processes finished

print("Completed!")