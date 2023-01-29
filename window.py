import tkinter as tk
import signal
import os

class Window:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Get User Input")

        # Create an entry field for user input
        self.entry = tk.Entry(self.root)
        self.entry.pack()

        # Create a submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack()

        # Start the main event loop
        self.root.mainloop()
        
    def on_submit(self):
        user_input = self.entry.get()
        #print(f"User entered: {user_input}")
        if user_input == "send":
            os.kill(os.getppid(), signal.SIGUSR1)