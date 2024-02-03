

import psutil
import platform

cpu_info = platform.processor()
print(f"CPU type: {cpu_info}")

def print_cpu_utilization():
    cpu_percentages = psutil.cpu_percent(percpu=True, interval=1)
    print('\n\n')
    for i, percentage in enumerate(cpu_percentages):
        print("Core: ",i,' ',percentage)
        
import os
print(f"PID: {os.getpid()}")

while True: 
    print_cpu_utilization()









