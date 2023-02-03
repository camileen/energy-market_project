from multiprocessing import Event, Array, Value
import signal

from end.end import signal_handler
from weather.weather import Weather
from weather.season import Season
from market.market import Market


INITIAL_TEMPERATURE = 0
INITIAL_RAIN = 0

if __name__ == "__main__":
  season_event = [Event(), Event()]
  signal.signal(signal.SIGINT, signal_handler)

  shared_meteo = Array('i', [INITIAL_TEMPERATURE, INITIAL_RAIN])
  weather_update = Value('i', 0) # flag used to detect a change in temperature and rain

  weather = Weather(shared_meteo, weather_update, season_event[0])
  weather.start()

  market_process = Market(shared_meteo, weather_update, season_event[1])
  market_process.start()

  season_process = Season(season_event)
  season_process.start()
