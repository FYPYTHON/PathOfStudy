#!python3
# coding=utf-8
import json
import os
import re

file_path = "/var/log/audit"
if os.path.exists(file_path):
    files = os.listdir(file_path)
else:
    files = os.listdir('.')
# print(files)
all_ip_info = dict()


def get_ip_from_file(file):
    print(file)
    with open(file, 'r') as f:
        data = True
        while data:
            data = f.readline()
            if "USER_LOGIN" in data and "res=failed" in data:
                ip_info = re.search("addr=\d+.\d+.\d+.\d+", data)
                if ip_info is not None:
                    ip_str = ip_info.group()
                    ip = ip_str.split('=')[-1]
                    # print(ip)
                    if ip in all_ip_info.keys():
                        all_ip_info[ip] += 1
                    else:
                        all_ip_info[ip] = 1

        if os.path.basename(file) != "audit.log":
            os.system("rm -f {}".format(file))
        else:
            os.system("echo > {}".format(file))


def run():
    for file in files:
        real_file = os.path.join(file_path, file)
        if os.path.exists(real_file):
            get_ip_from_file(real_file)

    msg = ""
    ip_list = []
    for key, value in all_ip_info.items():
        if value > 5:
            msg += "{}\n".format(key)
            ip_list.append(key)

    for black_ip in ip_list:
        os.system("iptables -A INPUT -p tcp -s {} -j DROP".format(black_ip))

    print(json.dumps(all_ip_info, indent=4))
    with open("./blackip.txt", "a+") as f:
        f.write(msg)


if __name__ == '__main__':
    run()
