import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server is running...")

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            print(f"{client_address}: {message}")

            client_socket.send("Message received".encode())

        except:
            break

    print(f"[DISCONNECTED] {client_address}")
    client_socket.close()


while True:
    client_socket, client_address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )
    thread.start()