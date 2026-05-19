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
clients_lock = threading.Lock() 
def broadcast(message):
  
    with clients_lock:
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
            
        print(f"[NEW CONNECTION] {username} connected from {ip}")
        broadcast(f"System: {username} has joined the chat!")

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message or message == "/exit":
                break

          
            if message.startswith(">pm"):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    client_socket.send("System: Invalid PM format. Use: >pm <userIP> <message>\n".encode('utf-8'))
                    continue
                
                target_ip = parts[1]
                pm_message = parts[2]
                sent = False
                
                with clients_lock:
                    for c, info in clients.items():
                        if info['ip'] == target_ip:
                            c.send(f"[PM from {username}]: {pm_message}\n".encode('utf-8'))
                            sent = True
                            
                if not sent:
                    client_socket.send(f"System: No user found with IP {target_ip}\n".encode('utf-8'))
                else:
                    client_socket.send(f"[PM to {target_ip}]: {pm_message}\n".encode('utf-8'))
                continue

         
            if message.startswith(">users"):
                with clients_lock:
                    user_list = "\n".join([f"- {info['username']} ({info['ip']})" for c, info in clients.items()])
                client_socket.send(f"\n--- Connected Users ---\n{user_list}\n-----------------------\n".encode('utf-8'))
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
        client_socket.close()
        broadcast(f"System: {username} has left the chat.")


while True:
    client_socket, client_address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.daemon = True
    thread.start()