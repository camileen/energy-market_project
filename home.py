import socket
import struct
import random
import time
import sys
import sysv_ipc
from multiprocessing import Process


HOST = "localhost"
PORT = 23333

key_need = 123
key_give = 321

class Home:
    def __init__(self):
        #self.mq_need = sysv_ipc.MessageQueue(key_need, sysv_ipc.IPC_CREAT)
        self.mq_give = sysv_ipc.MessageQueue(key_give, sysv_ipc.IPC_CREAT)
        self.home1_process = Process(target= self.home_1)
        self.home2_process = Process(target= self.home_2)
        self.home3_process = Process(target= self.home_3)
        self.home1_process.start()
        time.sleep(1)
        self.home2_process.start()
        time.sleep(1)
        self.home3_process.start()
        self.host = HOST
        self.port = PORT


    def home_1(self):
        stockage = 0
        money = 10
        while True:
            production = random.randint(0,10)
            consommation = random.randint(0,10)
            stockage = stockage + production - consommation
            print("Home 1 stockage:", stockage)
            while (stockage < 0) :
                print("Home 1 need help!")
                if self.mq_give.current_messages != 0 :
                    m,t = self.mq_give.receive(type=1)
                    dt = m.decode()
                    print("Home 1 Receive Help:", dt)
                    stockage += int(dt)
                    print("Home 1 stockage:", stockage, "with help")
                else :
                    # buy from market
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((HOST, PORT))
                        message = [stockage, 0]
                        data_send = struct.pack('2d', *message)
                        client_socket.send(data_send)
                        data = client_socket.recv(16)
                        print("Home 1 Buy: ", -stockage,"energy from Market with Price", struct.unpack('2d',data)[0])
                        #print("Price", struct.unpack('2d',data)[0])
                        money -= (-stockage) * struct.unpack('2d',data)[0]
                        print("Home 1 have", money, "left")
                        stockage = 0
                        client_socket.close()
            if (stockage > 3) :
                message = str(stockage-3).encode()
                self.mq_give.send(message, type=1)
                print("Home 1 give",stockage-3,"to his neighbor.")
            
            print("---------------------------")
            time.sleep(10)

    def home_2(self):
        stockage = 0
        money = 10
        while True:
            production = random.randint(0,10)
            consommation = random.randint(0,10)
            stockage = stockage + production - consommation
            print("Home 2 stockage:", stockage)
            if (stockage < 0) :
                print("Home 2 need help!")
                if self.mq_give.current_messages != 0 :
                    m,t = self.mq_give.receive(type=1)
                    dt = m.decode()
                    print("Home 2 Receive Help:", dt)
                    m,t = self.mq_give.receive()
                    stockage += int(dt)
                else :
                    # buy from market
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((HOST, PORT))
                        message = [stockage, 0]
                        data_send = struct.pack('2d', *message)
                        client_socket.send(data_send)
                        data = client_socket.recv(16)
                        print("Home 2 Buy: ", -stockage,"energy from Market with Price", struct.unpack('2d',data)[0])
                        #print("Price", struct.unpack('2d',data)[0])
                        money = money -(-stockage) * struct.unpack('2d',data)[0]
                        print("Home 2 have", money, "left")
                        stockage = 0
                        client_socket.close()
                    
            if (stockage > 3) :
                # sell to market
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((HOST, PORT))
                    message = [stockage, 0]
                    data_send = struct.pack('2d', *message)
                    client_socket.send(data_send)
                    data = client_socket.recv(16)
                    print("Home 2 Sell: ", stockage - 3,"energy from Market with Price", struct.unpack('2d',data)[0])
                    #print("Price", struct.unpack('2d',data)[0])
                    money += (stockage - 3) * struct.unpack('2d',data)[0]
                    print("Home 2 have", money, "left")
                    stockage = 0
                    client_socket.close()
            print("---------------------------")
            time.sleep(10)

    def home_3(self):
        stockage = 0
        money = 10
        while True:
            production = random.randint(0,10)
            consommation = random.randint(0,10)
            stockage = stockage + production - consommation
            print("Home 3 stockage:", stockage)
            if (stockage < 0) :
                print("Home 3 need help!")
                if self.mq_give.current_messages != 0 :
                    m,t = self.mq_give.receive(type=1)
                    dt = m.decode()
                    print("Home 3 Receive Help:", dt)
                    m,t = self.mq_give.receive()
                    stockage += int(dt)
                else :
                    # buy from market
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((HOST, PORT))
                        message = [stockage, 0]
                        data_send = struct.pack('2d', *message)
                        client_socket.send(data_send)
                        data = client_socket.recv(16)
                        print("Home 3 Buy: ", -stockage,"energy from Market with Price", struct.unpack('2d',data)[0])
                        #print("Price", struct.unpack('2d',data)[0])
                        money = money -(-stockage) * struct.unpack('2d',data)[0]
                        print("Home 3 have", money, "left")
                        stockage = 0
                        client_socket.close()
                    
            if (stockage > 3) :
                if self.mq_give.current_messages == 0 :
                    message = str(stockage-3).encode()
                    self.mq_give.send(message, type=1)
                    print("Home 3 give",stockage-3,"to his neighbor.")
                else :
                     # sell to market
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((HOST, PORT))
                        message = [stockage, 0]
                        data_send = struct.pack('2d', *message)
                        client_socket.send(data_send)
                        data = client_socket.recv(16)
                        print("Home 3 Sell: ", stockage - 3,"energy from Market with Price", struct.unpack('2d',data)[0])
                        #print("Price", struct.unpack('2d',data)[0])
                        money += (stockage - 3) * struct.unpack('2d',data)[0]
                        print("Home 3 have", money, "left")
                        stockage = 0
                        client_socket.close()
            print("---------------------------")
            time.sleep(10)

if __name__ == "__main__":
    home_objet = Home()

