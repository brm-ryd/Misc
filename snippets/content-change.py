#!/usr/bin/python
"""
tampering content of any file with generate random char
Need to improve optimization of walking folder & measure the tampering process compression
"""

import random, sys, os

def crypt(c, byte,f):
        if c.lower() == "e":
                for i in range(len(byte)):
                        byt = (byte[i] + random.randint(0,255)) % 256
                        f.write(chr(byt))
        elif c.lower() == "d":
                for i in range(len(byte)):
                        byt = ((byte[i] - random.randint(0,255)) + 256) % 256
                        f.write(chr(byt))

        f.close()
if len(sys.argv) != 4:
	print "fcipher.py <e/d> <key-num> <file/dir>"
	raise SystemExit(1)
k = long(sys.argv[2])
random.seed(k)
add = sys.argv[3]
	
if os.path.isdir(add) == True:
        for root, dir, files in os.walk(str(add)):
                for fp in files:
                        try:
                                p = os.path.join(root, fp)
                                f1 = open(p, "rb")
                                byte = map(ord, f1.read())
                                f2 = open(p, "wb")
                                crypt(sys.argv[1], byte, f2)
                        except:
                                pass

else:
        f1=open(add, "rb")
        byte = map(ord, f1.read())
        f2 = open(add, "wb")
        crypt(sys.argv[1], byte, f2)
