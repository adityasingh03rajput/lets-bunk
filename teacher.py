import tkinter as tk
from tkinter import ttk
import socket
import json
import threading

# Server configuration
HOST = "192.168.1.100"  # Replace with the server's IP address
PORT = 65432

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to send data to the server
def send_data(action):
    data = {"action": action}
    client_socket.send(json.dumps(data).encode("utf-8"))

# Function to update the attendance table
def update_table(data):
    for row in tree.get_children():
        tree.delete(row)
    for username, status in data.items():
        tree.insert("", "end", values=(username, "P" if status == "present" else "A"))

# Function to handle incoming messages from the server
def receive_messages():
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        message = json.loads(data)
        if message.get("action") == "update_attendance":
            update_table(message.get("data"))

# Start a thread to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

# Create the admin window
teacher_root = tk.Tk()
teacher_root.title("Teacher Panel")
teacher_root.geometry("600x400")

# Create a table to display attendance
tree = ttk.Treeview(teacher_root, columns=("Username", "Status"), show="headings")
tree.heading("Username", text="Username")
tree.heading("Status", text="Status")
tree.pack(fill="both", expand=True)

teacher_root.mainloop()
