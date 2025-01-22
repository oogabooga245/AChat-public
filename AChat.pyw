import socket
import threading
from tkinter import Tk, Text, Button, Scrollbar, Entry, END

class ChatRoom:
    def __init__(self, host, port):
        self.root = Tk()
        self.root.title("AChat Room")
        self.chat_log = Text(self.root, state='disabled', width=50, height=20, wrap='word')
        self.chat_log.pack(padx=10, pady=10)
        
        self.scrollbar = Scrollbar(self.root, command=self.chat_log.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.chat_log['yscrollcommand'] = self.scrollbar.set
        
        self.message_entry = Entry(self.root, width=40)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind('<Return>', lambda event: self.send_message())
        
        self.send_button = Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)
        
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_relay()
        
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.mainloop()

    def connect_to_relay(self):
        try:
            self.socket.connect((self.host, self.port))
            self.append_message("Connected to relay.")
        except Exception as e:
            self.append_message(f"Failed to connect to relay: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.append_message(message)
            except:
                break

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                self.socket.sendall(message.encode('utf-8'))
                self.append_message(f"You: {message}")
                self.message_entry.delete(0, END)
            except Exception as e:
                self.append_message(f"Failed to send message: {e}")

    def append_message(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.see(END)

if __name__ == "__main__":
    HOST = "69.164.196.248"
    PORT = 9000
    ChatRoom(HOST, PORT)
