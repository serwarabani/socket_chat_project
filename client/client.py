import tkinter as tk
import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter username: ")
client.send(username.encode())

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            chat_log.config(state='normal')
            chat_log.insert(tk.END, message + "\n")
            chat_log.config(state='disabled')
        except:
            break

def send_message():
    msg = message_entry.get()
    if msg == "/exit":
        client.close()
        root.destroy()
        return
    client.send(msg.encode())
    message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Socket Chat GUI")

chat_log = tk.Text(root, state='disabled', width=50, height=20)
chat_log.pack()

message_entry = tk.Entry(root, width=40)
message_entry.pack(side=tk.LEFT)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()