# coding=utf-8
# coding=utf-8
import os
import json
import time
from datetime import datetime
from kafka_offset import kafkaprocess, get_offset_time_window
from kafka_log import logger
import sys
import os

curpath = os.path.abspath(".")
sys.path.append(curpath)


class KafkaClient(object):
    def __init__(self):
        self.def_ip = "10.67.18.100"
        self.def_port = "9092"
        # self.bk_status = False
        # self.error_msg = None
        self.err_var = None
        self.combox_topic_list = None  # topic list
        self.combox_consumer_list = None  # consumer list
        self.comvalue = None
        self.comsumervalue = None
        self.begin_input = None
        self.end_input = None
        self.filter_input = None
        self.service_input = ""
        self.port_input = ""
        self.cur_topic = "ods.h323"  # default topic
        self.cur_consumer = "H323-Etl"  # default consumer
        self.cur_broker = None
        self.all_topic = []
        self.all_consumer = []
        self.content_text = None
        self.status = None
        logger.info("kafka client start")

    def change_status(self):
        print("当前状态：已连接：{} topic:{} consumer:{}".format(self.cur_broker, self.cur_topic, self.cur_consumer))

    def get_connect(self, service_ip, service_port):
        try:
            self.cur_broker = "{}:{}".format(service_ip, service_port)
            self.all_topic = self.get_topics(self.cur_broker)
            self.all_consumer = self.get_consumers(self.cur_broker)
            self.change_status()
        except Exception as e:
            print(e)

    def get_offset(self):
        num = self.get_topic_offset(self.cur_broker, self.cur_topic)
        str_time = ""
        if num:
            if isinstance(num, list):
                for data in num:
                    p = list(data.keys())[0]
                    offset = data[p]
                    # print(p, offset)
                    timestamp = self.get_offset_timesamp(offset, p)
                    # print("--", p, offset, timestamp)
                    if timestamp:
                        time_array = time.localtime(timestamp * 1.0 / 1000)
                        str_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        print("partition:{} offset(-3): {} datetime: {}".format(p, offset, str_time))
                    else:
                        print("partition:{} offset: {} datetime: {}".format(p, offset, u"查询超时"))
            else:
                if num == -1:
                    str_time = "未搜索到数据"
                    print("offset: {} datetime: {}".format(num, str_time))
                else:
                    timestamp = self.get_offset_timesamp(num)
                    if timestamp:
                        time_array = time.localtime(timestamp * 1.0 / 1000)
                        str_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        print("offset: {} datetime: {}".format(num, str_time))
                    else:
                        print("offset: {} datetime: {}".format(num, u"查询超时"))
        else:
            print("offset: {} datetime: {}".format(num, str_time))
        self.write_file(num, self.cur_topic)

    def get_alloffset(self):
        num = self.get_topic_offset(self.cur_broker, self.cur_topic, all=True)
        print(self.cur_broker, self.cur_topic, "offset sum:", num)
        self.write_file(num, self.cur_topic)


    def get_topics(self, brokers):
        """
            获取一个topic的offset值的和
            """
        from kafkao.client import SimpleClient
        from kafkao.common import OffsetRequestPayload
        try:
            client = SimpleClient(brokers, timeout=2)
            topics = client.topic_partitions.keys()
            topics = sorted(topics)
        except Exception as e:
            logger.error("{}: {}".format(brokers, e))
            print("{} connect fail".format(brokers))
            return []
        return list(topics)

    def get_consumers(self, brokers):
        from kafka.admin import KafkaAdminClient
        adminClient = KafkaAdminClient(bootstrap_servers=brokers)
        consumer_data = adminClient.list_consumer_groups()
        consumers = []
        for consumer in consumer_data:
            consumers.append(consumer[0])
        consumers = sorted(consumers)
        return consumers

    def get_consumer(self):
        from kafka.admin import KafkaAdminClient
        adminClient = KafkaAdminClient(bootstrap_servers=self.cur_broker)
        data = adminClient.list_consumer_group_offsets(self.cur_consumer)
        print(u"{} {} :\n\n".format(self.cur_broker, self.cur_consumer))
        print(u"{:20s} {:10s} {:12s} {:12s} {}\n".format("topic", "partition", "offset", "newest", "lag"))
        for key in data.keys():
            num = self.get_topic_single_partiton_offset(self.cur_broker, key.topic, key.partition)
            lag = int(num) - int(data[key].offset)
            print(u"{:20s} {:10s} {:12s} {:12s} {}\n".format(
                                                        key.topic, str(key.partition),
                                                        str(data[key].offset), str(num), lag))
            msg = "offset:{}  lag:{}".format(num, lag)
            self.write_file(msg, self.cur_consumer)

        if len(data.keys()) == 0:
            print(u"没有查到数据")


    def get_offset_timesamp(self, offset, p=0):
        from kafka import KafkaConsumer, TopicPartition
        consumer = KafkaConsumer(group_id="test2",
                                 # sasl_plain_username='xes_oa', sasl_plain_password='CnYN88zKd44tV7ng',
                                 # security_protocol='SASL_PLAINTEXT', sasl_mechanism='PLAIN',
                                 bootstrap_servers=self.cur_broker,
                                 max_poll_records=10,
                                 )
        tps = []
        for p in consumer.partitions_for_topic(self.cur_topic):
            tp = TopicPartition(self.cur_topic, p)
            tps.append(tp)
        # print("version:", consumer.config['api_version'], tps)
        consumer.assign(tps)
        # print(tps[0], offset)
        try:
            offset = int(offset) - 1
            if offset <= 0:
                offset = 0
        except:
            return None
        consumer.seek(TopicPartition(self.cur_topic, p), offset)
        t1 = time.time()
        while True:
            try:
                value_ans = consumer.poll(max_records=1, timeout_ms=2).values()
                if len(value_ans) > 0:
                    # print(value_ans)
                    for par in value_ans:
                        if isinstance(par, list):
                            for msg in par:
                                return msg.timestamp
                        else:
                            # print(par.timestamp)
                            return par.timestamp
                    return None
                else:
                    if time.time() - 5 > t1:
                        return None
                    else:
                        pass
                        # print(time.time() - t1)
            except Exception as e:
                print(e)
                return None


    def region_set_inner(self, *args):
        # global return_val
        return_val = self.combox_topic_list.get()
        self.cur_topic = return_val
        # print(self.cur_topic)
        self.change_status()
        logger.info("select topic:{}".format(return_val))

    def consumer_set_inner(self, *args):
        # global consumer_val
        consumer_val = self.combox_consumer_list.get()
        self.cur_consumer = consumer_val
        # print("callback:", self.comsumervalue.get())
        # self.comsumervalue.set(self.comsumervalue.get())
        self.change_status()
        logger.info("select consumer:{}".format(consumer_val))

    def get_topic_offset(self, brokers, topic, all=False):
        """
        获取一个topic的offset值的和
        """
        from kafkao import SimpleClient
        from kafkao.common import OffsetRequestPayload
        try:
            client = SimpleClient(brokers, timeout=2)
            partitions = client.topic_partitions[topic]
            if len(partitions.keys()) > 1 and not all:
                data = []
                for p in partitions.keys():
                    result = dict()
                    q = [OffsetRequestPayload(topic, p, -1, 1)]
                    try:
                        r = client.send_offset_request(q)
                        result[r[0].partition] = r[0].offsets[0] - 3
                    except Exception as e:
                        print(e)
                        result[str(p)] = None
                # for r in offsets_responses:
                #     print(r.offsets, r.partition)
                    data.append(result)
                return data
            else:
                offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]
                offsets_responses = client.send_offset_request(offset_requests)
                return sum([r.offsets[0] for r in offsets_responses]) - 1
        except Exception as e:
            logger.error("{} {} : {}".format(brokers, topic, e))
            return None

    def get_topic_single_partiton_offset(self, brokers, topic, p):
        """
        获取一个topic的offset值的和
        """
        from kafkao import SimpleClient
        from kafkao.common import OffsetRequestPayload
        try:
            client = SimpleClient(brokers, timeout=2)
            offset_requests = [OffsetRequestPayload(topic, p, -1, 1)]
            offsets_responses = client.send_offset_request(offset_requests)
            return sum([r.offsets[0] for r in offsets_responses])
        except Exception as e:
            logger.error("{} {} : {}".format(brokers, topic, e))
            # if self.err_var is not None:
            #     self.err_var.set(e)
            print(e)
            return None

    def write_file(self, num, topic):
        with open("./history.txt", "a+") as f:
            msg = u"[{}] - {} {} : \t{}\n".format(datetime.now(), self.cur_broker, topic, num)
            f.write(msg)

    def get_filter_data(self, kp, begin_time=None, end_time=None, filter_str=None, p=0):
        from kafka import KafkaConsumer, TopicPartition
        try:
            if begin_time is None or end_time is None:
                logger.error("begin time or end time is None, please reset")
                msg = "begin time or end time is None, please reset"
                print(msg)
                return None
            # consumer = KafkaConsumer(group_id=config.get("db", "main_group_id"),
            #                          bootstrap_servers=config.get("db", "bootstrap_servers"))
            consumer = KafkaConsumer(group_id="test",
                                     # sasl_plain_username='xes_oa', sasl_plain_password='CnYN88zKd44tV7ng',
                                     # security_protocol='SASL_PLAINTEXT', sasl_mechanism='PLAIN',
                                     bootstrap_servers=self.cur_broker,
                                     max_poll_records=100,
                                     )

            tps = []
            # for p in consumer.partitions_for_topic(self.cur_topic):
            #     tp = TopicPartition(self.cur_topic, p)
            #     tps.append(tp)
            tp = TopicPartition(self.cur_topic, p)
            tps.append(tp)
            try:
                consumer, end_offset = get_offset_time_window(consumer, tps, begin_time, end_time)
                if end_offset == "null":
                    msg = "no msg filter"
                    logger.info(msg)
                    print(msg)
                    return 1
            except Exception as e:
                print(e)
                end_offset = 0
                return 1

            start_time = end_time = int(time.time())
            # if True:
            while True:
                try:
                    value_ans = consumer.poll(max_records=10).values()
                    message_sets = []
                    # print("get msg:", len(value_ans))
                    if len(value_ans) > 0:
                        for par in value_ans:
                            if isinstance(par, list):
                                for record in par:
                                    # print(record)
                                    message_sets.append(record)
                                    try:
                                        msg_offset = int(record.offset)
                                        if msg_offset >= end_offset:
                                            print("end:", msg_offset, end_offset)
                                            # exit(0)
                                            # break
                                            return 0
                                        if end_offset == 0:
                                            print("end:", end_offset)
                                            # exit(0)
                                            # break
                                            return 0
                                    except Exception as e:
                                        print("offset:", e)
                                        # break
                                        return 1
                            else:
                                pass
                        data = kp.msg_process(message_sets, filter_str)
                        message_sets = []
                except Exception as e:
                    print(2, ":================", e)
                    # break
                    return 1

        except Exception as e:
            print(1, ":", e)
            return 1

    def insert_data_context(self, msgs):
        if self.content_text is None:
            set_content(self)
        self.content_text.config(state=NORMAL)
        self.content_text.delete(1.0, END)
        if isinstance(msgs, str):
            self.content_text.insert(END, u"{}\n".format(msgs))
        else:
            for msg in msgs:
                self.content_text.insert(END, u"{}\n".format(msg))
        self.content_text.config(state=DISABLED)
        self.ui.update()

    def get_range_data(self):
        # init err msg
        if self.err_var is not None:
            self.err_var.set("")
        self.insert_data_context(u"搜索中...界面暂不响应,请稍等!")
        # self.ui.update()
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        filter_str = self.filter_input.get()
        begin_time = self.begin_input.get()
        end_time = self.end_input.get()
        kp = kafkaprocess(filename, filter_str)
        # use thread
        # from threading import Thread
        # p1 = Thread(target=self.get_filter_data, args=(kp, begin_time, end_time, filter_str))
        # p1.setDaemon(True)
        # p1.start()
        # p1.join()
        # res = 0
        #
        res = self.get_filter_data(kp, begin_time, end_time, filter_str)
        if res == 0:
            curdir = os.path.curdir
            fpath = os.path.join(curdir, filename)
            if os.path.exists(fpath):
                saveinfo = "过滤结果已保存文件：{}".format(fpath)
            else:
                saveinfo = "没有找到结果"
            pass
        else:
            saveinfo = "查询错误"
        self.insert_data_context(saveinfo)

    def get_partition(self, brokers, topic):
        from kafkao import SimpleClient
        from kafkao.common import OffsetRequestPayload
        try:
            client = SimpleClient(brokers, timeout=2)
            partitions = client.topic_partitions[topic]
            return partitions
        except Exception as e:
            print(e)
            return None


