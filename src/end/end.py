from multiprocessing import active_children
import sys

# Signal ----------------------
def signal_handler(sig, frame):
    for child in active_children():
        print("Terminated:", child.name)
        child.terminate()
    sys.exit(0)




