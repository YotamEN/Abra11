from .errors import UnsupportedMessageQueueError
from furl import furl
import pika

TO_Q = 0
TO_FILE = 1

SUPPORTED_MQS = ["RabbitMQ"]
SAVER_NAME = "saver"
# RabbitMQ Constants:
RB_EXCHANGE_TYPE = 'fanout'
RB_EXCHANGE_NAME = 'parsers'


class MQHandler:

    def __init__(self, q_path):
        f_url = furl(q_path)
        # choose mq scheme:
        if f_url.scheme == "rabbitmq":
            self.mq = RabbitMQHandler(q_path)
        else:
            raise UnsupportedMessageQueueError(f'ERROR: only supported message queues are: {SUPPORTED_MQS!r}')

        self.declare_parser_queue = self.mq.declare_parser_queue
        self.publish_to_parsers = self.mq.publish_to_parsers
        
        self.declare_saver_queue = self.mq.declare_saver_queue
        self.publish_to_saver_queue = self.mq.publish_to_saver_queue
        self.consume_saver_queue = self.mq.consume_saver_queue
        
        self.close = self.mq.close
        self.consume_queue = self.mq.consume_queue


class RabbitMQHandler:

    def __init__(self, q_path):

        self.q_f_url = furl(q_path)
        self.parameters = pika.ConnectionParameters(host=self.q_f_url.host, port=self.q_f_url.port)
        self.conn = pika.BlockingConnection(self.parameters)
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange=RB_EXCHANGE_NAME, exchange_type=RB_EXCHANGE_TYPE)

    def close(self):
        self.conn.close()

    def consume_queue(self, queue, callback):
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    # *****************************************************
    # ************* methods on parser queues  *************
    # *****************************************************
    def declare_parser_queue(self, queue):
        result = self.channel.queue_declare(queue=queue, exclusive=True)
        self.channel.queue_bind(exchange=RB_EXCHANGE_NAME, queue=result.method.queue)

    def publish_to_parsers(self, msg):
        self.channel.exchange_declare(exchange=RB_EXCHANGE_NAME, exchange_type='fanout')
        self.channel.basic_publish(exchange=RB_EXCHANGE_NAME, routing_key='', body=msg)

    # *********************************************
    # ************* methods on saver  *************
    # *********************************************
    def declare_saver_queue(self):
        self.channel.queue_declare(queue=SAVER_NAME, exclusive=True)

    def publish_to_saver_queue(self, msg):
        self.channel.queue_declare(SAVER_NAME)
        self.channel.basic_publish(exchange="", routing_key=SAVER_NAME, body=msg)

    def consume_saver_queue(self, callback):
        self.consume_queue(SAVER_NAME, callback)

