from multiprocessing import Event, Array, Value
import signal

from weather.weather import Weather
from weather.season import Season
from market.market import Market
from end.end import signal_handler


# Event -----------------
weather_change_return = Event() # why "return" in the name??
market_change_return = Event()

# Signal -----------------
signal.signal(signal.SIGINT, signal_handler)

# Shared Memory between weather, market and season parallel processes ------------
meteo = [0,0]
meteo_shared = Array('i', [0,0])
temperature_flag = Value('i', 0)

# Process-----------------------
weather = Weather(meteo_shared, temperature_flag, weather_change_return)
weather.start()

market_process = Market(meteo_shared,temperature_flag, market_change_return)
market_process.start()

season_process = Season(weather_change_return,market_change_return)
season_process.start()

signal.pause()