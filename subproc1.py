

import synthbase as syn
from multiprocessing import Process
import random


p = Process(target=syn.runsound)
p.start()
p.join()
print('joi')