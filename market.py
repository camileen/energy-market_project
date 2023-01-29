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
from multiprocessing import Process, Lock
import socket
import termios
import tty
import window

season_list = ["Spring", "Summer", "Automn", "Winter"]
mutex = Lock()
access_price = Lock()

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season

HOST = "localhost"
PORT = 23334


# ---------------------------- Market ---------------------------------------------------------
class Market:
    def __init__(self,meteo_shared,temperature_flag, meteo,season_change, market_change_return ):
        self.meteo_shared = meteo_shared
        self.temperature_flag = temperature_flag
        self.meteo = meteo
        self.season_change = season_change
        self.market_change_return = market_change_return

        #print("Market Process id:" , os.getpid())
        self.show_season = Process(target=self.get_season)
        self.show_season.start()
        self.show_weather = Thread(target=self.get_weather)
        self.show_weather.start()
        self.socket = Thread(target=self.handle_socket)
        self.socket.start()

        time.sleep(5)
        signal.signal(signal.SIGUSR1, self.signal_handler1)
        self.childProcess = Process(target=window.Window)
        self.childProcess.start()
        self.childProcess.join()
        # self.external_process = Process(target=self.recieve_signal)
        # self.external_process.start() 
        #signal.pause()


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
        price = 0.145
        price = 0.99*price + 0.001*(self.meteo_shared[0]-3*self.meteo_shared[1])
        print("instant price:", price)
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

    def recieve_signal(self):
        while True:
            print("enter something:")
            ch = self.getch()
            if ch == '\x01': # Ctrl+A
                print("got it")
                os.kill(os.getpid(), signal.SIGUSR1)
                time.sleep(2)

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def signal_handler1(self,signum, frame):
        print("Signal recieve!!!")
        #os.kill(self.childProcess.pid, signal.SIGKILL)

    
    

    