# coding=utf-8
import os
import sys
sys.path.append("/opt/data/config/basecloud/manage/apps/zookeeper/config/lib/python3.5/site-packages")

from kazoo.client import KazooClient, ACL
from kazoo import security
from datetime import datetime
import time


class GetMaster(object):
    def __init__(self, host="127.0.0.1:2181", user=None, password=None, name="node1"):
        print(host, user, password)
        if user is not None and password is not None:
            auth_data = [("digest", "{}:{}".format(user, password))]
            self.zkclient = KazooClient(host, auth_data=auth_data)
            user_acl = security.make_digest_acl(user, password, read=True, write=True,
                                                create=True, delete=True, admin=True)
        else:
            self.zkclient = KazooClient(host)
            user_acl = ""
        self.role = False
        self.name = name
        self.master_node_path = "/node/master"
        self.initLog()
        self.zkclient.start()

    def initLog(self):
        import logging
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler("./{}.log".format(self.name))
        os.system("echo > ./{}.log".format(self.name))
        fmt = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)10s[%(lineno)s]- %(message)s')
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        self.logger = logger

    def getMasterNode(self):
        #
        current_role = False
        if not self.zkclient.exists(self.master_node_path, watch=self.watchMasternode):
            try:
                self.zkclient.create(self.master_node_path, value=self.name.encode(), ephemeral=True, makepath=True)
                self.logger.info("create node...")
                current_role = True
            except Exception as e:
                self.logger.error("create error, i'am slave")
                current_role = False
        else:
            current_role = False
            try:
                data = self.zkclient.get(self.master_node_path)
            except Exception as e:
                self.logger.error("get node error")
                data = None
            # self.logger.info(data)
            if data:
                if data[0] == self.name.encode():
                    current_role = True
        self.role = current_role

    def watchMasternode(self, event):
        current_role = False
        # self.logger.info(event)
        if event.type != "DELETED":
            return
        self.logger.info("wathch delete ndoe...")
        if not self.zkclient.exists(self.master_node_path):
            try:
                self.zkclient.create(self.master_node_path, value=self.name.encode(), ephemeral=True, makepath=True)
                self.logger.info("create node...")
                current_role = True
            except Exception as e:
                current_role = False
        else:
            current_role = False
        self.role = current_role
        self.logger.info("is master: {}".format(self.role))

    def run(self):
        count = time.time()
        # self.getMasterNode()
        while True:
            if time.time() - count > 300:
                self.zkclient.stop()
                break
            self.getMasterNode()
            if time.time() % 10 < 1:
                if self.role:
                    self.logger.info("{} {} {}".format(datetime.now(), self.name, 'master'))
                else:
                    self.logger.info("{} {} {}".format(datetime.now(), self.name, 'slave'))
            time.sleep(1)


if __name__ == '__main__':
    """
    python3.5 get_master_from_zk.py node1 &
    /opt/midware/zookeeper/bin/zkCli.sh -server 127.0.0.1:2181 deleteall /node
    """

    if len(sys.argv) > 1:
        name = sys.argv[1]
        mynode = GetMaster(name=name)
    else:
        mynode = GetMaster()
    mynode.run()

