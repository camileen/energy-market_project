from multiprocessing import Process, Event, active_children, Array, Value
import signal
import sys

from weather.weather import Weather
from season.season import Season
from market.market import Market


T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season

# Event -----------------
season_change = Event()
weather_change_return = Event()
market_change_return = Event()

# Signal ----------------------
def signal_handler(sig, frame):
    for child in active_children():
        child.terminate()
    print("Exit!!!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)




# Shared Memory------------
meteo = [0,0]
meteo_shared = Array('i', [0,0])
temperature_flag = Value('i', 0)


# Process-----------------------
weather_object = Weather(meteo_shared,temperature_flag,season_change,weather_change_return)
weather_process = Process(target=weather_object.run)
weather_process.start()

market_process = Process(target = Market, args=(meteo_shared,temperature_flag, meteo,season_change,market_change_return))
market_process.start()

season_process = Process(target= Season, args=(season_change,weather_change_return,market_change_return))
season_process.start()

signal.pause()




