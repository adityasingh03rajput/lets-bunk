# client.py
import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Connection closed by the server.")
                break
            print(f"Received: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        try:
            message = input("You: ")
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            break

# Main client function
def main():
    server_ip = "169.254.157.6"  # Server's IP address
    host_code = input("Enter host code: ")  # Host code provided by the server
    port = int(input("Enter port: "))  # Port provided by the server

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, port))
        print("Connected to the chat server. Start chatting!")

        # Start threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print("Disconnected from the server.")

if __name__ == '__main__':
    main()
