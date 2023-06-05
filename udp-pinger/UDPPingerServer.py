#!/usr/local/bin/python3
# UDPPingerServer.py

# We will need the following module to generate randomized lost packets
from random import randint
from socket import *

# Create a UDP socket, using SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('127.0.0.1', 12000))

while True:
    # Generate random number in the range of 0 to 10
    rand = randint(0, 10)
    
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Capitalize the message from the client
    message = message.upper()

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue

    # Otherwise, the server responds
    serverSocket.sendto(message, address)