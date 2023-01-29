# import os
# import signal
# import subprocess

# def handle_sigusr1(signum, frame):
#     print("Received SIGUSR1, returning int")
#     return int

# def external_process():
#     input_str = input("Enter a string: ")
#     if input_str == "zxy":
#         os.kill(os.getppid(), signal.SIGUSR1)

# if __name__ == "__main__":
#     signal.signal(signal.SIGUSR1, handle_sigusr1)
#     proc = subprocess.Popen(["python", "-c", "import external; external.external_process()"])
#     signal.pause()

# import signal
# import time

# def signal_handler(signum, frame):
#     print("Signal Number:", signum, "Frame: ", frame)

# def exit_handler(signum, frame):
#     print("Exiting...")
#     exit(0)

# signal.signal(signal.SIGINT, signal_handler)

# signal.signal(signal.SIGTSTP, exit_handler)

# while 1:
#     print("Enter something.")
#     time.sleep(3)
# import signal
# import os
# import sys
# import termios
# import tty

# def handle_sigusr1(signum, frame):
#     print("Received SIGUSR1, returning int")
#     return int

# def getch():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(fd)
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch

# if __name__ == "__main__":
#     signal.signal(signal.SIGUSR1, handle_sigusr1)
#     while True:
#         ch = getch()
#         if ch == '\x01': # Ctrl+A
#             os.kill(os.getpid(), signal.SIGUSR1)

import os
import signal
import market

print("market process id:", market.pid())

pid = int(input("Enter the PID of the receiver process: "))

os.kill(pid, signal.SIGUSR1)
print("Signal sent!")

            




