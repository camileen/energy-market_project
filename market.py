<<<<<<< HEAD
import random
import time
import os
import sys
import weather
import season
import struct
import threading
import multiprocessing
from threading import Thread
from multiprocessing import Process, Lock
import socket

season_list = ["Spring", "Summer", "Automn", "Winter"]
mutex = Lock()
access_price = Lock()

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season

HOST = "localhost"
PORT = 23333


# ---------------------------- Market ---------------------------------------------------------
class Market:
    def __init__(self,meteo_shared,temperature_flag, meteo,season_change, market_change_return ):
        self.meteo_shared = meteo_shared
        self.temperature_flag = temperature_flag
        self.meteo = meteo
        self.season_change = season_change
        self.market_change_return = market_change_return

        self.show_season = Process(target=self.get_season)
        self.show_season.start()
        self.show_weather = Thread(target=self.get_weather)
        self.show_weather.start()
        self.socket = Thread(target=self.handle_socket)
        self.socket.start()

    def get_season(self): 
        i=0
        while True:
            self.market_change_return.wait()
            turn = i % 4
            i += 1
            print("----- Now we are in", season_list[turn],"-----")
            self.market_change_return.clear()

    def get_weather(self):  
        #print("get_weather in process:", os.getpid(), "child de:", os.getppid())
        while True:
            while self.temperature_flag.value == 1:
                #print(weather_flag.value)
                mutex.acquire()
                try:
                    self.temperature_flag.value = 0
                    print("[Temperature, Rain]: ",self.meteo_shared[:])
                finally:
                    mutex.release()

    def get_price(self):
        price = 0.145
        mutex.acquire()
        price = 0.99*price + 0.001*(self.meteo_shared[0]-3*self.meteo_shared[1])
        print("instant price:", price)
        mutex.release()
        return price

    def handle_socket(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((HOST, PORT))
                server_socket.listen()
                client_socket, address = server_socket.accept()
                with client_socket:
                    print("Connected to client: ", address)
                    data = client_socket.recv(8)
                    while len(data):
                        #price = round(self.get_price(), 4)
                        price = self.get_price()
                        message = [price,0]
                        data_send = struct.pack('2d',*message)
                        client_socket.send(data_send)
                        data = client_socket.recv(1024)
                    print("Disconnecting from client: ", address)
    
            
    #def run(self):
        
        

        
        
        

        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        #     server_socket.setblocking(False)
        #     server_socket.bind((HOST, PORT))
        #     server_socket.listen(2)
        #     while serve:
        #         readable, writable, error = select.select([server_socket], [], [], 1)
        #         if server_socket in readable:
        #             client_socket, address = server_socket.accept()
        #             p = Process(target=client_handler, args=(client_socket, address))
        #             p.start()
    

=======
import random
import time
import os
import sys
import weather
import season
import struct
import threading
import multiprocessing
from threading import Thread
from multiprocessing import Process, Lock
import socket

season_list = ["Spring", "Summer", "Automn", "Winter"]
mutex = Lock()
access_price = Lock()

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season

HOST = "localhost"
PORT = 6666


# ---------------------------- Market ---------------------------------------------------------
class Market:
    def __init__(self,meteo_shared,temperature_flag, meteo,season_change, market_change_return ):
        self.meteo_shared = meteo_shared
        self.temperature_flag = temperature_flag
        self.meteo = meteo
        self.season_change = season_change
        self.market_change_return = market_change_return

    def get_season(self): 
        i=0
        while True:
            self.market_change_return.wait()
            turn = i % 4
            i += 1
            print("----- Now we are in", season_list[turn],"-----")
            self.market_change_return.clear()

    def get_weather(self):  
        #print("get_weather in process:", os.getpid(), "child de:", os.getppid())
        while True:
            while self.temperature_flag.value == 1:
                #print(weather_flag.value)
                mutex.acquire()
                try:
                    self.temperature_flag.value = 0
                    print("[Temperature, Rain]: ",self.meteo_shared[:])
                finally:
                    mutex.release()

    def get_price(self):
        price = 0.145
        mutex.acquire()
        price = 0.99*price + 0.001*(1/self.meteo_shared[0]-1/self.meteo_shared[1])
        print("instant price:", price)
        mutex.release()
        return price

    # def handle_socket(self):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    #         server_socket.bind((HOST, PORT))
    #         server_socket.listen()
    #         client_socket, address = server_socket.accept()
    #         with client_socket:
    #             print("Connected to client: ", address)
    #             data = client_socket.recv(1024)
    #             while len(data):
    #                 message = self.get_price()
    #                 client_socket.sendall(message.encode())
    #                 data = client_socket.recv(1024)
    #             print("Disconnecting from client: ", address)
    
            
    def run(self):
        
        self.show_season = Thread(target=self.get_season)
        self.show_season.start()
        self.show_weather = Thread(target=self.get_weather)
        self.show_weather.start()

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((HOST, PORT))
                server_socket.listen()
                client_socket, address = server_socket.accept()
                with client_socket:
                    print("Connected to client: ", address)
                    data = client_socket.recv(1024)
                    while len(data):
                        price = round(self.get_price(), 4)
                        message = [price,0]
                        data_send = struct.pack('<2f',*message)
                        client_socket.send(data_send)
                        data = client_socket.recv(1024)
                    print("Disconnecting from client: ", address)
        
        

        
    

>>>>>>> 762d40c72f6f9dd5625ac3ba4081747edae52061
    