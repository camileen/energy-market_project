from multiprocessing import Process
import time

class Season(Process):
    def __init__(self, weather, market):
        super().__init__()
        self.weather = weather
        self.market = market

    # Season Signal ---------------------------------
    def run(self):
        i = 0
        while True:
            self.weather.set()
            self.market.set()
            time.sleep(15)