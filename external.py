import os
import signal
import subprocess

def handle_sigusr1(signum, frame):
    print("Received SIGUSR1, returning int")
    return int

def external_process():
    input_str = input("Enter a string: ")
    if input_str == "zxy":
        os.kill(os.getppid(), signal.SIGUSR1)

if __name__ == "__main__":
    signal.signal(signal.SIGUSR1, handle_sigusr1)
    proc = subprocess.Popen(["python", "-c", "import example; example.external_process()"])
    signal.pause()
