

import threading
import os
import re

def ping_ip(ip):
    response = os.popen(f"ping {ip} -c 1").read()
    latency = re.findall(r"time=\d+.\d+", response)
    latency = latency[0].split('=')[1] if latency else 'unreachable'
    return {'ip': ip, 'latency': latency}

def ping_ips():
    threads = []
    results = []
    for i in range(1, 255):
        for j in range(1, 255):
            ip = f"192.168.{i}.{j}"
            thread = threading.Thread(target=lambda: results.append(ping_ip(ip)))
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()
    return results
