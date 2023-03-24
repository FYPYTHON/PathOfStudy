# coding=utf-8
from datetime import datetime

from kafka import SimpleClient, KafkaConsumer, KafkaProducer
from kafka.producer import SimpleProducer
import json

def send_kafka():
    client = SimpleClient("127.0.0.1:9092", timeout=2)
    msgs = []
    for i in range(1000):
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


def sendData(id, producer=None):
    # sendBytes()
    msg_dict = {
        "id": "{}".format(id),
        "time": str(datetime.now())
    }
    msg = json.dumps(msg_dict)
    try:

        res = producer.send('zsimple', msg.encode('utf-8'), partition=0)
        # print("res:", res.get(timeout=1))
        # print(res.value)
        producer.flush()
    except Exception as e:
        print(e)


def main():
    producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092", send_buffer_bytes=2 * 1024 * 1024,
                             request_timeout_ms=100, )
    for i in range(20):
        sendData(i, producer)


if __name__ == "__main__":
    # send_kafka()
    main()