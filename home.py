import socket
import struct

HOST = "localhost"
PORT = 23333
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    m = input("message> ")
    while len(m):
        client_socket.sendall(m.encode())
        data = client_socket.recv(1024)
        
        print("echo> ", struct.unpack('2d',data))
        m = input("message> ")

