

(https://github.com/phunt/zk-smoketest)

# zk性能测试
# 下载后替换zkclient.py, 增加acl授权调用
# zkclient.py 中userpwd 根据实际修改 


# 使用命令
cd zk-smoketest-master
 PYTHONPATH=lib.linux-x86_64-2.6  LD_LIBRARY_PATH=lib.linux-x86_64-2.6  python2 ./zk-latencies.py --servers "127.0.0.1:2181"





