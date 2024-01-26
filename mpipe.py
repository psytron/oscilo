



import multiprocessing as mp
import numpy as np
import random
import time

ITER_COUNT = 1000


def get_mcs_diff(ts):
    return round((time.time() - ts) * 1e6, 0)


def main(v, input_pipe):
    for _ in range(ITER_COUNT):
        v.value = time.time()
        input_pipe.send(None)
        time.sleep((0.1 + random.random()) / 100)


if __name__ == "__main__":
    v = mp.Value('d', time.time())
    (ip, op) = mp.Pipe()
    p = mp.Process(target=main, args=(v, ip,))
    measurements = []

    p.start()
    i = 0
    while i < ITER_COUNT:
        op.recv()
        measurements.append(get_mcs_diff(v.value))
        i += 1

    print(np.percentile(measurements, [50, 90, 95, 99], axis=0))
    p.join()

