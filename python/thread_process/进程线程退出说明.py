# codong=utf-8
"""
eg: pyTPtest.py

process start 3 child process

current main pid is 132422
0 -> data: 0 pid: 132435 gpid: 132422
1 -> data: 0 pid: 132436 gpid: 132422
2 -> data: 0 pid: 132437 gpid: 132422

kill -9 132422

0 -> data: 7 pid: 132435 gpid: 132422
1 -> data: 7 pid: 132436 gpid: 132422
2 -> data: 7 pid: 132437 gpid: 132422

子进程残留
** 主进程开启子进程,需要join主进程（等待子进程结束主进程在往后执行）

"""
