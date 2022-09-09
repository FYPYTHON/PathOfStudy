from __future__ import absolute_import

__title__ = 'kafka'
from .version import __version__
__author__ = 'Dana Powers'
__license__ = 'Apache License 2.0'
__copyright__ = 'Copyright 2016 Dana Powers, David Arthur, and Contributors'

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


from kafkao.consumer import KafkaConsumer
from kafkao.consumer.subscription_state import ConsumerRebalanceListener
from kafkao.producer import KafkaProducer
from kafkao.conn import BrokerConnection
from kafkao.protocol import (
    create_message, create_gzip_message, create_snappy_message)
from kafkao.partitioner import RoundRobinPartitioner, HashedPartitioner, Murmur2Partitioner
from kafkao.structs import TopicPartition, OffsetAndMetadata
from kafkao.serializer import Serializer, Deserializer

# To be deprecated when KafkaProducer interface is released
from kafkao.client import SimpleClient
from kafkao.producer import SimpleProducer, KeyedProducer

# deprecated in favor of KafkaConsumer
from kafkao.consumer import SimpleConsumer, MultiProcessConsumer


import warnings
class KafkaClient(SimpleClient):
    def __init__(self, *args, **kwargs):
        warnings.warn('The legacy KafkaClient interface has been moved to'
                      ' kafkao.SimpleClient - this import will break in a'
                      ' future release', DeprecationWarning)
        super(KafkaClient, self).__init__(*args, **kwargs)


__all__ = [
    'KafkaConsumer', 'KafkaProducer', 'KafkaClient', 'BrokerConnection',
    'SimpleClient', 'SimpleProducer', 'KeyedProducer',
    'RoundRobinPartitioner', 'HashedPartitioner',
    'create_message', 'create_gzip_message', 'create_snappy_message',
    'SimpleConsumer', 'MultiProcessConsumer',
]
