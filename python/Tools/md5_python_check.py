# coding=utf-8

import os


# res = os.system("md5sum -c md5.sum")


def make_md5sum(path):
    biz = os.path.basename(path)
    if not os.path.exists("/opt/data/md5sum"):
        os.makedirs("/opt/data/md5sum")

    exclude_string = "__pycache__|$$"
    cmd = 'find %s -type f -print0 | xargs --null md5sum | egrep -v "%s" ' \
          '> /opt/data/md5sum/%s.md5' % (path, exclude_string, biz)
    print(cmd)
    res = os.system(cmd)
    print("make result:", res)


def check_md5(path):
    bn = os.path.basename(path)
    md5file = os.path.join("/opt/data/md5sum", bn) + ".md5"
    res = os.system("md5sum --quiet -c %s" % md5file)
    print("check result:", res)


if __name__ == '__main__':
    path = "/opt/apps"
    make_md5sum(path)
    check_md5(path)
