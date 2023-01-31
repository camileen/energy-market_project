from multiprocessing import Process, Event, active_children, Array, Value
import signal

from weather.weather import Weather
from season.season import Season
from market.market import Market
import end.end as end

# Event -----------------
weather_change_return = Event()
market_change_return = Event()

# Signal -----------------
signal.signal(signal.SIGINT, end.signal_handler)

# Shared Memory------------
meteo = [0,0]
meteo_shared = Array('i', [0,0])
temperature_flag = Value('i', 0)


# Process-----------------------
weather_object = Weather(meteo_shared,temperature_flag,weather_change_return)
weather_process = Process(target=weather_object.run)
weather_process.start()

market_process = Process(target = Market, args=(meteo_shared,temperature_flag, market_change_return ))
market_process.start()

season_process = Process(target= Season, args=(weather_change_return,market_change_return))
season_process.start()

signal.pause()
