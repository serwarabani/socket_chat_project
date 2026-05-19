import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print("Server is running...")

clients = []


def broadcast(message, sender_socket):

    for client in clients:

        if client != sender_socket:

            try:
                client.send(message.encode())

            except:
                client.close()

                if client in clients:
                    clients.remove(client)


def handle_client(client_socket, client_address):

    print(f"[NEW CONNECTION] {client_address}")

    clients.append(client_socket)

    while True:

        try:

            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message == "/exit":
                break

            full_message = f"{client_address[0]}: {message}"

            print(full_message)

            broadcast(full_message, client_socket)

        except:
            break

    print(f"[DISCONNECTED] {client_address}")

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()


while True:

    client_socket, client_address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    thread.start()