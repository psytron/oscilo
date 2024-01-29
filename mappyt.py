
# Memory-mapped files allow you to map the contents of a file directly into the memory space of your application. This can be an efficient way of reading and writing files, as well as sharing data between multiple processes. Python's mmap module provides an interface for memory-mapped files. Here's how you can use it:

# 1. Create or Open a File: First, you need a file to map. You can use an existing file or create a new one and make sure it's large enough to hold the data you plan to share.

# 2. Map the File to Memory: Use the mmap module to create a memory-mapped object that represents the file.

# 3. Access the Memory-Mapped File: Once the file is mapped, you can access and manipulate the data as if it were a bytearray.

# 4. Synchronize Changes: If you modify the contents of the memory-mapped object, you can synchronize the changes back to the file.

# Here's an example of how to create a memory-mapped file and write to it:

import mmap
import os

# Size of the memory-mapped file
size = 1000

# Open the file for reading and writing
with open('example.dat', 'wb') as f:
    # Ensure the file is the right size
    f.seek(size - 1)
    f.write(b'\x00')

# Now open the file again and create a memory-mapped object
with open('example.dat', 'r+b') as f:
    # Memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(), 0)
    # Write to the memory-mapped file
    mm[0:11] = b'Hello World'
    # Flush changes to the file
    mm.flush()
    # Access the content via standard file methods
    print(mm.readline())  # prints b'Hello World'
    # Close the memory-mapped file
    mm.close()

# Clean up the file
os.remove('example.dat')



# use it
with open('example.dat', 'r+b') as f:
    mm = mmap.mmap(f.fileno(), 0)
    # Read content via standard file methods
    print(mm[:11])  # prints b'Hello World'
    mm.close()