import time


# Season Signal ---------------------------------
def Season(weather_change_return,market_change_return):
    i = 0
    while True:
        #season_change.set()

        weather_change_return.set()
        market_change_return.set()
        #season_change.clear()
        # weather_change_return.wait()
        # market_change_return.wait()
        

        # market_change_return.clear()
        # weather_change_return.clear()
        
        
        time.sleep(15)