#!/usr/local/bin/python3
# util.py

import pickle

SHARED_HOST = '127.0.0.1'
SHARED_PORT = 12000

def recv_all(sock, buffer_size=1024):
    '''Read until EOF in case buffer is too small.'''
    data = b''

    while part := sock.recv(buffer_size):
        data += part
        if len(part) < buffer_size:
            break
    
    try:
        return pickle.loads(data)
    except EOFError:
        exit('Received out of range number, exiting!')