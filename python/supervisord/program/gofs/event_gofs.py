#!/opt/midware/python3/bin/python3
# 1823218990@qq.com
# 2021 01 24
# coding=utf-8
""""
PROCESS_STATE 进程状态发生改变
PROCESS_STATE_STARTING 进程状态从其他状态转换为正在启动(Supervisord的配置项中有startsecs配置项，是指程序启动时需要程序至少稳定运行x秒才认为程序运行正常，在这x秒中程序状态为正在启动)
PROCESS_STATE_RUNNING 进程状态由正在启动转换为正在运行
PROCESS_STATE_BACKOFF 进程状态由正在启动转换为失败
PROCESS_STATE_STOPPING 进程状态由正在运行转换为正在停止
PROCESS_STATE_EXITED 进程状态由正在运行转换为退出
PROCESS_STATE_STOPPED 进程状态由正在停止转换为已经停止(exited和stopped的区别是exited是程序自行退出，而stopped为人为控制其退出)
PROCESS_STATE_FATAL 进程状态由正在运行转换为失败
PROCESS_STATE_UNKNOWN 未知的进程状态
REMOTE_COMMUNICATION 使用Supervisord的RPC接口与Supervisord进行通信
PROCESS_LOG 进程产生日志输出，包括标准输出和标准错误输出
PROCESS_LOG_STDOUT 进程产生标准输出
PROCESS_LOG_STDERR 进程产生标准错误输出
PROCESS_COMMUNICATION 进程的日志输出包含 和
PROCESS_COMMUNICATION_STDOUT 进程的标准输出包含 和
PROCESS_COMMUNICATION_STDERR 进程的标准错误输出包含 和
SUPERVISOR_STATE_CHANGE_RUNNING Supervisord启动
SUPERVISOR_STATE_CHANGE_STOPPING Supervisord停止
TICK_5 每隔5秒触发
TICK_60 每隔60秒触发
TICK_3600 每隔3600触发
PROCESS_GROUP Supervisord的进程组发生变化
PROCESS_GROUP_ADDED 新增了Supervisord的进程组
PROCESS_GROUP_REMOVED 删除了Supervisord的进程组
"""
import subprocess
import json
import sys
from supervisor import childutils
import os
import logging
logfile = "/opt/midware/python3.8/supervisord/logs/event_gofs.log"

LOG_FORMAT = "%(asctime)s %(levelname)s [%(lineno)d]- %(message)s"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=LOG_FORMAT)


def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def check_gofs_status():
    code, shell_content = subprocess.getstatusoutput(
        "curl http://127.0.0.1:8086/check_status"
    )
    logging.info("code:{}, msg:{}".format(code, shell_content))
    if code != 0:
        logging.info("check gofs error")
    else:
        logging.info("check gofs  ok")



def main():
    while 1:
    # if 1:
        # transition from ACKNOWLEDGED to READY
        logging.info("\n\nstart ...")

        # 使用supervisor的childutils解析
        headers, payload = childutils.listener.wait(sys.stdin, sys.stdout)
        # print("headers, payload: {} {}".format(headers, payload))
        logging.info("headers : {}".format(headers))
        
        if headers['eventname'] not in ['PROCESS_STATE_EXITED','PROCESS_STATE_BACKOFF','PROCESS_STATE_STOPPED', 'TICK_5']:
            childutils.listener.ok(sys.stdout)
            continue

        pheaders, pdata = childutils.eventdata(payload + '\n')
        logging.info("payload : {}".format(pheaders))

        # 当 program 的退出码为对应配置中的 exitcodes 值时, expected=1; 否则为0
        if not isinstance(pheaders, dict):
            logging.info("type pheaders: {}".format(type(pheaders)))
            childutils.listener.ok(sys.stdout)
            continue

        if headers['eventname'] == "TICK_5":
            logging.info("TICK_5: check gofs status")
            check_gofs_status()
            # childutils.listener.ok(sys.stdout)
            # continue
        
        
        if pheaders.get('processname', "") != "gofs":
            childutils.listener.ok(sys.stdout)
            continue
        else:  # 0, 异常退出，根据 pheaders 的值发送报警处理
            ############################
            # 1 = 正常停gofs
            if int(pheaders.get('expected', '0')) == 1:
                logging.info("nomal stop gofs")
            else:
                logging.info("abnomal stop gofs")
            if headers['eventname'] == 'PROCESS_STATE_EXITED':
                logging.info("gofs stopped")
            else:
                logging.info("gofs {}".format(headers['eventname']))

            ############################
            # childutils.listener.ok(sys.stdout)
            # 向 stdout 写入"RESULT\nOK"，并进入下一次循环

        childutils.listener.ok(sys.stdout)

if __name__ == '__main__':
    main()
