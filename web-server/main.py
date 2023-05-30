from socket import *

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6789

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((SERVER_HOST, SERVER_PORT))
serverSocket.listen()

def recv_all(sock, buffer_size=1024):
    '''Read until EOF in case buffer is too small.'''
    data = b''

    while part := sock.recv(buffer_size):
        data += part
        if len(part) < buffer_size:
            break
    
    return data.decode()

while True:
    print('Ready to serve...') 

    # Establish the connection
    connectionSocket, addr = serverSocket.accept()

    try:
        message = recv_all(connectionSocket)
        filename = message.split()[1]
        print('Requested file:', filename)

        with open(filename[1:], 'rb') as f:
            # Send one HTTP header line into socket
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
            connectionSocket.send('Content-Type: text/html\r\n'.encode())
            connectionSocket.send('\r\n'.encode())

            # Send the content of the requested file to the client
            connectionSocket.send(f.read())
            connectionSocket.send('\r\n'.encode())
            # Close client socket
            connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/plain\r\n'.encode())
        connectionSocket.send('\r\n'.encode())

        # Send 404 and terminates program
        connectionSocket.send('404 Not Found'.encode())
        connectionSocket.send('\r\n'.encode())
        # Close client socket
        connectionSocket.close()
        break

# Terminate the program after sending the corresponding data
serverSocket.close()