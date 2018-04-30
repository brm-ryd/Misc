#!/usr/bin/python
#service banner grabbing - bannergrab.py
"""
simple banner grabbing - not really useful when port protected, pretty much can read HTTP Header/SMTP/POP 
"""

import sys, socket, urllib

if len(sys.argv) != 2:
    print "usage: python bannergrab.py <url/host> "
    raise SystemExit(1)

target = sys.argv[1]

if target[0:4] == "http":
    page = urllib.urlopen(target)
    print page.info()
else:
    port = raw_input("enter port number: ")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((target, int(port)))
    print sock.recv(1024)
    sock.close()
