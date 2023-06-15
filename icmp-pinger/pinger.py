#!/usr/local/bin/python3

from socket import *
from statistics import mean

import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
ICMP_HEADER_FORMAT = 'bbHHh'
ERROR_CODES = {
    0: 'Net Unreachable',
    1: 'Host Unreachable',
    2: 'Protocol Unreachable',
    3: 'Port Unreachable',
    4: 'Fragmentation Needed and Don\'t Fragment was Set',
    5: 'Source Route Failed',
    6: 'Destination Network Unknown',
    7: 'Destination Host Unknown',
    8: 'Source Host Isolated',
    9: 'Communication with Destination Network is Administratively Prohibited',
    10: 'Communication with Destination Host is Administratively Prohibited',
    11: 'Destination Network Unreachable for Type of Service',
    12: 'Destination Host Unreachable for Type of Service',
    13: 'Communication Administratively Prohibited',
    14: 'Host Precedence Violation',
    15: 'Precedence cutoff in effect'
}
TIMED_OUT = 'Request timed out.'

def checksum(string):
    string = bytearray(string)
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    
    if countTo < len(string):
        csum = csum + string[-1]
        csum = csum & 0xffffffff
    
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout):
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return TIMED_OUT
        
        timeReceived = time.time()
        recPacket, _addr = mySocket.recvfrom(1024)

        # Fetch the ICMP header from the IP packet
        header, payload = recPacket[20:28], recPacket[28:]
        icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence = struct.unpack(ICMP_HEADER_FORMAT, header)

        if icmp_type == 0 and ID == icmp_id:
            print(f'type: {icmp_type}, code: {icmp_code}, checksum: {icmp_checksum}, id: {icmp_id}, sequence: {icmp_sequence}')
            rtt = timeReceived - struct.unpack('d', payload)[0]
            return rtt
        
        # Optional Exercise: Parse and display the ICMP response errors
        # To test this, try a broken website on iidrn.com
        if icmp_type == 3:
            print(f'got error {icmp_code}: {ERROR_CODES[icmp_code]}')

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return TIMED_OUT

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack('d', time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    
    header = struct.pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))
    # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects which can be referenced by their position number within the object.
    
def doOnePing(destAddr, timeout):
    icmp = getprotobyname('icmp')

    # SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout)

    mySocket.close()
    return delay

def ping(host, timeout=1, sample_size=10, sleep_duration=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print(f'Pinging {dest} using Python:\n')

    # Send ping requests to a server separated by approximately one second
    rtt_data = []
    for _ in range(sample_size):
        delay = doOnePing(dest, timeout)
        print(delay)

        if delay != TIMED_OUT:
            rtt_data.append(delay)
            
        time.sleep(sleep_duration)
    
    # Optional Exercise: Summarize RTT data at the end
    if rtt_data:
        stats = [min(rtt_data), max(rtt_data), mean(rtt_data), 100 * (sample_size - len(rtt_data)) / sample_size]
        print(f'=== Min: {stats[0]:.3f} secs, Max: {stats[1]:.3f} secs, Avg: {stats[2]:.3f} secs, Loss: {stats[3]:.3f}% === ')

ping('google.com')