"""
sniff and save ARP table based network interface
you'll need scapy 
apt-get install scapy 
pip install scapy
http://www.secdev.org/projects/scapy/
"""

import sys
from scapy.all import sniff, ARP
from signal import signal, SIGINT

arp_watcher = "/var/cache/arpwatch.db"
ip_mac = {}

def sig_int_handler(signum, frame):
	print "Got SIGINT, saving ARP to file "
	try:
		f = open(arp_watcher, "w")
		for (ip, mac) in ip_mac.items():
			f.write(ip + " " + mac + "\n")
		f.close()
		print "DONE."
	except IOError:
		print "cannot write to file " + arp_watcher
		sys.exit(1)

def watch(pkt):
	if pkt[ARP].op == 2:
		print pkt[ARP].hwsrc + " " + pkt[ARP].psrc
		if ip_mac.get(pkt[ARP].psrc) == None:
			print "found new device " + \
			pkt[ARP].hwsrc + " " + \
			pkt[ARP].psrc
			ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc
		
		elif ip_mac.get(pkt[ARP].psrc) and ip_mac[pkt[ARP].psrc] != pkt[ARP].hwsrc:
			print pkt[ARP].hwsrc + " got new ip " + pkt[ARP].psrc + " (old " + ip_mac[pkt[ARP].psrc] + ")"
			ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc

signal(SIGINT, sig_int_handler)

if len(sys.argv) < 2:
	print sys.argv[0] + " <interface>"
	sys.exit(0)

try:
	fh = open(arp_watcher, "r")
except IOError:
	print "cannot read fiie "  + arp_watcher
	sys.exit(1)

for line in fh:
	line.chomp()
	(ip, mac) = line.split(" ")
	ip_mac[ip] = mac

sniff(prn = watch, filter="arp", iface=sys.argv[1], store=0)
