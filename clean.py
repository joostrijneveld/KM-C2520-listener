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
	while byte != "" or not i:
		byte = f.read(2)
		if byte == "\x60\x00" and c < 4:
			print i-mark
			if i-mark == 1460*16+1218 or not mark: # after each set of 16 x 1460 bytes, 1218 is received
				c += 1
				mark = i
				i += 2
				continue
		f2.write(byte)
		buff8.extend(byte)
		if "".join(list(buff8)[2:]) == "%%EOF\n":
			break # prevent noise at the end, after EOF
		i += 2
	print buff8
	print c
finally:
	f.close()
