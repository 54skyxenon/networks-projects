#!/usr/local/bin/python3
# UDPHeartbeatServer.py, Optional Exercise

from datetime import datetime
import pickle
from random import randint
from socket import *

def main():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('127.0.0.1', 12000))

    curr_seq = 1
    while True:
        try:
            serverSocket.settimeout(5)
            message, address = serverSocket.recvfrom(4096)

            # Simulate randomly dropping packets
            if randint(0, 10) < 3:
                continue

            message = pickle.loads(message)
            sequence_number, time_sent = message['sequence_number'], message['time']

            while curr_seq < sequence_number:
                print(f'Lost heartbeat for SEQ #{curr_seq}')
                curr_seq += 1
            curr_seq = sequence_number + 1
            
            one_way_time = datetime.now() - time_sent
            one_way_time = round(one_way_time.total_seconds() * 1000, 3)
            print(f'Heartbeat for SEQ #{sequence_number} received after {one_way_time} ms')
        except TimeoutError:
            print('Client application has stopped')
            serverSocket.close()
            break

if __name__ == '__main__':
    main()