

from multiprocessing import Process
import time

def worker():
    print("Starting worker")
    time.sleep(5)
    print("Finished worker")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    #p.join()  # Main program will wait until p is done
    print("Main program continues after worker is done")