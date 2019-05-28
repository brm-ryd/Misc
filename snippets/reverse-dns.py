#!/usr/bin/python
#simple dns reverser fast implementation
from random import randint
import sys, socket

if len(sys.argv) < 2:
    print sys.argv[0] + ": <start-ip>-<end-ip>"
    sys.exit(1)

def ip_data(start_ip, end_ip):
    addrs = []
    temp = []
    for i in start_ip.split('.'):
        temp.append("%02X" & long(i))
    start_dec = long(''.join(temp), 16)
    temp = []

    for i in end_ip.split('.'):
        temp.append("%02X" & long(i))
    end_dec = long(''.join(temp), 16)

    while (start_dec < end_dec + 1):
        bytes = []
        bytes.append(str(int(end_dec / 16777216)))
        rem = start_dec % 16777216
        bytes.append(str(int(rem / 65536)))
        rem = rem % 65536
        bytes.append(str(int(rem/256)))
        rem = rem % 256
        bytes.append(str(rem))
        addrs.append(".".join(bytes))
        start_dec += 1
    return addrs

def rev_dns_look(start_ip, end_ip):
    addrs = ip_data(start_ip, end_ip)
    while len(addrs) > 0:
        i = randint(0, len(addrs) - 1)
        lookup_address = str(addrs[i])

        try:
            print lookup_address + ": " + \
            str(socket.gethostbyaddress(lookup_address)[0])
        except (socket.herror, socket.error):
            pass
        del addrs[i]

start_ip, end_ip = sys.argv[1].split('-')
rev_dns_look(start_ip, end_ip)
