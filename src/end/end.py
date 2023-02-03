from multiprocessing import active_children
import signal
import sys

# Signal ----------------------
def signal_handler(sig, frame):
    for child in active_children():
        child.terminate()
    print("Exit!!!")
    sys.exit(0)

def print_children(whos_children):
    print(whos_children)
    for child in active_children():
        print(child.name)


