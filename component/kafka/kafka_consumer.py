# coding=utf-8


def init1():
    from kafka import KafkaConsumer
    consumer = KafkaConsumer('my_favorite_topic')
    # consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group')
    for msg in consumer:
        print(msg)


def assign_partition():
    from kafka import TopicPartition
    consumer = KafkaConsumer(bootstrap_servers='localhost:1234')
    consumer.assign([TopicPartition('foobar', 2)])
    msg = next(consumer)


def deserialize_msg():
    consumer = KafkaConsumer(value_deserializer=msgpack.loads)
    consumer.subscribe(['msgpackfoo'])
    for msg in consumer:
        assert isinstance(msg.value, dict)

    # Access record headers. The returned value is a list of tuples
    # with str, bytes for key and value
    for msg in consumer:
        print(msg.headers)

    # Get consumer metrics
    metrics = consumer.metrics()


