# coding: utf-8
import socket


messages = ['This is the message ', 'It will be sent ', 'in parts ', ]

host = '127.0.0.1'
port = 9080
server_address = (host, port)

# Create aTCP/IP socket

socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET,  socket.SOCK_STREAM), ]

# Connect thesocket to the port where the server is listening

print('connecting to %s port %s' % server_address)
# 连接到服务器
for s in socks:
    s.connect(server_address)

for index, message in enumerate(messages):
    # Send messages on both sockets
    for s in socks:
        print('%s: sending "%s"' % (s.getsockname(), message + str(index)))
        s.send((message + str(index)).decode('utf-8'))
    # Read responses on both sockets

for s in socks:
    data = s.recv(1024)
    print('%s: received "%s"' % (s.getsockname(), data))
    if data != "":
        print('closing socket', s.getsockname())
        s.close()
