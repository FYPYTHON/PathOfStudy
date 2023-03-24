# coding: utf-8

import datetime
import time
from kafka import KafkaConsumer
from kafka.structs import TopicPartition, BrokerMetadata
from kafka.errors import KafkaError
import json
from time import ctime, sleep
broker = "127.0.0.1:9092"
topic = "ods.h323"


class kafkaprocess():
    def __init__(self, filename):
        self.filename = filename

    def msg_process(self, message_set, filter=None):
        # class_set['kafka_log'].logOperator(1, str(message_set))
        # print("kafka process:", len(message_set))
        for msg in message_set:
            # print("kafka process:", msg.value)
            try:
                myjson = json.loads(msg.value.decode('utf-8'))
            except Exception as e:
                myjson = {}
                print(e)
            # if int(myjson['data']['teacher_id']) == 6557:
            #     print("test0=====", msg.key.decode('utf-8'))
            if 'summary' in myjson.keys():
                summary = myjson['summary']
                print("summary:", summary, myjson['timestamp'], msg.offset)
            else:
                print("kafka process:", myjson.keys())
            if filter is not None:
                strmsg = msg.value.decode('utf-8')
                if filter in strmsg:
                    self.write_file(strmsg)

            # print(myjson)
        return None

    def write_file(self, msg):
        with open(self.filename, 'w+') as f:
            f.write(json.dumps(json.loads(msg), indent=4))
            f.write("\n")


def getmd5(filename):
    fd = open(filename, "r")
    fcont = fd.read()
    fd.close()
    fmd5 = hashlib.md5(fcont)
    return fmd5.hexdigest()


def working(config):
    global conf_md5
    while True:
        sleep(5)
        conf_ing_md5 = getmd5('para.conf')
        if conf_md5 != conf_ing_md5:
            config.read("para.conf")
            conf_md5 = conf_ing_md5


def get_offset_time_window(consumer, partitions_structs, begin_time, end_time):
    begin_search = {}
    for partition in partitions_structs:
        begin_search[partition] = begin_time if isinstance(begin_time, int) else __str_to_timestamp(begin_time)
    begin_offset = consumer.offsets_for_times(begin_search)
    print("begin timestamp:", begin_search)
    print("begin OffsetAndTimestamp:", begin_offset)
    end_search = {}
    for partition in partitions_structs:
        end_search[partition] = end_time if isinstance(end_time, int) else __str_to_timestamp(end_time)
    end_offset = consumer.offsets_for_times(end_search)

    e_offset = 'null'
    for topic_partition, offset_and_timestamp in begin_offset.items():
        b_offset = 'null' if offset_and_timestamp is None else offset_and_timestamp[0]
        e_offset = 'null' if end_offset[topic_partition] is None else end_offset[topic_partition][0]
        print('Between {0} and {1}, {2} offset range = [{3}, {4}]'.format(begin_time, end_time, topic_partition, b_offset,
                                                                        e_offset))
        if b_offset != 'null':
            print("begin offset:", topic_partition, b_offset)
            consumer.seek(topic_partition, b_offset)
    return consumer, e_offset


def __str_to_timestamp(str_time, format_type='%Y-%m-%d %H:%M:%S'):
    time_array = time.strptime(str_time, format_type)
    return int(time.mktime(time_array)) * 1000


def workline1(self, kp, begin_time=None, end_time=None, filter_str=None):
    try:
        if begin_time is None or end_time is None:
            print("begin time or end time is None, please")
            return None
        # consumer = KafkaConsumer(group_id=config.get("db", "main_group_id"),
        #                          bootstrap_servers=config.get("db", "bootstrap_servers"))
        consumer = KafkaConsumer(group_id="test",
                                 # sasl_plain_username='xes_oa', sasl_plain_password='CnYN88zKd44tV7ng',
                                 # security_protocol='SASL_PLAINTEXT', sasl_mechanism='PLAIN',
                                 bootstrap_servers=broker
                                 )

        tps = []
        for p in consumer.partitions_for_topic(topic):
            tp = TopicPartition(topic, p)
            tps.append(tp)
        print("version:", consumer.config['api_version'], tps)
        consumer.assign(tps)
        try:
            consumer, end_offset = get_offset_time_window(consumer, tps, begin_time, end_time)
        except Exception as e:
            print(e)
            exit(0)


        start_time = end_time = int(time.time())
        while True:
            try:
                value_ans = consumer.poll(max_records=20).values()
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
                                        exit(0)
                                        break
                                except Exception as e:
                                    print("offset:", e)
                                    break
                        else:
                            msg_offset = int(par.offset)
                        # msg_partition = int(par.partition)
                        # msg_topic = str(par.topic)
                        # if (对应分片的截止时间戳的end_offset到达)：
                        # 停止

                        # message_sets += par
                    print("to msg process...")
                    kp.msg_process(message_sets, filter_str)
                # del message_sets[:]
            except Exception as e:
                print(2, ":================", e)
                break

    except Exception as e:
        print(1, ":", e)
        return None


if __name__ == '__main__':
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    filter_str = "openLogicalChannel"
    begin_time = '2020-04-30 10:59:03'
    end_time = '2020-04-30 10:59:05'
    kp = kafkaprocess(filename)
    workline1("", kp, begin_time, end_time, filter_str)
