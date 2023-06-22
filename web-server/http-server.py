#!/usr/local/bin/python3
# http-server.py

from socket import *
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6789

def recv_all(sock, buffer_size=1024):
    '''Read until EOF in case buffer is too small.'''
    data = b''

    while part := sock.recv(buffer_size):
        data += part
        if len(part) < buffer_size:
            break
    
    return data.decode()

def handle_request(connection_socket):
    try:
        message = recv_all(connection_socket)
        filename = message.split()[1]
        print('Requested file:', filename)

        with open(filename[1:], 'rb') as f:
            # Send one HTTP header line into socket
            connection_socket.sendall('HTTP/1.1 200 OK\r\n'.encode())
            connection_socket.sendall('Content-Type: text/html\r\n'.encode())
            connection_socket.sendall('\r\n'.encode())
            # Send the content of the requested file to the client
            connection_socket.sendall(f.read())
    except IOError:
        # Send response message for file not found
        connection_socket.sendall('HTTP/1.1 404 Not Found\r\n'.encode())
        connection_socket.sendall('Content-Type: text/plain\r\n'.encode())
        connection_socket.sendall('\r\n'.encode())
        # Send 404 and terminates program
        connection_socket.sendall('404 Not Found'.encode())
    
    connection_socket.sendall('\r\n'.encode())
    # Close client socket
    connection_socket.close()

def main():
    # Prepare a server socket
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()

        while True:
            print(f'Ready to serve with {threading.active_count()} threads...') 

            # Establish the connection
            connection_socket, addr = server_socket.accept()

            # OPTIONAL EXERCISE: Service the client request in a separate thread
            t = threading.Thread(target=handle_request, args=(connection_socket,))
            t.start()

if __name__ == '__main__':
    main()