#! /usr/bin/python

import socket, sys, os

HOST = ''    # Symbolic name meaning the local host
PORT = 37100 # Arbitrary non-privileged port dictated by the scanner daemon
PATH = '~/Documents/scans van kopieerapparaat/' # destination to write files to

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
    try:
        s.listen(1)
        gotnullbytes = False # track if we have received the nullbytes yet
        print 'Socket now listening'
        # Accept the connection once
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        conn.send('\x4F\x4B\x00\x05') # initial 'OK05'
        data = conn.recv(1024) # should be \x00\x06\x34\x00\x00\x02\x00\x00
        print 'recv 1',data.encode('hex')
        print 'expected  00 06 34 00 00 02 00 00'
        conn.send('\x00\x6a\x34\x10\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        data = conn.recv(1024) # seems to be 542
        print 'recv 2', data.encode('hex')
        print 'expected 542, got ',str(len(data))
        conn.send('\x00\x0a\x34\x11\x00\x01\x00\x00\xff\xff\xff\xff')
        data = conn.recv(1024) # 6 bytes? or 86 bytes? first difference between connections
        print 'recv 3b', data.encode('hex')
        if data == '\x00\x00': # for some large files, suddenly the null-bytes appear here.. what the hell..?
            data = conn.recv(1024) # 6 bytes? or 86 bytes? first difference between connections
            gotnullbytes = True
            print 'recv 3b-afternull', data.encode('hex')

        if data == '\x00\x04\x36\x01\xFF\xF1':
            # this was apparently an 'are you there?'-call
            conn.close()
            continue

        filename = os.path.join(PATH, data[38:62].strip('\x00')) # byte 37 is $, then 24 bytes of filename follow
        print filename
        print 'recv 3', len(data), data
        f = open(filename,'w')
        # debug = open('debug','w')
        data = conn.recv(2) # maybe two initial nullbytes
        print 'recv 3c', data.encode('hex')
        retaindata = False
        if data == '\x00\x00':
            if gotnullbytes:
                print "Two blocks of 2 nullbytes!"
            else:
                print 'Confirming nullbytes'
        else:
            print 'Oops. Ate initial bytes off the PDF while zero-testing'
            retaindata = True
        remainingblock = 0
        print 'Reading file..'
        canceled = False
        while True:
            if retaindata:
                print 'Retaining data..'
                # data += conn.recv(1024)
                retaindata = False
            else:
                data = conn.recv(1024)
            # debug.write(data) # starts with 0a69?
            if len(data) < 100:
                print 'Data trace:'
                print data.encode('hex')
            if data == '\x00\x04\x30\x02\x00\x00':
                print 'found closing string..'
                break
            if len(data) == 0:
                print "User seems to have pressed cancel during scan.."
                canceled = True
                break
            if remainingblock == 0:
                datahead = data
                remainingblock = data[:2]
                data = data[2:]
                remainingblock = int(remainingblock.encode('hex'), 16)
            if len(data) > remainingblock:
                print 'This should not be happening', len(data), remainingblock
                print 'Data head:',datahead.encode('hex')
                print 'data at the moment:', data.encode('hex')
                f.write(data[:remainingblock])
                print 'Written to file:', data[:remainingblock].encode('hex')
                data = data[remainingblock:]
                remainingblock = 0
                print 'data at the moment:', data.encode('hex')
                retaindata = True
            else:
                remainingblock -= len(data)
                f.write(data)
        # debug.close()
        f.close()
        if canceled:
            os.remove(filename)
            print 'Removed file'
            conn.close()
            continue
        print 'Saved file'
        # sends another package after the closing string, before expecting a reply 
        data = conn.recv(6)
        print 'recv 4' # 00 04 30 05 bf d5 discarded
        # capture of 1 long file: 00 04 30 05 36 ce
        conn.send('\x00\x06\x30\x15\x00\x01\x00\x00')
        data = conn.recv(6) # 00 04 30 03 00 00
        print 'recv 5', data.encode('hex')
        conn.send('\x00\x06\x30\x13\x00\x01\x00\x00')
        print 'done'
    except Exception as inst:
        print inst
    finally:
        conn.close()
        
