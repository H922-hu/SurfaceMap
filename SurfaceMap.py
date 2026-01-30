import socket
import random
import threading
import queue
import time
import os

PORTS = [                                       #Add or remove ports as needed
    21
]
TIMEOUT = 2
THREADS = 100
OUTPUT_FILE = "alive_ips.txt"
q = queue.Queue()
lock = threading.Lock()
active_count = 0
unacceptable_count = 0
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
def clear():
    os.system("clear" if os.name == "posix" else "cls")
def banner():
    clear()
    print(RED + r"""
 ____              __                __  __             
/ ___| _   _ _ __ / _| __ _  ___ ___|  \/  | __ _ _ __  
\___ \| | | | '__| |_ / _` |/ __/ _ \ |\/| |/ _` | '_ \ 
 ___) | |_| | |  |  _| (_| | (_|  __/ |  | | (_| | |_) |
|____/ \__,_|_|  |_|  \__,_|\___\___|_|  |_|\__,_| .__/ 
                                                 |_|    
        
                    """ + RESET)
    print(f"{GREEN}Active: {active_count}   Unacceptable: {unacceptable_count}{RESET}\n")
def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))
def check_ip():
    global active_count, unacceptable_count
    while True:
        ip = q.get()
        connected = False
        for port in PORTS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(TIMEOUT)
                s.connect((ip, port))
                s.close()
                with lock:
                    active_count += 1
                    banner()
                    print(f"{GREEN}[ OK ] {ip}:{port}{RESET}")
                    with open(OUTPUT_FILE, "a") as f:
                        f.write(f"{ip}:{port}\n")
                connected = True
                break
            except:
                pass
        if not connected:
            with lock:
                unacceptable_count += 1
                banner()
        q.task_done()
for _ in range(THREADS):
    t = threading.Thread(target=check_ip, daemon=True)
    t.start()
banner()
print("[*] ScIP Scanner Started ...\n")
try:
    while True:
        q.put(random_ip())
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\n[!] Stopped by user")
