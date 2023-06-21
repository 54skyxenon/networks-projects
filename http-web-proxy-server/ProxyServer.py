#!/usr/local/bin/python3
# ProxyServer.py

# Inspiration from: https://github.com/jzplp/Computer-Network-A-Top-Down-Approach-Answer/blob/master/Chapter-2/Socket-Programming-Assignment-4/ProxyServer.py

from socket import *
import os
import sys

def recv_all(sock, buffer_size=1024):
    '''Read until EOF in case buffer is too small.'''
    data = b''

    while part := sock.recv(buffer_size):
        data += part
        if len(part) < buffer_size:
            break
    
    return data.decode()

def main():
    if len(sys.argv) < 2:
        print('Usage: ./ProxyServer.py port_number\n[port_number: Which port should localhost use?]')
        sys.exit(2)

    # Create a server socket, bind it to a port and start listening
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_server_socket.bind(('localhost', int(sys.argv[1])))
    tcp_server_socket.listen()

    while True:
        # Start receiving data from the client
        print('Ready to serve...')
        tcp_client_socket, addr = tcp_server_socket.accept()
        print('Received a connection from:', addr)
        message = recv_all(tcp_client_socket)

        if not message:
            continue

        # Extract the file name from the given message
        file_path = message.split()[1]
        print(file_path)
        file_name = file_path.partition("/")[2]
        file_name = file_name.replace('www.', '', 1)
        cached_path = f'./cached/{file_name}'
        file_exists = False

        try:
            # Check whether the file exist in the cache
            with open(cached_path, 'rb') as f:
                output_data = f.read()
                file_exists = True
                # ProxyServer finds a cache hit and generates a response message
                tcp_client_socket.send(b'HTTP/1.1 200 OK\r\n')
                tcp_client_socket.send(b'Content-Type: text/html\r\n\r\n')
                tcp_client_socket.send(output_data)
            
            print('Cache hit!')
        # Error handling for file not found in cache
        except IOError:
            if not file_exists:
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                host_name, _, resource_name = file_name.partition('/')
                
                try:
                    # Connect to the socket to port 80
                    c.connect((host_name, 80))
                    
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    with c.makefile('rwb', 0) as file_obj:
                        print(f'Cache miss, doing GET /{resource_name} HTTP/1.0')
                        file_obj.write(f"GET /{resource_name} HTTP/1.0\r\n\r\n".encode())
                        # Read the response into buffer
                        buf = file_obj.read()
                        payload = buf.split(b'\r\n\r\n')[1]

                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        tcp_client_socket.send(b'HTTP/1.1 200 OK\r\n')
                        tcp_client_socket.send(b'Content-Type: text/html\r\n\r\n')
                        tcp_client_socket.send(payload)

                        cached_dir = os.path.dirname(cached_path)
                        os.makedirs(cached_dir, exist_ok=True)
                        with open(cached_path, 'wb') as tmp_file:
                            tmp_file.write(payload)
                except:
                    print('Illegal request')
            else:
                # HTTP response message for file not found
                tcp_client_socket.send(b'HTTP/1.0 404 Not Found\r\n')
                tcp_client_socket.send(b'Content-Type: text/plain\r\n\r\n')
                tcp_client_socket.send(b'404 Not Found')

        # Close the client and the server sockets
        tcp_client_socket.close()

    tcp_server_socket.close()

if __name__ == '__main__':
    main()