#!/usr/local/bin/python3
# UDPPingerClient.py

from socket import *
from datetime import datetime
from statistics import mean

NUM_REQUESTS = 10

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

rtt_data = []

for sequence_number in range(1, NUM_REQUESTS + 1):
    try:
        request_time = datetime.now()
        ping = f'Ping {sequence_number} {request_time.strftime("%H:%M:%S")}'

        clientSocket.sendto(ping.encode(), ('127.0.0.1', 12000))
        clientSocket.settimeout(1)
        
        message = clientSocket.recvfrom(1024)[0]
        rtt = datetime.now() - request_time
        rtt = round(rtt.total_seconds() * 1000, 3)
        rtt_data.append(rtt)

        print(f'{message.decode()}, RTT = {rtt} ms')
    except timeout:
        print('Request timed out')

def main():
    # Optional Exercise
    print('\n=== SUMMARY ===')
    print(f'Avg: {round(mean(rtt_data), 3)} ms, Min: {min(rtt_data)} ms, Max: {max(rtt_data)} ms')
    print(f'Packet loss: {100 - len(rtt_data) * 10}%')

if __name__ == '__main__':
    main()