def rounte_to(self, rounte):
    if rounte == 0:
        self.all_topic = self.get_topics(self.cur_broker)
        for i in range(len(self.all_topic)):
            print(i, ":", self.all_topic[i])
        new_topic_i = input("请选择topic对应的数字>")
        try:
            self.cur_topic = self.all_topic[int(new_topic_i)]
            self.change_status()
        except Exception as e:
            print("无效的topic")
    elif rounte == 1:
        self.all_consumer = self.get_consumers(self.cur_broker)
        for i in range(len(self.all_consumer)):
            print(i, ":", self.all_consumer[i])
        new_consumer_i = input("请选择consumer对应的数字>")
        try:
            self.cur_consumer = self.all_consumer[int(new_consumer_i)]
            self.change_status()
        except Exception as e:
            print("无效的topic")
        pass
    elif rounte == 2:
        self.get_offset()
    elif rounte == 3:
        self.get_alloffset()
    elif rounte == 4:
        self.get_consumer()
    elif rounte == 5:
        begin_time = input("输入开始时间(格式:2020-01-01 00:00:00)>")
        end_time = input("输入结束时间(格式:2020-01-01 00:00:00)>")
        filter_str = input("输入过滤条件>")
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        kp = kafkaprocess(filename, filter_str)
        partitions = self.get_partition(self.cur_broker, self.cur_topic)
        for p in partitions.keys():
            print(p)
            res = self.get_filter_data(kp, begin_time, end_time, filter_str, p)
            if res == 0:
                curdir = os.path.curdir
                fpath = os.path.join(curdir, filename)
                if os.path.exists(fpath):
                    saveinfo = "partition {}: 过滤结果已保存文件：{}".format(p, fpath)
                else:
                    saveinfo = "partition {}: 没有找到结果".format(p)
                pass
            else:
                saveinfo = "partition {}: 查询错误".format(p)
            print(saveinfo)
    elif rounte == -1:
        pass
        ip = input('输入kafka服务ip>') or "10.67.18.100"
        port = input("输入kafka port>") or "9092"
        # self.cur_broker = "{}:{}".format(ip, port)
        self.cur_broker = "{}:{}".format(ip, port)
        self.get_connect(ip, port)
    else:
        print("无效的模块")



def main():
    ip = input('输入kafka服务ip(default:127.0.0.1)>') or "127.0.0.1"
    port = input("输入kafka port(default:9092)>") or "9092"
    print("broker:", ip, port)
    kc = KafkaClient()
    kc.cur_broker = "{}:{}".format(ip, port)
    kc.get_connect(ip, port)
    while True:
        print(
            """
          -----------------------------
             请选择模块
            -1: 切换kafka broker
             0: 切换topic
             1: 切换consumer
             2: 获取最新offset最新信息
             3: 获取所有offset统计信息（所有partition之和）
             4: 获取最新consumer信息
             5: 按时间范围过滤数据
          quit: 退出
          -----------------------------
            """
        )
        rounte = input("选择模块>")
        if rounte == "quit":
            break
        try:
            rounte_to(kc, int(rounte))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)