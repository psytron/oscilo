


import random
import time


def matrix_multiplication(a, b):
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result


def measure_ghz():
    start_time = time.time()
    iterations = 0
    while True:
        iterations += 1
       # Create two 2x2 matrices
        a = [[random.randint(0, 99) for _ in range(2)] for _ in range(2)]
        b = [[random.randint(0, 99) for _ in range(2)] for _ in range(2)]
        res = matrix_multiplication(a, b)

        end_time = time.time()
        if end_time - start_time >= 1:  # If more than a second has passed
            print(f" ")  
            print(f" ")  
            print(f"Python ")  
            print(f"Hz       : {iterations}")  
            print(f"Hz in KHz: {iterations / 1_000:.3f}")
            print(f"Hz in MHz: {iterations / 1_000_000:.6f}")
            print(f"Hz in GHz: {iterations / 1_000_000_000:.9f}") 
            print(f"   Result: ", res[0][0],res[0][1],res[1][0],res[1][1])                                          
            iterations = 0
            start_time = time.time()
            
if __name__ == "__main__":
    measure_ghz()
