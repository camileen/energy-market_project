<<<<<<< HEAD
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


=======
import socket
import struct

HOST = "localhost"
PORT = 6666
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    m = input("message> ")
    while len(m):
        client_socket.sendall(m.encode())
        data = client_socket.recv(1024)
        
        print("echo> ", struct.unpack('<2f',data))
        m = input("message> ")


 

    


>>>>>>> 762d40c72f6f9dd5625ac3ba4081747edae52061
