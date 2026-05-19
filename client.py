import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading
import sys
import time

HOST = '127.0.0.1'
PORT = 5000

class FullyCompliantClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() 
        
        self.username = simpledialog.askstring("Username", "Please enter your username:", parent=self.root)
        if not self.username:
            sys.exit()

        self.build_gui()
        self.running = True
        self.connected = False
        
   
        self.connection_thread = threading.Thread(target=self.manage_connection)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def build_gui(self):
        self.root.deiconify()
        self.root.title(f"Chat Room - {self.username}")
        self.root.geometry("450x550")
        self.root.configure(bg="#2f3640") 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        header = tk.Label(self.root, text=f"💬 Global Chat Room", font=("Arial", 14, "bold"), bg="#1e252f", fg="#f5f6fa", pady=10)
        header.pack(fill=tk.X)

        self.chat_log = tk.Text(self.root, state='disabled', bg="#2f3640", fg="#f5f6fa", 
                                font=("Segoe UI", 11), wrap=tk.WORD, bd=0, padx=10, pady=10)
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.chat_log.tag_config("system", foreground="#eccc68", font=("Segoe UI", 10, "italic")) 
        self.chat_log.tag_config("private", foreground="#ff4757", font=("Segoe UI", 11, "bold")) 
        self.chat_log.tag_config("history", foreground="#a4b0be") 

        self.bottom_frame = tk.Frame(self.root, bg="#2f3640")
        self.bottom_frame.pack(padx=10, pady=(0, 15), fill=tk.X)

        self.message_entry = tk.Entry(self.bottom_frame, font=("Segoe UI", 12), bg="#353b48", 
                                      fg="white", insertbackground="white", bd=1, relief=tk.FLAT, state='disabled')
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(self.bottom_frame, text="Send", command=self.send_message, 
                                bg="#70a1ff", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=15, state='disabled')
        self.send_button.pack(side=tk.RIGHT, ipady=5)

    def manage_connection(self):
 
        while self.running:
            if not self.connected:
                self.display_message("System: Trying to connect to server...", "system")
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.client.connect((HOST, PORT))
                    self.client.send(self.username.encode('utf-8'))
                    self.connected = True
                    self.enable_input()
                    self.display_message("System: Connected successfully!", "system")
                    
                  
                    self.receive_messages()
                except socket.error:
                    self.connected = False
                    self.disable_input()
                    self.display_message("System: Connection failed. Retrying in 5 seconds...", "system")
                    time.sleep(5)

    def receive_messages(self):
        while self.running and self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    bg_err = True
                    break
                self.display_message(message)
            except:
                break
        
    
        self.connected = False
        self.disable_input()
        self.display_message("System: Connection lost!", "system")

    def enable_input(self):
        self.message_entry.config(state='normal')
        self.send_button.config(state='normal')
        self.message_entry.focus_set()

    def disable_input(self):
        self.message_entry.config(state='disabled')
        self.send_button.config(state='disabled')

    def display_message(self, message, tag=None):
        self.chat_log.config(state='normal')
        if tag is None:
            if message.startswith("System:"): tag = "system"
            elif "[PM" in message: tag = "private"
            elif message.startswith("-") or "history" in message.lower(): tag = "history"

        if tag:
            self.chat_log.insert(tk.END, message + "\n", tag)
        else:
            self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.see(tk.END)
        self.chat_log.config(state='disabled')

    def send_message(self):
        msg = self.message_entry.get().strip()
        if not msg:
            return
        self.message_entry.delete(0, tk.END)
        
        if msg == "/exit":
            self.on_closing()
            return
        
        try:
            self.client.send(msg.encode('utf-8'))
        except:
            self.display_message("System: Message delivery failed. Connection is down.", "system")

    def on_closing(self):
        self.running = False
        try:
            if self.connected:
                self.client.send("/exit".encode('utf-8'))
                self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    app = FullyCompliantClient()
    app.root.mainloop()