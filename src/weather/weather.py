import random
import time
from threading import Thread
from queue import Queue
from multiprocessing import Lock, Process


temp_queue = Queue()

SPRING = 15
SUMMER = 30
AUTUMN = 15
WINTER = 5
season_temp = [SPRING, SUMMER, AUTUMN, WINTER]

class Weather(Process):
    def __init__(self, shared_meteo,weather_update,season_event):
        super().__init__()
        self.shared_meteo = shared_meteo # Array
        self.weather_update = weather_update # Integer 0 or 1
        self.season_event = season_event
    
    def run(self):
        global_temp = Thread(target=self.get_season_temp)
        global_temp.start()
        show_temp = Thread(target=self.temperature)
        show_temp.start()

    def get_season_temp(self):
        turn = 0
        while True:
            self.season_event.wait()
            index = turn % 4
            temp_queue.put(season_temp[index])
            self.season_event.clear()
            turn += 1

    def temperature(self):
        temp = -100
        while True:
            if not temp_queue.empty():
                temp = temp_queue.get()
            if temp != -100:
                with self.shared_meteo.get_lock():
                    self.shared_meteo[0] = temp + random.randint(-10, 10)  # temperature
                    self.shared_meteo[1] = random.randint(0,5)    # rain
                    self.weather_update.value = 1    
                time.sleep(5)

