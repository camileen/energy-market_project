from multiprocessing import Process
from threading import Thread
import tkinter as tk
import signal
import os

class God(Process):
    def __init__(self):
        super().__init__()
    
    def run(self):
        # Create the main window
        root = tk.Tk()
        root.title("Finger of GOD")
        root.geometry("300x100")

        # Create a submit button
        submit_button = tk.Button(root, text="Crise!!!", command=self.crise)
        submit_button.pack()

        submit_button = tk.Button(root, text="Promotion", command=self.promotion)
        submit_button.pack()

        # Start the main event loop
        root.mainloop()

    def crise(self):
        os.kill(os.getppid(), signal.SIGUSR1)

    def promotion(self):
        os.kill(os.getppid(), signal.SIGUSR2)

