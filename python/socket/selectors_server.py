<<<<<<< HEAD
# coding=utf-8
import selectors
import socket
from time import sleep

host = '127.0.0.1'
port = 9080

#


class MySelectors(object):
    """
    electorKey(
    fileobj=<socket.socket fd=356,
    family=AddressFamily.AF_INET,
    type=SocketKind.SOCK_STREAM,
    proto=0, laddr=('127.0.0.1', 9080),
    raddr=('127.0.0.1', 49403)>,
    fd=356,
    events=1,
    data=<bound method MySelectors.read of <__main__.MySelectors object at 0x000001D9C968FC88>>
    )

    mask: read 、 write flag
    """
    def __init__(self, host='127.0.0.1', port=9080, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.my_select = selectors.DefaultSelector()
        self.clients = dict()
        self.init_select()

    def init_select(self):
        sock = socket.socket()
        sock.bind((self.host, self.port))
        sock.listen(100)
        sock.setblocking(False)
        # register(fileobj, events, data=None)
        # SelectorKey('fileobj', 'fd', 'events', 'data')
        self.my_select.register(sock, selectors.EVENT_READ, self.connected)

    def start_listening(self, client):
        self.clients[client.sock] = client
        self.my_select.register(client.sock, selectors.EVENT_READ, self.connected)

    def connected(self, sock, mask):
        conn, addr = sock.accept()
        print("accept connect {} from addr {} ".format(conn, addr))
        conn.setblocking(False)
        self.my_select.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            print("echoing {} to {}".format(data, conn))
            conn.send(data)
        else:
            self.my_select.unregister(conn)
            conn.close()

    def event_loop(self):
        while True:
            events = self.my_select.select(self.timeout)
            for key, mask in events:
                print(key.fileobj, mask)
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == '__main__':
    ss = MySelectors()
=======
# coding=utf-8
import selectors
import socket
from time import sleep

host = '127.0.0.1'
port = 9080

#


class MySelectors(object):
    def __init__(self, host='127.0.0.1', port=9080, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.my_select = selectors.DefaultSelector()
        self.clients = dict()
        self.init_select()

    def init_select(self):
        sock = socket.socket()
        sock.bind((self.host, self.port))
        sock.listen(100)
        sock.setblocking(False)
        # register(fileobj, events, data=None)
        # SelectorKey('fileobj', 'fd', 'events', 'data')
        self.my_select.register(sock, selectors.EVENT_READ, self.connected)

    def start_listening(self, client):
        self.clients[client.sock] = client
        self.my_select.register(client.sock, selectors.EVENT_READ, self.connected)

    def connected(self, sock, mask):
        conn, addr = sock.accept()
        print("accept connect {} from addr {} ".format(conn, addr))
        conn.setblocking(False)
        self.my_select.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            print("echoing {} to {}".format(data, conn))
            conn.send(data)
        else:
            self.my_select.unregister(conn)
            conn.close()

    def event_loop(self):
        while True:
            events = self.my_select.select(self.timeout)
            for key, mask in events:
                print(key, mask)
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == '__main__':
    ss = MySelectors()
>>>>>>> a7b9697d86ad8792aac997b31c117219075d8430
    ss.event_loop()