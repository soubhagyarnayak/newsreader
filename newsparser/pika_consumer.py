import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

import functools
import pika

from config import QUEUE_CONNECTION_STRING

TASK_PROCESSOR_QUEUE_NAME = 'newsparser'
EXCHANGE_NAME = ''

logger = logging.getLogger(__name__)

"""
Please refer https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py
"""

class PikaConsumer():
    def __init__(self, handler):
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._consuming = False
        self._prefetch_count = 1
        self.handler = handler

    def connect(self):
        logger.info('Creating connection to message queue')
        return pika.SelectConnection(
            parameters=pika.URLParameters(QUEUE_CONNECTION_STRING+'?heartbeat=600'),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def on_connection_open(self, _unused_connection):
        logger.info('Connection opened')
        self.open_channel()

    def open_channel(self):
        logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self,channel):
        logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(EXCHANGE_NAME)

    def add_on_channel_close_callback(self):
        logger.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        logger.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            logger.info('Connection is closing or already closed')
        else:
            logger.info('Closing connection')
            self._connection.close()

    def close_channel(self):
        logger.info('Closing the channel')
        self._channel.close()

    def on_connection_open_error(self, _unused_connection, err):
        logger.error('Connection open failed: %s', err)
        self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def stop(self):
        if not self._closing:
            self._closing = True
            logger.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            logger.info('Stopped')

    def stop_consuming(self):
        if self._channel:
            logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        logger.info('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)
        self.close_channel()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            logger.warning('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def setup_exchange(self, exchange_name):
        logger.info('Declaring exchange: %s', exchange_name)
        if(exchange_name != ''):
            self._channel.exchange_declare(
                exchange=exchange_name,
                exchange_type='direct',
                callback=self.on_exchange_declareok)
        else:
            logger.info('Skipping binding as it is the default exchange')
            self.set_qos()

    def on_exchange_declareok(self, _unused_frame):
        logger.info('Exchange declared')
        self.setup_queue(TASK_PROCESSOR_QUEUE_NAME)

    def setup_queue(self, queue_name):
        logger.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(queue=queue_name, callback=self.on_queue_declareok)

    def on_queue_declareok(self, _unused_frame):
        logger.info('Binding %s to %s with %s', EXCHANGE_NAME, TASK_PROCESSOR_QUEUE_NAME,
                    TASK_PROCESSOR_QUEUE_NAME)
        self._channel.queue_bind(
            TASK_PROCESSOR_QUEUE_NAME,
            EXCHANGE_NAME,
            routing_key=TASK_PROCESSOR_QUEUE_NAME,
            callback=self.on_bindok)

    def on_bindok(self, _unused_frame):
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        logger.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        logger.info('Issuing consumer related RPC commands')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
        self._consumer_tag = self._channel.basic_consume(
            TASK_PROCESSOR_QUEUE_NAME, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        logger.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        self.handler(body)
        self._channel.basic_ack(basic_deliver.delivery_tag)

    def on_consumer_cancelled(self, method_frame):
        logger.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            logger.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            logger.info('Stopped')