from multiprocessing import Process, Lock, active_children
from threading import Thread
import socket
import struct
import signal
import sys

from external.god import God

SEASONS = ["Spring", "Summer", "Autumn", "Winter"]

PRICE_THRESHOLD = 0.1
INITIAL_PRICE = 1.45

HOST = "localhost"
PORT = 23333


class Market(Process):
    def __init__(self,shared_meteo,weather_update, market_change_return ):
        super().__init__()
        self.shared_meteo = shared_meteo
        self.weather_update = weather_update
        self.market_change_return = market_change_return
        self.price = INITIAL_PRICE
        self.purchases = 0
        self.sales = 0
        
    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler1)
        signal.signal(signal.SIGUSR1, self.signal_handler_crise)
        signal.signal(signal.SIGUSR2, self.signal_handler_promotion)

        show_season = Thread(target=self.get_season)
        show_season.start()
        show_weather = Thread(target=self.get_weather)
        show_weather.start()
        socket = Thread(target=self.market_socket)
        socket.start()
        
        external_process = God()
        external_process.start()


    def get_season(self): 
        i=0
        while True:
            self.market_change_return.wait()
            turn = i % 4
            i += 1
            print("----- Now we are in", SEASONS[turn],"-----")
            self.market_change_return.clear()

    def get_weather(self):  
        while True:
            if self.weather_update.value == 1:
                with self.shared_meteo.get_lock():
                    print("[Temperature, Rain]: ", self.shared_meteo[:])
                    self.get_price()
                    self.weather_update.value = 0

    def get_price(self):
        self.price = 0.99*self.price + 0.001*(self.shared_meteo[0]-3*self.shared_meteo[1])
        print("instant price:", round(self.price, 2))
        return self.price

    def market_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            while True:
                client_socket, address = server_socket.accept()
                home_socket_thread = Thread(target=self.handle_socket, args=(client_socket, address))
                home_socket_thread.start()

    def handle_socket(self,client_socket, address):
        data = client_socket.recv(16)
        if struct.unpack('2d',data)[1] == 0.0:
            self.purchases +=1
            print("--------------------------------Market receive a BUY demand")
        else :
            self.sales +=1
            print("--------------------------------Market receive a SELL demand")
        message = [self.price,0]
        data_send = struct.pack('2d',*message)
        client_socket.send(data_send)
        if (self.purchases - self.sales >= 3):
            print("--------------------------------many buy demand ---- price increase!!!")
            self.price += 0.2
            self.purchases = 0
            self.sales = 0
        elif (self.sales - self.purchases >= 3):
            print("--------------------------------many sell demand ---- price reduction!!!")
            self.price -= 0.2
            self.purchases = 0
            self.sales = 0
        

    def signal_handler_crise(self,signum, frame):
        print("--------------------------------Crise!!!")
        self.price += 0.5
        print("crise: ---------------",self.price)

    def signal_handler_promotion(self,signum, frame):
        print("--------------------------------Promotion!!!")
        if (self.price - 0.5) > PRICE_THRESHOLD:
            self.price -= 0.5
            print("promo: ---------------",self.price)
        else:
            print("promo: ---------------","Even God can't create negative price...")

    
    # Signal ----------------------
    def signal_handler1(self, sig,frame):
        for child in active_children():
            print("Terminated:", child.name)
            child.kill()
        sys.exit(0)
