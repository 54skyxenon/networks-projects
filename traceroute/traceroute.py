#!/usr/local/bin/python3
# traceroute.py

from socket import * 
import os
import sys
import struct
import time
import select

ICMP_HEADER_FORMAT = 'bbHHh'
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

def checksum(string):
    ''' Same checksum function in ICMP Pinger exercise. '''
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

def build_packet():
    ''' Same packet construction implementation as the ICMP Pinger lab. '''
    myID = os.getpid() & 0xFFFF

    myChecksum = 0
    header = struct.pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack('d', time.time())

    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    
    header = struct.pack(ICMP_HEADER_FORMAT, ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet

def print_host_name(addr):
    ''' OPTIONAL EXERCISE: Prints host name and deals with unknown host exceptions. '''
    try:
        print(gethostbyaddr(addr)[0])
    except herror:
        print('Unknown Host')

def get_route(hostname):
    ''' Executes the traceroute function. '''
    time_left = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for _ in range(TRIES):
            # Make a raw socket named my_socket
            my_socket = socket(AF_INET, SOCK_RAW)
            my_socket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            my_socket.settimeout(TIMEOUT)

            try:
                d = build_packet()
                my_socket.sendto(d, (hostname, 0))
                t = time.time()
                started_select = time.time()
                what_ready = select.select([my_socket], [], [], time_left)
                how_long_in_select = (time.time() - started_select)
                if what_ready[0] == []: # Timeout
                    print(' * * * Request timed out.')
                
                recv_packet, addr = my_socket.recvfrom(1024)
                time_received = time.time()
                time_left -= how_long_in_select
                if time_left <= 0:
                    print(' * * * Request timed out.')
                    time_left = TIMEOUT
            except timeout:
                continue
            else:
                # Fetch the icmp type from the IP packet
                types, _, _, _, _ = struct.unpack(ICMP_HEADER_FORMAT, recv_packet[20:28])
                bytes = struct.calcsize('d')

                if types == 11:
                    time_sent = struct.unpack('d', recv_packet[28:28 + bytes])[0]
                    rtt_ms = (time_received - t) * 1000
                    print(f'{ttl}   rtt={rtt_ms:.0f} ms   {addr[0]}')
                    print_host_name(addr[0])
                elif types == 3:
                    time_sent = struct.unpack('d', recv_packet[28:28 + bytes])[0]
                    rtt_ms = (time_received - t) * 1000
                    print(f'{ttl}   rtt={rtt_ms:.0f} ms   {addr[0]}')
                    print_host_name(addr[0])
                elif types == 0:
                    time_sent = struct.unpack('d', recv_packet[28:28 + bytes])[0]
                    rtt_ms = (time_received - time_sent) * 1000
                    print(f'{ttl}   rtt={rtt_ms:.0f} ms   {addr[0]}')
                    print_host_name(addr[0])
                    return
                else:
                    print('error')
            finally:
                my_socket.close()
            
get_route('google.com')