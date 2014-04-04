#! /usr/bin/env python

import sys
from collections import deque

try:
	f = open(sys.argv[1],'rb')
	f2 = open(sys.argv[2],'w')
	byte = ''
	buff8 = deque(maxlen=8)
	i = 0
	mark = 0
	c = 0
	f.read(2) # clean up the accidental two nullbytes
	f.read(2) # clean up the first size indicator
	while byte != "" or not i:
		byte = f.read(2)
		i += 2
		if i-mark == 1460*16+1218: # after each block, skip new size indicator
			print "{:02x} {:02x}".format(*map(ord, byte))
			c += 1
			mark = i
			continue
		f2.write(byte)
		buff8.extend(byte)
		if "".join(list(buff8)[2:]) == "%%EOF\n":
			break # prevent noise at the end, after EOF
	print buff8
	print c
finally:
	f.close()
