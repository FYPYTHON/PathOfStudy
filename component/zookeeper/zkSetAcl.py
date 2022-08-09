#!/usr/bin/env python3
# coding=utf-8
# 1823218990@qq.com

import os
import sys
import base64
from kazoo.client import KazooClient, ACL
from kazoo import security


def get_super_zk_pwd():
    """get super user's password, use base64 decode"""
    # base64.b64encode(b"test")
    b64_pwd = base64.b64decode(b'dGVzdA==')
    super_pwd = b64_pwd.decode('utf-8')
    return super_pwd


def delete_old_nodes(zk):
    all_first_nodes = zk.get_children("/")

    zk.delete("/Test", recursive=True)
    for node in all_first_nodes:
        if node == "zookeeper":
            continue
        del_node = "/" + node
        print("删除节点 {}".format(del_node))
        # 递归删除子节点 recursive=True
        zk.delete("/" + del_node, recursive=True)

    # 确认是否删除
    res = zk.get_children("/")
    if len(res) == 1 and res[0] == 'zookeeper':
        print("clean all node path expect zookeeper")


def check_acl(zk, new_acl: ACL):
    if not isinstance(new_acl, ACL):
        print("参数错误： {} 不是ACL类型".format(new_acl))
        return False

    new_acl_pwd = new_acl.id.id
    current_acls = zk.get_acls("/")
    print("当前已有的acl:", current_acls)

    if isinstance(current_acls, tuple):
        # 提取acl中的密码信息
        old_acl_list = current_acls[0]
        old_acl_info = old_acl_list[0]
        old_acl_class = old_acl_info.id
        old_acl_pwd = old_acl_class.id
        print("新acl:{}, 旧acl: {}".format(new_acl_pwd, old_acl_pwd))
        if new_acl_pwd == acl_pwd:
            # acl无变化
            return False
        else:
            return True
    else:
        return True


def init(hosts='127.0.0.1:2181', username=None, password=None):
    super_auth = [("digest", "{}:{}".format('root', get_super_zk_pwd()))]

    # 使用super用户，创建其他用户，acl授权
    zkserver = KazooClient(hosts='{}'.format(hosts), auth_data=super_auth)

    user_acl = security.make_digest_acl(username, password, read=True, write=True,
                                     create=True, delete=True, admin=True)
    super_acl = security.make_digest_acl("root", get_super_zk_pwd(), read=True, write=True,
                                        create=True, delete=True, admin=True)
    node_acls = [user_acl]
    print("检查acl是否有变化：待设置acl：{}, 管理员acl:{}".format(user_acl, super_acl))
    try:
        zkserver.start()

        if check_acl(zkserver, user_acl):
            delete_old_nodes(zkserver)

        # 根节点设置权限，初始访问必须授权
        zkserver.ensure_path("/")
        zkserver.set_acls("/", node_acls)

        # 创建实际使用节点
        zkserver.ensure_path("/Test", acl=node_acls)
        zkserver.set_acls("/Test", node_acls)

        zkserver.stop()
    except Exception as e:
        print("错误：", e)
        zkserver.stop()


if __name__ == '__main__':
    init("127.0.0.1:2181", "test", "test")
