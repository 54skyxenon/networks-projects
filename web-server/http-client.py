#!/usr/local/bin/python3
# http-client.py

from socket import *
import sys

def http_get(server_host, server_port, filename):
    # Create a socket and connect to the server
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # Send the HTTP GET request
    request = f'GET {filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n'
    client_socket.sendall(request.encode())

    # Receive and display the server's response
    response = b''
    while data := client_socket.recv(1024):
        response += data

    print(response.decode())

    # Close the socket
    client_socket.close()

def main():
    # Check if the command line arguments are provided
    if len(sys.argv) != 4:
        print('Usage: ./http-client.py server_host server_port filename')
        exit(1)

    # Parse the command line arguments
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    # Call the HTTP GET function
    http_get(server_host, server_port, filename)

if __name__ == '__main__':
    main()