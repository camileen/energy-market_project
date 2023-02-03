from multiprocessing import Process
import time

class Season(Process):
    def __init__(self, events):
        super().__init__()
        self.weather = events[0]
        self.market = events[1]

    def run(self):
        i = 0
        while True:
            self.weather.set()
            self.market.set()
            time.sleep(15)