import random
import time
import os
import sys
import weather
import season
import struct
import threading
import multiprocessing
import signal
from threading import Thread
from multiprocessing import Process, Lock, active_children
import socket
import termios
import tty
import external

season_list = ["Spring", "Summer", "Automn", "Winter"]
mutex = Lock()
access_price = Lock()

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season
PRICE = 1.45

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
        self.price = PRICE

        #signal.signal(signal.SIGTERM, self.signal_handler1)

        #print("Market Process id:" , os.getpid())
        self.show_season = Process(target=self.get_season)
        self.show_season.start()
        self.show_weather = Thread(target=self.get_weather)
        self.show_weather.start()

        self.socket = Thread(target=self.market_socket)
        self.socket.start()
        
        signal.signal(signal.SIGUSR1, self.signal_handler_crise)
        signal.signal(signal.SIGUSR2, self.signal_handler_promotion)
        self.external_object = external.Window()
        self.external_process = Process(target=self.external_object)
        self.external_process.start()
        #self.external_process.join()

        

        self.market_socket()


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
                    self.get_price()
                finally:
                    mutex.release()

    def get_price(self):
        self.price = 0.99*self.price + 0.001*(self.meteo_shared[0]-3*self.meteo_shared[1])
        print("instant price:", self.price)
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
        print("------------------- Connected to client: ", address)
        data = client_socket.recv(16)
        print("Server receive:", struct.unpack('2d',data))
        while len(data):
            #price = round(self.get_price(), 4)
            message = [self.price,0]
            data_send = struct.pack('2d',*message)
            client_socket.send(data_send)
            data = client_socket.recv(1024)
        print("------------------- Disconnecting from client: ", address)
        #client_socket.close()



    def signal_handler_crise(self,signum, frame):
        print("Crise recieve!!!")
        self.price += 0.5
        print("crise: ---------------",self.price)
        #os.kill(self.childProcess.pid, signal.SIGKILL)

    def signal_handler_promotion(self,signum, frame):
        print("Promotion recieve!!!")
        self.price -= 0.5
        print("promo: ---------------",self.price)
        #os.kill(self.childProcess.pid, signal.SIGKILL)

    
    # Signal ----------------------
    def signal_handler1(self, sig,frame):
        self.external_object.root.lift()
        for child in active_children():
            child.kill()
        print("Exit!!!")
        sys.exit(0)

    
    

    