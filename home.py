import socket
import struct
import random
import sys
import sysv_ipc
from multiprocessing import Process

# HOST = "localhost"
# PORT = 23333
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#     client_socket.connect((HOST, PORT))
#     m = input("message> ")
#     while len(m):
#         client_socket.sendall(m.encode())
#         data = client_socket.recv(1024)
        
#         print("echo> ", struct.unpack('2d',data))
#         m = input("message> ")

key_need = 123
# key_give = 321

class Home:
    def __init__(self):
        self.mq_need = sysv_ipc.MessageQueue(key_need, sysv_ipc.IPC_CREAT)
        #self.mq_give = sys_ipc.MessageQueue(key_give, sysv_ipc.IPC_CREAT)
        self.home1_process = Process(target= self.home_1)
        self.home2_process = Process(target= self.home_2)
        self.home1_process.start()
        self.home2_process.start()


    def home_1(self):
        stockage = 0
        while True:
            #production = random(0,10)
            #consommation = random(0,10)
            #stockage = stockage + production - consommation
            stockage = -3 
            if (stockage > 0) :
                m,t = mq.receive(type=1)
                dt = m.decode()
                print("Receive demande:", dt)
                m,t = self.mq_need.recieve()
                if t == 1:
                    dt = str(stockage).encode()
                    self.mq_need.send(message, type=2)
            if (stockage < 0) :
                message = str(stockage).encode()
                self.mq_need.send(message, type=1)
                m,t = self.mq_need.receive(type=2)
                dt = m.decode()
                print("Receive:", dt)
                

    def home_2(self):
        stockage = 0
        while True:
            #production = random(0,10)
            #consommation = random(0,10)
            #stockage = stockage + production - consommation
            stockage = 3
            if stockage > 0 :
                m,t = mq.receive(type=1)
                dt = m.decode()
                print("Receive demande:", dt)
                m,t = self.mq_need.recieve()
                if t == 1:
                    dt = str(stockage).encode()
                    self.mq_need.send(message, type=2)
            if stockage < 0 :
                message = str(stockage).encode()
                mq.send(message, type=1)
                m,t = mq.receive(type=2)
                dt = m.decode()
                print("Receive give: ", dt)

