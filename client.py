import socket
import threading


# Function to receive messages from server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            index_of_colon = message.rfind(':')
            f = open('chatlog.txt', "w")
            f.write(message[index_of_colon+1::])
            f.close()
        except:
            # If there is an error while receiving, assume server is disconnected
            print("Connection to server closed")
            break

# Connect to the server
server_address = ('localhost', 5555)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Start a thread to receive messages from server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


name = input("Enter your name :")
# Main loop to send messages to server
while True:
    message = input()
    message = name + ' :' + message
    client_socket.send(message.encode('utf-8'))
