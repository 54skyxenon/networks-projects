# server.py

import pickle
import random
import socket
from util import recv_all, SHARED_HOST, SHARED_PORT

'''
Creates a server name and then begins accepting connections from clients.

On receipt of a client message:
    (i) prints the client's name (extracted from the received message) and the server's name
    (ii) picks an integer from 1 to 100 and display the client's number, its number, and the sum of those numbers
    (iii) send its name string and the server-chosen integer value back to the client
    (iv) if received an integer value that is out of range, should terminate after releasing any created sockets (shutdown)
'''

SERVER_NAME = '54skyxenon-server'

if __name__ == '__main__':
    # `with` handles closing resources for both the welcome and connection sockets
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as welcome_socket:
        # socket.SO_REUSEADDR mitigates `Address already in use` after successive re-runs
        welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        welcome_socket.bind((SHARED_HOST, SHARED_PORT))
        welcome_socket.listen()

        print('The server is ready to receive!')

        while True:
            with welcome_socket.accept()[0] as connection_socket: 
                request = recv_all(connection_socket)
                client_number = request['client_number']
                client_name = request['client_name']
                server_number = random.randint(1, 100)

                print('Received request from client:')
                print(f'\tServer: {SERVER_NAME}, Client: {client_name}')
                print(f'\tClient number: {client_number}, Server number: {server_number}, Sum: {client_number + server_number}')

                if not 1 <= client_number <= 100:
                    exit('Received out of range number, exiting!')

                serialized = pickle.dumps({'server_name': SERVER_NAME, 'server_number': server_number})
                connection_socket.send(serialized)