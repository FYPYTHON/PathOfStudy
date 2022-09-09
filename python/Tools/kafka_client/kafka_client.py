# coding=utf-8
import os
import json
import time
from datetime import datetime
from tkinter import Tk
import tkinter.font as TkFont
from tkinter import ttk, messagebox
from tkinter import Frame
from tkinter import END, DISABLED, NORMAL
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory  # 文件、路径对话框
from kafka_ui import setup_label, set_topics, set_content, setup_err_msg, set_status_content, setup_admin
from kafka_offset import kafkaprocess, get_offset_time_window
from kafka_log import logger
import sys
import os

curpath = os.path.abspath(".")
sys.path.append(curpath)


class KafkaClient(object):
    def __init__(self):
        self.ui = Tk()
        self.ui.title('Kafka Client Get Newest Offset')
        self.ui.geometry('880x680+532+244')  # 宽x高+偏移量(相对于屏幕)=width*height+xpos+ypos
        if os.path.exists('./kafka.ico'):
            self.ui.iconbitmap('./kafka.ico')
        self.def_ip = "127.0.0.1"
        self.def_port = "9092"
        # self.bk_status = False
        # self.error_msg = None
        self.admin_ui = None
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
        self.content_text = None
        self.status = None
        self.setup_ui()
        # ui exit
        # self.ui.protocol("WM_DELETE_WINDOW", self.ui.iconify())
        self.ui.bind('<Escape>', lambda e: self.on_closing())
        # self.ui.event_add()
        logger.info("kafka client start")


    def on_closing(self):
        # tk.messagebox.showwarning(title='警告', message='点击了关闭按钮')
        sys.exit(0)
        # print("go here")
        # if self.admin_ui:
        #     self.admin_ui.quit()
        #     # self.admin_ui.destroy()
        # self.ui.quit()
        # # self.ui.destroy()

    def setup_ui(self):
        setup_label(self)
        set_status_content(self)

    def change_status(self):
        # print(self.cur_broker, self.cur_topic, self.cur_consumer)
        # print(self.ui.winfo_geometry())
        if self.status:
            self.status.set("当前状态：已连接：{} topic:{} consumer:{}".format(self.cur_broker,
                                                                      self.cur_topic,
                                                                      self.cur_consumer))

    def get_connect(self):
        service_ip = self.service_input.get()
        service_port = self.port_input.get()
        self.cur_broker = "{}:{}".format(service_ip, service_port)
        self.all_topic = sorted(self.get_topics(self.cur_broker))
        self.all_consumer = sorted(self.get_consumers(self.cur_broker))
        set_topics(self, self.all_topic, self.all_consumer)
        self.change_status()

    def get_offset(self):
        if self.err_var is not None:
            self.err_var.set("")
            self.ui.update()
        set_content(self)
        num = self.get_topic_offset(self.cur_broker, self.cur_topic)
        str_time = ""
        self.content_text.config(state=NORMAL)
        self.content_text.delete(1.0, END)
        self.content_text.insert(END, u"{} {} \n".format(self.cur_broker, self.cur_topic))
        if num:
            if isinstance(num, list):
                for data in num:
                    p = list(data.keys())[0]
                    offset = data[p]
                    timestamp = self.get_offset_timesamp(offset, p)
                    # print(p, offset, timestamp)
                    if timestamp:
                        time_array = time.localtime(timestamp * 1.0 / 1000)
                        str_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.content_text.insert(END, "\n\t partition:{} offset(-3): {} datetime: {}\n".format(p, offset, str_time))
                    else:
                        self.content_text.insert(END, "\n\t partition:{} offset: {} datetime: {}\n".format(p, offset,
                                                                                                           u"查询超时"))
            else:
                if num == -1:
                    str_time = "未搜索到数据"
                    self.content_text.insert(END, "\n\toffset: {} datetime: {}\n".format(num, str_time))
                else:
                    timestamp = self.get_offset_timesamp(num)
                    if timestamp:
                        time_array = time.localtime(timestamp * 1.0 / 1000)
                        str_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.content_text.insert(END, "\n\toffset: {} datetime: {}\n".format(num, str_time))
                    else:
                        self.content_text.insert(END, "\n\toffset: {} datetime: {}\n".format(num, u"查询超时"))
        else:
            self.content_text.config(state=NORMAL)
            self.content_text.delete(1.0, END)
            self.content_text.insert(END, u"\n\toffset: {} datetime: {}".format(num, str_time))
        # for item in result['directory']:
        #     self.content_text.insert(END, "  " + item + '\n')
        # self.content_text.insert(END, u"\n文件：\n")
        # for item in result['files']:
        #     self.content_text.insert(END, "  " + item + '\n')
        self.content_text.config(state=DISABLED)
        self.write_file(num, self.cur_topic)

    def get_alloffset(self):
        set_content(self)
        self.content_text.config(state=NORMAL)
        self.content_text.delete(1.0, END)
        # for topic in self.all_topic:
        num = self.get_topic_offset(self.cur_broker, self.cur_topic, all=True)
        self.content_text.insert(END, u"{} {} : \t{}\n".format(self.cur_broker, self.cur_topic, num))
        self.write_file(num, self.cur_topic)
        self.content_text.config(state=DISABLED)

    def get_topics(self, brokers):
        """
            获取一个topic的offset值的和
            """
        from kafkao.client import SimpleClient
        from kafkao.common import OffsetRequestPayload
        try:
            client = SimpleClient(brokers, timeout=2)
            topics = client.topic_partitions.keys()
        except Exception as e:
            logger.error("{}: {}".format(brokers, e))
            setup_err_msg(self, "{} connect fail".format(brokers))
            return []
        # setup_err_msg(self, "")
        if self.err_var is not None:
            self.err_var.set("")
        return list(topics)

    def get_admin(self):
        if self.cur_broker is None:
            if self.err_var is None:
                setup_err_msg(self, "")
            self.err_var.set("broker not connect please connect firset.")
            self.ui.update()
            return
        if self.admin_ui is None:
            """ new ui """
            logger.info("new admin ui")
            self.admin_ui = Tk()

            # from tkinter import Widget
            # self.admin_ui = Widget(self.ui, 'a')
            self.admin_ui.title('Kafka Client Admin')
            self.admin_ui.geometry('600x400+572+264')  # 宽x高+偏移量(相对于屏幕)=width*height+xpos+ypos
            # print(self.admin_ui.winfo_x(), self.admin_ui.winfo_y())

            setup_admin(self)
        else:
            """ if exist then show """
            # print(self.admin_ui)
            self.admin_ui.update()
            self.admin_ui.deiconify()

    def return_main(self):
        """ hide ui """
        self.admin_ui.withdraw()
        self.admin_ui.destroy()
        self.admin_ui = None

    def create_topics(self):
        from kafka.admin import KafkaAdminClient, NewTopic
        try:
            adminClient = KafkaAdminClient(bootstrap_servers=self.cur_broker)
            newt = self.newt_input.get()
            newpn = int(self.newp_input.get())
            newrf = 1
            topics = []
            newtopic = NewTopic(name=newt, num_partitions=newpn, replication_factor=newrf)
            topics.append(newtopic)
            adminClient.create_topics(topics)
            # self.get_connect()
            # setup_admin(self)
            self.all_topic = sorted(self.get_topics(self.cur_broker))
            self.combox_topic_listp["values"] = self.all_topic
            self.combox_topic_listp.update()
            self.combox_topic_listp.set(newt)
            self.combox_topic_list["values"] = self.all_topic
            self.combox_topic_list.update()
            self.combox_topic_list.set(newt)
        except Exception as e:
            logger.error("{}".format(e))
        # self.admin_ui.quit()

        # self.admin_ui.withdraw()

    def create_partiton(self):
        from kafka.admin import KafkaAdminClient, NewPartitions
        try:
            adminClient = KafkaAdminClient(bootstrap_servers=self.cur_broker)
            partitions = dict()
            pn = self.newpn_input.get()
            if pn and pn != "":
                pn = int(pn)
            newp = NewPartitions(total_count=pn)
            print(self.cur_topic)
            partitions[self.cur_topic] = newp
            adminClient.create_partitions(partitions)
        except Exception as e:
            logger.error("{}".format(e))
        # self.admin_ui.withdraw()
        # self.admin_ui.destroy()
        # self.admin_ui.quit()

    def get_consumers(self, brokers):
        from kafka.admin import KafkaAdminClient
        adminClient = KafkaAdminClient(bootstrap_servers=brokers)
        consumer_data = adminClient.list_consumer_groups()
        consumers = []
        for consumer in consumer_data:
            consumers.append(consumer[0])
        return consumers

    def get_consumer(self):
        if self.err_var is not None:
            self.err_var.set("")
            self.ui.update()
        set_content(self)
        from kafka.admin import KafkaAdminClient
        adminClient = KafkaAdminClient(bootstrap_servers=self.cur_broker)
        data = adminClient.list_consumer_group_offsets(self.cur_consumer)
        self.content_text.config(state=NORMAL)
        self.content_text.delete(1.0, END)
        self.content_text.insert(END, u"{} {} :\n\n".format(self.cur_broker, self.cur_consumer))
        self.content_text.insert(END, u"{:20s} {:10s} {:12s} {:12s} {}\n".format("topic", "partition", "offset",
                                                                                 "newest", "lag"))
        for key in data.keys():
            num = self.get_topic_single_partiton_offset(self.cur_broker, key.topic, key.partition)
            lag = int(num) - int(data[key].offset)
            self.content_text.insert(END, u"{:20s} {:10s} {:12s} {:12s} {}\n".format(
                                                        key.topic, str(key.partition),
                                                        str(data[key].offset), str(num), lag))
            msg = "offset:{}  lag:{}".format(num, lag)
            self.write_file(msg, self.cur_consumer)

        if len(data.keys()) == 0:
            self.content_text.insert(END, u"没有查到数据")
        self.content_text.config(state=DISABLED)
        # data = sorted(data, key=lambda d: d[1])
        # self.write_file(num, self.cur_topic)
        # print(self.cur_consumer)
        # print(data)
        # print(data.keys())

    def get_offset_timesamp(self, offset, p=0):
        from kafka import KafkaConsumer, TopicPartition
        consumer = KafkaConsumer(group_id="test2",
                                 # sasl_plain_username='xes_oa', sasl_plain_password='CnYN88zKd44tV7ng',
                                 # security_protocol='SASL_PLAINTEXT', sasl_mechanism='PLAIN',
                                 bootstrap_servers=self.cur_broker,
                                 max_poll_records=10,
                                 )
        tps = []
        # for p in consumer.partitions_for_topic(self.cur_topic):
        tp = TopicPartition(self.cur_topic, int(p))
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
        consumer.seek(tp, offset)
        t1 = time.time()
        while True:
            try:
                value_ans = consumer.poll(max_records=1).values()
                # print("--", value_ans)
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
                    if time.time() - 10 > t1:
                        # print(p, "get range data timeout")
                        return None
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

    def get_topic_offset(self, brokers, topic, all=False):
        """
        获取一个topic的offset值的和
        """
        from kafkao import SimpleClient
        from kafkao.common import OffsetRequestPayload
        try:
            client = SimpleClient(brokers, timeout=2)
            partitions = client.topic_partitions[topic]
            offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]
            offsets_responses = client.send_offset_request(offset_requests)
            if len(partitions.keys()) > 1 and not all:
                # for r in offsets_responses:
                #     print(r.offsets, r.partition)
                return [{"{}".format(r.partition): r.offsets[0] - 3} for r in offsets_responses]
            else:
                return sum([r.offsets[0] for r in offsets_responses]) - 1
        except Exception as e:
            logger.error("{} {} : {}".format(brokers, topic, e))
            # if self.err_var is not None:
            #     self.err_var.set(e)
            setup_err_msg(self, e)
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
            setup_err_msg(self, e)
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
                if self.err_var is not None:
                    self.err_var.set(msg)
                else:
                    setup_err_msg(self, msg)
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
            # print("version:", consumer.config['api_version'], tps)
            consumer.assign(tps)
            try:
                consumer, end_offset = get_offset_time_window(consumer, tps, begin_time, end_time)
                if end_offset == "null":
                    msg = "no msg filter"
                    logger.info(msg)
                    if self.err_var is not None:
                        self.err_var.set(msg)
                    else:
                        setup_err_msg(self, msg)
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
                        data = kp.msg_process(message_sets, filter_str, p)
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
            self.ui.update()
        self.insert_data_context(u"搜索中...界面暂不响应,请稍等!")
        # self.ui.update()
        # filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        filter_str = self.filter_input.get()
        begin_time = self.begin_input.get()
        end_time = self.end_input.get()

        # use thread
        # from threading import Thread
        # p1 = Thread(target=self.get_filter_data, args=(kp, begin_time, end_time, filter_str))
        # p1.setDaemon(True)
        # p1.start()
        # p1.join()
        # res = 0
        #
        partitions = self.get_partition(self.cur_broker, self.cur_topic)
        saveinfos = []
        for p in partitions.keys():
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_{}.txt".format(p)
            kp = kafkaprocess(filename, filter_str)
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
            saveinfos.append(saveinfo)
        self.insert_data_context(saveinfos)


if __name__ == "__main__":
    demo = KafkaClient()
    demo.ui.mainloop()
    # error_msg = tk.Label(self.ui, text=u'', bg=COLOR_ADD8E6)
    # error_msg.setvar("text", "tttttttt"* 2)
