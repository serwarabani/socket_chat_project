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
    
    client_socket.send("Enter your username:".encode())
    username = client_socket.recv(1024).decode()
    clients[client_socket] = {'ip': client_address[0], 'username': username}

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

          
            if message.startswith(">pm"):
                
                parts = message.split(" ", 2)
                target_ip = parts[1]
                pm_message = parts[2]
                for c in clients:
                    if clients[c]['ip'] == target_ip:
                        c.send(f"Private from {username}: {pm_message}".encode())
                continue

           
            if message.startswith(">users"):
                user_list = "\n".join([f"{clients[c]['username']} - {clients[c]['ip']}" for c in clients])
                client_socket.send(f"Connected users:\n{user_list}".encode())
                continue

           
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {username}: {message}"

            broadcast(full_message, client_socket)
        except:
            break

    clients.pop(client_socket)
    client_socket.close()