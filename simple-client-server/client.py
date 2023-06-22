#!/usr/local/bin/python3
# client.py

import pickle
import socket
from util import recv_all, SHARED_HOST, SHARED_PORT

'''
Sends a request:
    1. Gets an integer between 1 and 100 from user input
    2. Opens a TCP socket to server and sends a message containing:
        (i) a string containing your name
        (ii) the entered integer value and then wait for a sever reply.

Upon receiving server's message:
    1. Read the message sent by the server and display: name, server's name, integer value, server's integer value
    2. Compute the sum.
    3. Terminates after releasing any created sockets.
'''

CLIENT_NAME = '54skyxenon-client'
INVALID = 1000

def main():
    print('The client is ready to send!')
    while True:
        # `with` handles closing resources for the client socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SHARED_HOST, SHARED_PORT))

            try:
                client_number = int(input('Pick a number from 1 to 100: '))
            except ValueError:
                client_number = INVALID

            serialized = pickle.dumps({'client_name': CLIENT_NAME, 'client_number': client_number})
            client_socket.send(serialized)

            response = recv_all(client_socket)
            server_name = response['server_name']
            server_number = response['server_number']

            print('Received response from server:')
            print(f'\tClient: {CLIENT_NAME}, Server: {server_name}')
            print(f'\tClient number: {client_number}, Server number: {server_number}, Sum: {client_number + server_number}')

if __name__ == '__main__':
    main()