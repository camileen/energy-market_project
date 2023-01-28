<<<<<<< HEAD
import weather
import season
import time
import market
from market import Market
from weather import Weather
import multiprocessing
from multiprocessing import Process, Value, Array, Lock, Queue, active_children
import signal
import sys
import os

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season

# Signal -----------------
season_change = multiprocessing.Event()
weather_change_return = multiprocessing.Event()
market_change_return = multiprocessing.Event()


# Shared Memory------------
meteo = [0,0]
meteo_shared = Array('i', [0,0])
temperature_flag = Value('i', 0)


# Process-----------------------
weather_object = Weather(meteo_shared,temperature_flag,season_change,weather_change_return)
weather_process = Process(target=weather_object.run)
weather_process.start()

#market_object = Market(meteo_shared,temperature_flag, meteo,season_change,market_change_return)
market_process = Process(target = Market, args=(meteo_shared,temperature_flag, meteo,season_change,market_change_return))
market_process.start()

season_process = Process(target= season.Season, args=(season_change,weather_change_return,market_change_return))
season_process.start()


def signal_handler(sig, frame):
    #print("EOF signal received!")
    #os.kill(market_process.pid(),sig)
    #market_process.kill()
    for child in active_children():
        child.kill()

signal.signal(signal.SIGINT, signal_handler)





=======
import weather
import season
import time
import market
from market import Market
from weather import Weather
import multiprocessing
from multiprocessing import Process, Value, Array, Lock, Queue

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season

# Signal -----------------
season_change = multiprocessing.Event()
weather_change_return = multiprocessing.Event()
market_change_return = multiprocessing.Event()


# Shared Memory------------
meteo = [0,0]
meteo_shared = Array('i', [0,0])
temperature_flag = Value('i', 0)


# Process-----------------------
market_object = Market(meteo_shared,temperature_flag, meteo,season_change,market_change_return)
market_process = Process(target = market_object.run)
market_process.start()

weather_object = Weather(meteo_shared,temperature_flag,season_change,weather_change_return)
weather_process = Process(target=weather_object.run)
weather_process.start()

season_process = Process(target= season.Season, args=(season_change,weather_change_return,market_change_return))
season_process.start()





>>>>>>> 762d40c72f6f9dd5625ac3ba4081747edae52061
