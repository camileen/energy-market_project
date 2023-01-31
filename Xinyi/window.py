import tkinter as tk
import signal
import os

class Window:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Finger of GOD")
        self.root.geometry("300x100")

        # Create a submit button
        self.submit_button = tk.Button(self.root, text="Crise!!!", command=self.crise)
        self.submit_button.pack()

        self.submit_button = tk.Button(self.root, text="Promotion", command=self.promotion)
        self.submit_button.pack()

        # Start the main event loop
        self.root.mainloop()
        
    def crise(self):
        os.kill(os.getppid(), signal.SIGUSR1)

    def promotion(self):
        os.kill(os.getppid(), signal.SIGUSR2)