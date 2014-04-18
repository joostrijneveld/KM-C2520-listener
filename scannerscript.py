import socket, sys
import os.path

HOST = ''    # Symbolic name meaning the local host
PORT = 37100 # Arbitrary non-privileged port dictated by the scanner daemon
PATH = '~/scans van kopieerapparaat/' # destination to write files to

PATH = os.path.expanduser(PATH)
if not os.path.exists(PATH):
    os.makedirs(PATH)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error code: ' + str(msg[0]) + 'Error message: ' + msg[1]
    sys.exit()
print 'Socket bind complete'

# program loop
while True:
    s.listen(1)
    print 'Socket now listening'
    # Accept the connection once
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    conn.send('\x4F\x4B\x00\x05') # initial 'OK05'
    print 'sent 1'
    data = conn.recv(8) # should be \x00\x06\x34\x00\x00\x02\x00\x00
    print 'recv 1',data.encode('hex')
    conn.send('\x00\x6a\x34\x10\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    print 'sent 2'
    data = conn.recv(542) # seems to be 542
    print 'recv 2', data.encode('hex')
    conn.send('\x00\x0a\x34\x11\x00\x01\x00\x00\xff\xff\xff\xff')
    print 'sent 3'
    data = conn.recv(1024) # 6 bytes? or 86 bytes?
    print 'recv 3', data.encode('hex')

    if data == '\x00\x04\x36\x01\xFF\xF1':
        # this was apparently an 'are you there?'-call
        conn.close()
        continue

    # data = conn.recv(1024) # 86 bytes. this is the first difference in the second connectionstream
    filename = data[38:62].strip('\x00') # byte 37 is $, then 24 bytes of filename follow
    print 'recv 3', len(data), data
    f = open(os.path.join(PATH, filename),'w')
    conn.recv(2) # two initial nullbytes
    remainingblock = 0
    print 'Reading file..'
    while True:
        data = conn.recv(1024)
        if data == '\x00\x04\x30\x02\x00\x00':
            print 'found closing string..'
            break
        if len(data) == 0:
            # raise Exception("Found zero data string.")
            print "Zero data string found"
            break
        if remainingblock == 0:
            remainingblock = data[:2]
            data = data[2:]
            remainingblock = int(remainingblock.encode('hex'), 16)
        if len(data) > remainingblock:
            raise Exception("Assumed that the protocol did not split packets.")
        else:
            remainingblock -= len(data)
            f.write(data)
        # print 'Packet received:',len(data)
    f.close()
    print 'Saved file'
    # sends another package after the closing string, before expecting a reply 
    data = conn.recv(6)
    print 'recv 4' # 00 04 30 05 bf d5 discarded
    conn.send('\x00\x06\x30\x15\x00\x01\x00\x00')
    print 'sent 4'
    data = conn.recv(6) # 00 04 30 03 00 00
    print 'recv 5', data.encode('hex')
    conn.send('\x00\x06\x30\x13\x00\x01\x00\x00')
    print 'sent 5'
    conn.close()
    print 'done'
