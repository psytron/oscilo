





import time

def measure_iterations_per_second():
    start_time = time.time()
    iterations = 0
    while True:
        iterations += 1
        end_time = time.time()
        if end_time - start_time >= 1:  # If more than a second has passed
            print(f"Iterations per second       : {iterations}")  
            print(f"Iterations per second in KHz: {iterations / 1_000:.3f}")
            print(f"Iterations per second in MHz: {iterations / 1_000_000:.6f}")
            print(f"Iterations per second in GHz: {iterations / 1_000_000_000:.9f}")                                           
            iterations = 0
            start_time = time.time()

if __name__ == "__main__":
    measure_iterations_per_second()
