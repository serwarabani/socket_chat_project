import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5000

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() 
        
       
        self.username = simpledialog.askstring("Username", "Please enter your username:", parent=self.root)
        if not self.username:
            sys.exit()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((HOST, PORT))
            self.client.send(self.username.encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server:\n{e}")
            sys.exit()

        self.build_gui()
        self.running = True
        
      
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True 
        self.receive_thread.start()

    def build_gui(self):
   
        self.root.deiconify() 
        self.root.title(f"Socket Chat - {self.username}")
        self.root.geometry("500x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    
        self.chat_log = tk.Text(self.root, state='disabled', bg="#f4f4f4", font=("Arial", 11), wrap=tk.WORD)
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

      
        self.message_entry = tk.Entry(bottom_frame, font=("Arial", 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda event: self.send_message()) # پشتیبانی از کلید اینتر

       
        send_button = tk.Button(bottom_frame, text="Send", command=self.send_message, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
        send_button.pack(side=tk.RIGHT)

    def receive_messages(self):
     
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message)
            except:
                if self.running:
                    self.display_message("System: Connection to server lost.")
                break

    def display_message(self, message):
       
        self.chat_log.config(state='normal')
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
            self.display_message("System: Failed to send message. Server might be down.")

    def on_closing(self):
       
        self.running = False
        try:
            self.client.send("/exit".encode('utf-8'))
            self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    app = ChatClient()
    app.root.mainloop()