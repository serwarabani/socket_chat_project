import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print("Server is listening...")

client_socket, client_address = server.accept()

print(f"Connected to {client_address}")

message = client_socket.recv(1024).decode()

print(message)

client_socket.send("hello client".encode())

client_socket.close()

server.close()