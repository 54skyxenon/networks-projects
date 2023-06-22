#!/usr/local/bin/python3
# ProxyServer.py

from socket import *
import os
import signal
import sys

def recv_all(sock, buffer_size=1024):
    data = b''

    while part := sock.recv(buffer_size):
        data += part
        if len(part) < buffer_size:
            break
    
    return data.decode()

def send_200(sock, payload):
    sock.sendall(b'HTTP/1.1 200 OK\r\n')
    sock.sendall(b'Content-Type: text/html\r\n\r\n')
    sock.sendall(payload)

def send_404(sock):
    sock.sendall(b'HTTP/1.1 404 Not Found\r\n')
    sock.sendall(b'Content-Type: text/plain\r\n\r\n')
    sock.sendall(b'404 Not Found')

def main():
    if len(sys.argv) < 2:
        print('Usage: ./ProxyServer.py port_number\n[port_number: Which port should localhost use?]')
        exit(2)

    # Create a server socket, bind it to a port and start listening
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_server_socket.bind(('localhost', int(sys.argv[1])))
    tcp_server_socket.listen()

    def signal_handler(sig, frame):
        print('\nClosing server socket and shutting down...')
        tcp_server_socket.close()
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # Start receiving data from the client
        print('Ready to serve...')
        tcp_client_socket, addr = tcp_server_socket.accept()
        print('Received a connection from:', addr)
        message = recv_all(tcp_client_socket).split()

        if not message:
            continue

        # Extract the file name from the given message
        method, file_path = message[0], message[1]
        print(method, file_path)
        file_name = file_path.partition("/")[2]
        file_name = file_name.replace('www.', '', 1)
        cached_path = f'./cached/{file_name}'
        file_exists = False

        # OPTIONAL EXERCISE: Check whether the file exist in the cache
        try:
            # Should not cache POSTs, force the request to happen
            if method == 'POST':
                raise IOError

            # ProxyServer finds a cache hit and generates a response message
            with open(cached_path, 'rb') as f:
                cached_payload = f.read()
                file_exists = True
                send_200(tcp_client_socket, cached_payload)
            
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
                        file_obj.write(f"{method} /{resource_name} HTTP/1.0\r\n".encode())

                        # OPTIONAL EXERCISE: Support POST requests (assuming application/x-www-form-urlencoded)
                        if method == 'POST':
                            file_obj.write(b'Content-Type: application/x-www-form-urlencoded\r\n\r\n')
                            post_data = message[-1]
                            file_obj.write(post_data.encode())
                            print(f'Doing POST request with {post_data}')
                        elif method == 'GET':
                            file_obj.write(b'\r\n')
                            print(f'Cache miss, doing GET request')
                        else:
                            raise ValueError

                        # Read the response into buffer
                        buf = file_obj.read()
                        header, payload = buf.split(b'\r\n\r\n')

                        # OPTIONAL EXERCISE: Handles 404
                        status_code = header.split()[1].decode()
                        if status_code == '404':
                            print('404 Not Found')
                            send_404(tcp_client_socket)
                            tcp_client_socket.close()
                            continue

                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        send_200(tcp_client_socket, payload)

                        # Caching POST requests not important: https://stackoverflow.com/q/626057/5674135
                        if method == 'GET':
                            cached_dir = os.path.dirname(cached_path)
                            os.makedirs(cached_dir, exist_ok=True)
                            with open(cached_path, 'wb') as tmp_file:
                                tmp_file.write(payload)
                except:
                    print('Illegal request')
            else:
                print('Error sending cached data!')

        # Close the client and the server sockets
        tcp_client_socket.close()

if __name__ == '__main__':
    main()