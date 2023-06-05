#!/usr/local/bin/python3
# UDPHeartbeatClient.py, Optional Exercise

from datetime import datetime
import pickle
from socket import *
from time import sleep

NUM_REQUESTS = 20

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

for sequence_number in range(1, NUM_REQUESTS + 1):
    request_time = datetime.now()
    print(f'Sent ping with SEQ #{sequence_number} at {request_time.strftime("%H:%M:%S")}')
    data = pickle.dumps({'sequence_number': sequence_number, 'time': request_time})
    clientSocket.sendto(data, ('127.0.0.1', 12000))
    sleep(0.5)