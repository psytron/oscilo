


import psutil
import time

# Get the CPU info
cpu_info = psutil.cpu_count(logical=False)
print(f"CPU: {psutil.cpu_info().brand_raw}, Cores: {cpu_info}")

# Continuously update the percentage utilization for each core
while True:
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"Core {i}: {percentage}%")
    time.sleep(1)  # Sleep for 1 second