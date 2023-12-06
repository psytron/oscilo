



import time

start_time = time.time()
global elapsed_time
elapsed_time = 0
iterations = 0 
while True:
    elapsed_time
    iterations +=1
    if( elapsed_time > 1):
        elapsed_time = 0
        print( 'FPS: ', iterations )
        iterations = 0
    else:
        elapsed_time = time.time() - start_time 


    print(": ", time.time() - start_time )
