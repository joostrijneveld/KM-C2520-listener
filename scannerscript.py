import socket, sys

HOST = ''   # Symbolic name meaning the local host
PORT = 37100    # Arbitrary non-privileged port dictated by the scanner daemon
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error code: ' + str(msg[0]) + 'Error message: ' + msg[1]
    sys.exit()
print 'Socket bind complete'

# program loop
# while True:
s.listen(1)
print 'Socket now listening'
# Accept the connection once
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])
conn.send('\x4F\x4B\x00\x05') # initial 'OK05'
print 'sent 1'
data = conn.recv(1024) # should be something like \x00\x06\x34\x00\x00\x02\x00\x00
print 'recv 1',data
conn.send('\x00\x6a\x34\x10\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
print 'sent 2'
data = conn.recv(1024) # seems to be 542
print 'recv 2', data
conn.send('\x00\x0a\x34\x11\x00\x01\x00\x00\xff\xff\xff\xff')
print 'sent 3'
data = conn.recv(1024) # 6 bytes?
print 'recv 3', data
conn.close()

s.listen(1)
print "listening for new connection"
conn, addr = s.accept() #second connection
print "accepting second connection"
conn.send('\x4F\x4B\x00\x05') # initial 'OK05'
print 'sent 1'
data = conn.recv(1024) # should be something like \x00\x06\x34\x00\x00\x02\x00\x00
print 'recv 1',data
conn.send('\x00\x6a\x34\x10\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
print 'sent 2'
data = conn.recv(1024) # seems to be 542 again
print 'recv 2', data
conn.send('\x00\x0a\x34\x11\x00\x01\x00\x00\xff\xff\xff\xff')
print 'sent 3'
data = conn.recv(1024) # 86 bytes. this is the first difference in the second connectionstream
# this data contains the file name we're going to scan to! Perhaps extract?
print 'recv 3', len(data), data
f = open('output.pdf','w')
debug = open('debug','w')
conn.recv(2) # two initial nullbytes
remainingblock = 0
while True:
    data = conn.recv(1024)
    debug.write(data)
    if data == '\x00\x04\x30\x02\x00\x00':
        print 'found closing string'
        break
    if len(data) == 0:
        raise Exception("Found zero data string.")
    if remainingblock == 0:
        remainingblock = data[:2]
        data = data[2:]
        print remainingblock.encode('hex'), int(remainingblock.encode('hex'), 16)
        remainingblock = int(remainingblock.encode('hex'), 16)
    if len(data) > remainingblock:
        raise Exception("Assumed that the protocol did split packets.")
        # print '#', len(data), remainingblock
        # if len(data) == remainingblock+1:
        #     data += conn.recv(1) # only received half of the next size indicator
        # f.write(data[:remainingblock])
        # rightdata = data[remainingblock+2:]
        # f.write(rightdata)
        # nextlen = data[remainingblock:remainingblock+2]
        # print data.encode('hex')
        # print nextlen.encode('hex'), int(nextlen.encode('hex'), 16)
        # remainingblock = int(nextlen.encode('hex'), 16) + 2 - len(rightdata)
    else:
        remainingblock -= len(data)
        f.write(data)
    # print 'Packet received:',len(data)
f.close()
debug.close()

# sends two more packages after the EOF before expecting a reply
# this does not really work correctly yet, as it triggers errors on the machine
conn.send('\x00\x06\x30\x15\x00\x01\x00\x00')
print 'sent 4'
data = conn.recv(1024)
print 'recv 4', data
conn.send('\x00\x06\x30\x13\x00\x01\x00\x00')
print 'sent 5'
conn.close()

print 'done'
