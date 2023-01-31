import os
import signal
import subprocess
import time

def handle_sigint(signum, frame):
    print("Received SIGINT, returning int")
    return int

def external_process():
    input_str = input("Enter a string: ")
    if input_str == "zxy":
        os.kill(os.getppid(), signal.CTRL_C_EVENT)

if __name__ == "__main__":
    signal.signal(signal.SIGEOF, handle_sigint)
    proc = subprocess.Popen(["python3", "-c", "import weather; weather.external_process()"])
    while True:
        time.sleep(1)
