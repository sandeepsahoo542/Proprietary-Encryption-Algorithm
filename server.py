import socket
import threading

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    while True:
        # Receive message from client
        message = client_socket.recv(1024).decode('utf-8')

        if not message:
            # If no message received, client might have disconnected
            print(f"Connection from {client_address} closed")
            break

        # Broadcast the message to all clients
        broadcast(message, client_socket)

    # Close the client socket
    client_socket.close()

# Function to broadcast message to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # If there is an error while sending, assume client is disconnected
                client.close()
                clients.remove(client)

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to localhost and a port (e.g., 5555)
server_socket.bind(('localhost', 5555))

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for connections...")

# List to keep track of connected clients
clients = []

while True:
    # Accept connection from client
    client_socket, client_address = server_socket.accept()

    # Add client to the list of clients
    clients.append(client_socket)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
