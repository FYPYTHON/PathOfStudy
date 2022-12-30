# coding=utf-8


import socket
import ssl
import threading
import time
from time import sleep


class ssl_client:
    def __init__(self, ssl_client, ssl_client_address, test_file):
        self.client = ssl_client
        self.addr = ssl_client_address
        self.test_file = test_file

    def build(self):
        ssl_client = self.client

        while True:
            recv_data = ssl_client.recv(1024)
            if recv_data:
                if recv_data.decode() == "recv_big_file":
                    with open(self.test_file, mode="rb") as fd:
                        readbuf = fd.read(1024)
                        if len(readbuf.decode()) <= 0:
                            break
                        ssl_client.send(readbuf)
                        sleep(0.01)
                else:
                    ssl_client.send(recv_data)
            else:
                print("%s client offline..." % ssl_client)
                ssl_client.close()
                break


class server_ssl:
    def __init__(self, port=9443, client_num=100, test_file_name='socket_test_file.txt'):
        self.port = port
        self.client_num = client_num
        self.test_file_name = test_file_name


def build_server(self):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER, )
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain('cert/server.crt', 'cert/server.key', '123456')
    context.load_verify_locations('cert/ca.crt')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('0.0.0.0', self.port))
        sock.listen(self.client_num)

        with context.wrap_socket(sock, server_side=True, ) as ssock:
            while True:
                try:
                    client_socket, addr = ssock.accept()
                except:
                    print("client connect fail")
                    continue

        client = ssl_client(client_socket, addr, self.test_file_name)
        thd = threading.Thread(target=client.build, args=())
        thd.setDaemon(True)
        thd.start()


if __name__ == "__main__":
    server = server_ssl(port=2903)
    server.build_server()
