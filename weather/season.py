import time


# Season Signal ---------------------------------
def Season(weather_change_return,market_change_return):
    i = 0
    while True:
        #season_change.set()
        weather_change_return.set()
        market_change_return.set()

        time.sleep(15)