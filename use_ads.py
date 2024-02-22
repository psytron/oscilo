


import ads


# uses loop to read 
import time
start_time = time.time()
iterations = 0
while True:
    #print(ads.readzero())
    z = ads.readzero()
    iterations += 1
    if time.time() - start_time >= 1:
        print(f"Iterations per second: {iterations}")
        iterations = 0
        start_time = time.time()

#ads.stream_to_address_on_port('Alophants-Air.lan', 65432 )