


# In the first Python interactive shell
from multiprocessing import shared_memory
import numpy as np

###

a = np.array([1, 3, 8])  # Start with an existing NumPy array
shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
b[:] = a[:]  # Copy the original data into shared memory


 
####
existing_shm = shared_memory.SharedMemory(name='xor')
c = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)


existing_shm.close()
shm.close()
shm.unlink()  # Free and release the shared memory block at the very end
