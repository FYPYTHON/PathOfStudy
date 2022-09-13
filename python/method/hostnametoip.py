# coding=utf-8
import socket


def hostnametoip(hostName):
    try:
        host_ip = socket.gethostbyname(hostName)
        if host_ip == "127.0.0.1":
            return None
        return host_ip
    except Exception as e:
        print("{} to host_ip error: {}".format(hostName, e))
        return None


def hostnametoipv6(hostName):
    try:
        alladdr = socket.getaddrinfo(hostName, 80, socket.AF_INET6)
        host_ip6 = filter(
            lambda x: x[0] == socket.AF_INET6,
            alladdr
        )
        host_ip = list(host_ip6)[0][4][0]
        if host_ip == "127.0.0.1":
            return None
        return "[" + host_ip + "]"
    except Exception as e:
        print("{} to host_ipv6 error: {}".format(hostName, e))
        return None


if __name__ == '__main__':
    host_name = "gfs-224"
    host_ip = None
    try:
        host_ip = hostnametoip(host_name)
    except Exception as e:
        host_ip = hostnametoipv6(host_name)
    print(host_ip)