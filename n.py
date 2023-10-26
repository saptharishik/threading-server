

import socket
import threading
import time
def message(port_no):
    # Server function for sending data to the client
    def server_send(client_socket):
        while True:
            message = input()
            client_socket.send(message.encode())

    # Server function for receiving data from the client
    def server_receive(client_socket):
        while True:
            data = client_socket.recv(1024)
            print("Client (Received): " + data.decode())


    # Server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.102', port_no))
    server_socket.listen(1)
    print("Server is waiting for a connection...")
    client_socket, addr = server_socket.accept()

    # Create and start server threads
    server_send_thread = threading.Thread(target=server_send, args=(client_socket,))
    server_receive_thread = threading.Thread(target=server_receive, args=(client_socket,))
    server_send_thread.start()
    server_receive_thread.start()
