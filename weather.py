import random
import time
from threading import Thread
from queue import Queue
from multiprocessing import Process, Value, Array, Lock

mutex = Lock()
temp_queue = Queue()

season_temp = [15, 30, 15, 5]
class Weather:
    def __init__(self, meteo_shared,temperature_flag,season_change,weather_change_return):
        self.meteo_shared = meteo_shared
        self.temperature_flag = temperature_flag
        self.season_change = season_change
        self.weather_change_return = weather_change_return

    def basic_temp(self):
        i = 0
        while True:
            self.weather_change_return.wait()
            turn = i % 4
            i += 1
            temp_queue.put(season_temp[turn])
            #print(season_temp[turn])
            self.weather_change_return.clear()

    def temperature(self):
        temp = -100
        while True:
            if not temp_queue.empty():
                temp = temp_queue.get()
            if temp != -100:
                mutex.acquire()
                try:
                    self.meteo_shared[0] = temp + random.randint(-10, 10)  # temperature
                    self.meteo_shared[1] = random.randint(0,5)    # rain
                    #print("real weather:",self.meteo_shared[:])
                    self.temperature_flag.value = 1     # update
                finally:
                    mutex.release()
                time.sleep(5)

    def run(self):
        self.get_basic_temp = Thread(target=self.basic_temp)
        self.get_basic_temp.start()
        self.show_temp = Thread(target=self.temperature)
        self.show_temp.start()


