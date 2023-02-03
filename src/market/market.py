from multiprocessing import Process, Lock, active_children
from threading import Thread
import socket
import struct
import signal
import sys

from external.god import God
from end.end import print_children

season_list = ["Spring", "Summer", "Automn", "Winter"]
mutex = Lock()

T_CONSTANT = 0.001   # temperature
R_CONSTANT = 0.002   # rain
E_CONSTANT = 0.01    # source
S_COMSTANT = 0.1     # season
PRICE = 1.45
PRICE_THRESHOLD = 0.1

HOST = "localhost"
PORT = 23333

#counter
buy = 0
sell = 0


# ---------------------------- Market ---------------------------------------------------------
class Market(Process):
    def __init__(self,shared_meteo,weather_update, market_change_return ):
        super().__init__()
        self.shared_meteo = shared_meteo
        self.weather_update = weather_update
        self.market_change_return = market_change_return
        self.price = PRICE
        self.buy = buy
        self.sell = sell
        
    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler1)

        self.show_season = Process(target=self.get_season, name="Show-season")
        self.show_season.start()
        self.show_weather = Thread(target=self.get_weather)
        self.show_weather.start()

        self.socket = Thread(target=self.market_socket)
        self.socket.start()
        
        signal.signal(signal.SIGUSR1, self.signal_handler_crise)
        signal.signal(signal.SIGUSR2, self.signal_handler_promotion)
        self.external_process = Process(target=God, name="God")
        self.external_process.start()

        print_children("****** Children of market: ******")

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
        #print("------------------- Connected to client: ", address)
        data = client_socket.recv(16)
        #print("Server receive:", struct.unpack('2d',data))
        if struct.unpack('2d',data)[1] == 0.0:
            self.buy +=1
            print("--------------------------------Market receive a BUY demande")
        else :
            self.sell +=1
            print("--------------------------------Market receive a SELL demande")
        #price = round(self.get_price(), 4)
        message = [self.price,0]
        data_send = struct.pack('2d',*message)
        client_socket.send(data_send)
        #print("------------------- Disconnecting from client: ", address)
        #client_socket.close()
        if (self.buy - self.sell >= 3):
            print("--------------------------------many buy demande ---- price increase!!!")
            self.price += 0.2
            self.buy = 0
            self.sell = 0
        elif (self.sell - self.buy >= 3):
            print("--------------------------------many sell demande ---- price reduction!!!")
            self.price -= 0.2
            self.buy = 0
            self.sell = 0
        

    def signal_handler_crise(self,signum, frame):
        print("--------------------------------Crise recieve!!!")
        self.price += 0.5
        print("crise: ---------------",self.price)
        #os.kill(self.childProcess.pid, signal.SIGKILL)

    def signal_handler_promotion(self,signum, frame):
        print("--------------------------------Promotion recieve!!!")
        if (self.price > PRICE_THRESHOLD):
            self.price -= 0.5
            print("promo: ---------------",self.price)
            #os.kill(self.childProcess.pid, signal.SIGKILL)
        else:
            print("promo: ---------------","Even God can't create negative price...")

    
    # Signal ----------------------
    def signal_handler1(self, sig,frame):
        #external.external.Window.show_window(external.external.Window)
        for child in active_children():
            child.kill()
        print("Exit!!! Market")
        sys.exit(0)
