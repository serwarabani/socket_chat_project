import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[*] Server is running on {HOST}:{PORT}...")

clients = {}
chat_history = []  
MAX_HISTORY = 50   
clients_lock = threading.Lock()

def broadcast(message):
    global chat_history
    with clients_lock:
        chat_history.append(message)
        if len(chat_history) > MAX_HISTORY:
            chat_history.pop(0)
            
        for client in list(clients.keys()):
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.pop(client, None)

def handle_client(client_socket, client_address):
    ip = client_address[0]
    username = "Unknown"
    
    try:
        username = client_socket.recv(1024).decode('utf-8')
        
        with clients_lock:
            clients[client_socket] = {'ip': ip, 'username': username}
            current_count = len(clients)
            
        print(f"[NEW CONNECTION] {username} connected from {ip}")
        
        if chat_history:
            client_socket.send("System: Loading chat history...\n-----------------------\n".encode('utf-8'))
            for past_msg in chat_history:
                client_socket.send((past_msg + "\n").encode('utf-8'))
            client_socket.send("-----------------------\n".encode('utf-8'))

        broadcast(f"System: {username} has joined the chat! ({current_count} users online)")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message or message == "/exit":
                break

            if message.startswith(">pm"):
                parts = message.split(maxsplit=2)
                if len(parts) < 3:
                    client_socket.send("System: Use: >pm <username> <message>\n".encode('utf-8'))
                    continue
                
                target_username = parts[1].strip()
                pm_message = parts[2].strip()
                sent = False
                
                with clients_lock:
                    for c, info in clients.items():
                        if info['username'] == target_username:
                            c.send(f"[PM from {username}]: {pm_message}".encode('utf-8'))
                            sent = True
                            break
                
                if not sent:
                    client_socket.send(f"System: No user found with username {target_username}\n".encode('utf-8'))
                else:
                    client_socket.send(f"[PM to {target_username}]: {pm_message}".encode('utf-8'))
                continue

            if message.strip() == ">show_ips":
                with clients_lock:
                    user_list = "\n".join([f"- {info['username']}: {info['ip']}" for c, info in clients.items()])
                client_socket.send(f"\n--- Connected Users & IPs ---\n{user_list}\n-----------------------------\n".encode('utf-8'))
                continue

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {username} ({ip}): {message}"
            print(full_message)
            broadcast(full_message)

    except Exception as e:
        pass
    finally:
        print(f"[DISCONNECTED] {username} - {ip}")
        with clients_lock:
            if client_socket in clients:
                del clients[client_socket]
            current_count = len(clients)
            
        client_socket.close()
        broadcast(f"System: {username} has left the chat. ({current_count} users online)")

while True:
    client_socket, client_address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.daemon = True
    thread.start()