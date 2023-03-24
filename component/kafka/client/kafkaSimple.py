# coding=utf-8
import multiprocessing
from threading import Thread
import os
import time
from kafka import SimpleClient, KafkaConsumer, TopicPartition
from kafka.producer import SimpleProducer


def send_kafka():
    client = SimpleClient("127.0.0.1:9092", timeout=2)
    msgs = []
    for i in range(100):
        msg = str(i).encode('utf-8')
        msgs.append(msg)
    producer = SimpleProducer(client, async=False)
    # msgs = [b'{"a:2","timestamp":1}', b'3', b'4', b'5']
    a = producer.send_messages("zsimple", *msgs)


def send_kafka_msgs(msgs):
    client = SimpleClient("127.0.0.1:9092", timeout=2)
    producer = SimpleProducer(client, async=False)
    # msgs = [b'{"a:2","timestamp":1}', b'3', b'4', b'5']
    a = producer.send_messages("test2", *msgs)
    print(msgs)
    print(a)


def consumer_kafka(id):
    # client = SimpleClient("127.0.0.1:9092", timeout=2)
    consumser = KafkaConsumer('zsimple', bootstrap_servers="127.0.0.1:9092", auto_offset_reset="earliest", group_id="test")
    msgs = []
    count = 0
    for msg in consumser:
        # msgs.append(msg.value)
        send_kafka_msgs([msg.value])
        count += 1
        print(id, count)
        # if len(msgs) > 50:
        #     send_kafka_msgs(msgs)
        #     msgs = []

# class KConsumer(Thread):
class KConsumer(multiprocessing.Process):
    """
    group_id (str or None): The name of the consumer group to join for dynamic
            partition assignment (if enabled), and to use for fetching and
            committing offsets. If None, auto-partition assignment (via
            group coordinator) and offset commits are disabled.
            Default: None
    auto_offset_reset (str): A policy for resetting offsets on
            OffsetOutOfRange errors: 'earliest' will move to the oldest
            available message, 'latest' will move to the most recent. Any
            other value will raise the exception. Default: 'latest'.
    """
    _TOPIC = "ods.h323"
    _BROKES = "127.0.0.1:9092"
    _GROUP_ID = "simple1"
    _OFFSET_SET = "earliest"

    def __init__(self, name=None):
        print("KConsumer start", name)
        multiprocessing.Process.__init__(self)
        # Thread.__init__(self)
        self.stop_event = multiprocessing.Event()
        self._name = name

    def stop(self):
        self.stop_event.set()
        print("KConsumer stop")

        # @property
        # def name(self, name):
        # 	self._name = name

    def process_message(self, msg):
        if msg.timestamp == -1:
            time_stamp = 1588223483 * 1000
        else:
            time_stamp = msg.timestamp
        # print(time_stamp)
        time_array = time.localtime(time_stamp * 1.0 / 1000)
        str_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        name_time = time.strftime("%Y_%m_%d_%H_%M_%S", time_array)
        # print(os.getppid(), str_time, msg.topic, msg.value)
        # print(self._name)
        if len(msg.value) < 50:
            print("%s-%s:%d:%d: %s key=%s value=%s" % (self._name, msg.topic, msg.partition, msg.offset, str_time,
                                                       msg.key, msg.value))
        else:
            print("%s-%s:%d:%d: %s key=%s value=%s" % (self._name, msg.topic, msg.partition, msg.offset, str_time,
                                                       msg.key, msg.value[0:50]))

    def run(self):
        # , auto_offset_reset='earliest' , auto_offset_reset='latest'
        consumer = KafkaConsumer(bootstrap_servers=self._BROKES
                                , auto_offset_reset=self._OFFSET_SET
                                , group_id=self._GROUP_ID
                                # , enable_auto_commit=False
                                , consumer_timeout_ms=1000)
        # consumer.subscribe([self._TOPIC])
        tps = []
        for p in consumer.partitions_for_topic(self._TOPIC):
            tp = TopicPartition(self._TOPIC, p)
            tps.append(tp)
        print("version:", consumer.config['api_version'], tps)
        consumer.assign(tps)

        while not self.stop_event.is_set():
            while True:
                value_ans = consumer.poll(max_records=500).values()
                # print(len(value_ans), self._name)
                for message in value_ans:
                    for msg in message:
                    # print(message)
                    # for message in consumer:
                        self.process_message(msg)
                if self.stop_event.is_set():
                    break
            # for message in value_ans:
            # for message in consumer:
            #     self.process_message(message)
            #     if self.stop_event.is_set():
            #         break
        consumer.close()

if __name__ == "__main__":
    # send_kafka()
    # consumer_kafka(1)
    # consumer_kafka(2)
    tasks = [KConsumer("k1"), KConsumer("k2"), KConsumer("k3"), KConsumer("k4")]
    for wk in tasks:
        wk.start()
