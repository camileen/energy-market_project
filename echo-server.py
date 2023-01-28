import socket

HOST = "localhost"
PORT = 6666
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        client_socket, address = server_socket.accept()
        with client_socket:
            print("Connected to client: ", address)
            data = client_socket.recv(1024)
            while len(data):
                client_socket.sendall(data)
                data = client_socket.recv(1024)
            print("Disconnecting from client: ", address)

            

            
