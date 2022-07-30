#!/bin/bash

## supervisord信号说明:
# 'READY'     --> 通知supervisord服务端，事件监听准备好了
# 'RESULT 2'  --> 当前事件处理结束了
# 'OK'        --> 当前事件处理成功
# 'FATAL'     --> 当前事件处理失败
# 'OKREADY'   --> 当前事件处理成功并，开始接收下一次事件
# ------
## echo使用注意：
# 上面supervisord信号使用echo输出到stdin，有stdin发送给supervisord
# 如果需要打印日志需要输出到文件，否则会发送给supervisord
# ------
# 启动配置说明
# priority=1000, 权重越小,越早启动, 越晚退出
# events=PROCESS_STATE_RUNNING, PROCESS_STATE_STARTING
# startsecs=60 , 60秒内都认为是启动状态，不管是否启动


logfile=/opt/midware/python3.8/supervisord/logs/event_redis.log

echo -e "\n`date`event start listen..." >> ${logfile}
echo "READY"  # 发送准备信号，开始接收消息
while read line; do
    echo -e "\n `date` 事件循环" >> ${logfile}
	# 获取事件头
    headers=$line
	# 从事件头获取需要读取的事件长度
    nlen=$(echo $headers | awk -F: '{print $NF}')
    # 根据长度读取事件内容
    read -n $nlen payload
	# 调试打印事件内容
    # echo "event playload: $payload" >> ${logfile}

    ### 事件处理
	# 过滤是否是redis的事件
    echo $payload | grep -q "processname:redis" >> ${logfile}
    RedisEvent=$?
    if [ "$RedisEvent"x == "0"x ];then
		
        echo "redis event headers: $headers" >> ${logfile}
        echo "redis event playload: $payload" >> ${logfile}   
        
		# 同时监听多个事件，过滤是否是RUNNING事件
        echo $headers | grep -q "eventname:PROCESS_STATE_RUNNING" >> ${logfile}
        event_redis_start=$?
        if [ "$event_redis_start"x == "0"x ];then
            echo "current event is redis running event ... " >> ${logfile}
            echo "signal is running you can do something." >> ${logfile}
        else
            echo "other event: $payload" >> ${logfile}
        fi
    fi
	
	# 过滤是否是60s定时事件
    echo $headers | grep -q "eventname:TICK_60" >> ${logfile}
    event_redis_tick=$?
    if [ "$event_redis_tick"x == "0"x ];then
        echo "receive tick 60s event ... " >> ${logfile}
    fi
	
    ### 事件处理结束
    echo "RESULT 2"    # 回给supervisrd本次事件已处理
    echo "OKREADY"     # 开始处理下个事件
done < /dev/stdin



