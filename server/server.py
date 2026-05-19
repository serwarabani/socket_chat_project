import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server is running...")

clients = {}  

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.pop(client, None)

def handle_client(client_socket, client_address):
    try:
        client_socket.send("Enter your username:".encode())
        username = client_socket.recv(1024).decode()
        clients[client_socket] = {'ip': client_address[0], 'username': username}
        print(f"[NEW CONNECTION] {username} - {client_address[0]}")

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

        
            if message == "/exit":
                break

     
            if message.startswith(">pm"):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    client_socket.send("Invalid PM format. Use: >pm <userIP> <message>".encode())
                    continue
                target_ip = parts[1]
                pm_message = parts[2]
                sent = False
                for c in clients:
                    if clients[c]['ip'] == target_ip:
                        c.send(f"Private from {username}: {pm_message}".encode())
                        sent = True
                if not sent:
                    client_socket.send(f"No user found with IP {target_ip}".encode())
                continue

            if message.startswith(">users"):
                user_list = "\n".join([f"{clients[c]['username']} - {clients[c]['ip']}" for c in clients])
                client_socket.send(f"Connected users:\n{user_list}".encode())
                continue

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {username}: {message}"
            print(full_message)
            broadcast(full_message, client_socket)

    except:
        pass

    print(f"[DISCONNECTED] {username} - {client_address[0]}")
    if client_socket in clients:
        clients.pop(client_socket)
    client_socket.close()

while True:
    client_socket, client_address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
    