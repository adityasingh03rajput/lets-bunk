import socket
import threading
import random

# Dictionary to store active chat sessions
chat_sessions = {}

# Function to handle communication between two clients
def handle_chat(client1, client2):
    while True:
        try:
            # Receive message from client1
            message = client1.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from client1: {message}")
            # Send message to client2
            client2.send(message.encode('utf-8'))

            # Receive message from client2
            message = client2.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from client2: {message}")
            # Send message to client1
            client1.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

    # Close connections
    client1.close()
    client2.close()

# Function to start the chat server
def start_chat_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(2)  # Allow 2 clients to connect
    print(f"Chat server started on port {port}...")

    # Wait for two clients to connect
    client1, addr1 = server_socket.accept()
    print(f"Client 1 connected: {addr1}")
    client2, addr2 = server_socket.accept()
    print(f"Client 2 connected: {addr2}")

    # Start a thread to handle communication between the two clients
    chat_thread = threading.Thread(target=handle_chat, args=(client1, client2))
    chat_thread.start()

# Function to generate a unique host code
def generate_host_code():
    return str(random.randint(100000, 999999))

# Main server function
def main():
    # Generate a host code and port for the chat session
    host_code = generate_host_code()
    port = random.randint(10000, 20000)  # Random port for the chat server

    # Store the host code and port mapping
    chat_sessions[host_code] = port

    # Start the chat server in a new thread
    chat_thread = threading.Thread(target=start_chat_server, args=(port,))
    chat_thread.start()

    print(f"Host code: {host_code}")
    print("Waiting for users to join...")

if __name__ == '__main__':
    main()
