import socket
import threading
import json
import os
import random

# Server configuration
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 65432

# File to store data
DATA_FILE = "data.json"

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If the file is empty or invalid, return default data
            return {"attendance": {}, "students_online": {}}
    return {"attendance": {}, "students_online": {}}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Handle client connections
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    data = load_data()
    while True:
        try:
            message = conn.recv(1024).decode("utf-8")
            if not message:
                break

            message = json.loads(message)
            action = message.get("action")

            if action == "login":
                username = message.get("username")
                data["students_online"][username] = conn
                save_data(data)
                broadcast_attendance()

            elif action == "start_timer":
                username = message.get("username")
                data["attendance"][username] = "present"
                save_data(data)
                broadcast_attendance()

            elif action == "stop_timer":
                username = message.get("username")
                data["attendance"][username] = "absent"
                save_data(data)
                broadcast_attendance()

            elif action == "random_ring":
                present_students = [user for user, status in data["attendance"].items() if status == "present"]
                if present_students:
                    selected_student = random.choice(present_students)
                    conn.send(json.dumps({"action": "ring", "student": selected_student}).encode("utf-8"))
                    if selected_student in data["students_online"]:
                        data["students_online"][selected_student].send(json.dumps({"action": "ring"}).encode("utf-8"))

        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the student from the online list when they disconnect
    for username, client_conn in data["students_online"].items():
        if client_conn == conn:
            del data["students_online"][username]
            save_data(data)
            broadcast_attendance()
            break

    conn.close()

# Broadcast attendance data to all clients
def broadcast_attendance():
    data = load_data()
    for conn in data["students_online"].values():
        conn.send(json.dumps({"action": "update_attendance", "data": data["attendance"]}).encode("utf-8"))

# Start the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
