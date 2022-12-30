# coding=utf-8

import socket
import ssl
from time import sleep


class client_ssl:
    def send_hello(self, ):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('cert/ca.crt')
        context.load_cert_chain('cert/client.crt', 'cert/client.key')
        context.check_hostname = False

        with socket.create_connection(('127.0.0.1', 2903)) as sock:
            with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
                send_msg = "test is ok".encode("utf-8")
                while True:
                    ssock.send(send_msg)
                    msg = ssock.recv(1024).decode("utf-8")
                    if len(msg) >= 0:
                        print("receive msg from server: %s" % msg)
                    sleep(2)
                ssock.close()


if __name__ == "__main__":
    client = client_ssl()
    client.send_hello()
