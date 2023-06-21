#!/usr/local/bin/python3
# ProxyServer.py

# Inspiration from: https://github.com/jzplp/Computer-Network-A-Top-Down-Approach-Answer/blob/master/Chapter-2/Socket-Programming-Assignment-4/ProxyServer.py

from socket import *
import sys

if len(sys.argv) < 2:
    print('Usage: ./ProxyServer.py server_ip\n[server_ip: It is the IP Address Of Proxy Server]')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen()

def recv_all(sock, buffer_size=1024):
    '''Read until EOF in case buffer is too small.'''
    data = b''

    while part := sock.recv(buffer_size):
        data += part
        if len(part) < buffer_size:
            break
    
    return data.decode()

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = recv_all(tcpCliSock)
    # print(message)

    if not message:
        continue

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    fileExists = False

    try:
        # Check whether the file exist in the cache
        f = open(filename, "r")
        outputdata = f.read()
        fileExists = True
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b'HTTP/1.1 200 OK\r\n')
        tcpCliSock.send(b'Content-Type: text/html\r\n\r\n')
        tcpCliSock.send(outputdata.encode())
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if not fileExists:
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace('www.', '', 1)
            print('Hostname:', hostn)
            
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                print('Connected to real web server!')
                
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                with c.makefile('rwb', 0) as fileobj:
                    fileobj.write(f"GET https://{filename} HTTP/1.1\r\n".encode())
                    # Read the response into buffer
                    buf = fileobj.read()            
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tcpCliSock.sendall(buf)
                    with open(f'./{filename}', 'wb') as tmpFile:
                        tmpFile.write(buf)
            except:
                print('Illegal request')
        else:
            # HTTP response message for file not found
            tcpCliSock.sendall(b'HTTP/1.1 404 Not Found\r\n')
            tcpCliSock.sendall(b'Content-Type: text/plain\r\n\r\n')
            tcpCliSock.sendall(b'404 Not Found')

    # Close the client and the server sockets
    tcpCliSock.close()

tcpSerSock.close()