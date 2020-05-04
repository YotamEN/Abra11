from utils.errors import UnsupportedMessageQueueError
from furl import furl
import pika

TO_Q = 0
TO_FILE = 1

SUPPORTED_MQS = ["RabbitMQ"]
PARSED_DATA_EXCHANGE_NAME = "parsed_data"
# RabbitMQ Constants:
RB_EXCHANGE_TYPE = 'fanout'
RB_EXCHANGE_NAME = 'parsers'



class MQHandler:

    def __init__(self, q_path):
        f_url = furl(q_path)
        # choose mq_h scheme:
        if f_url.scheme == "rabbitmq":
            self.mq = RabbitMQHandler(q_path)
        else:
            raise UnsupportedMessageQueueError(f'ERROR: only supported message queues are: {SUPPORTED_MQS!r}')
        # FIXME do this differently:
        self.__dict__ = self.mq.__dict__


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
    def declare_parsed_data_exchange(self):
        self.channel.exchange_declare(exchange=PARSED_DATA_EXCHANGE_NAME, excange_type="topic")

    def publish_to_parsed_data_exchange(self, msg, topic):
        self.channel.basic_publish(exchange=PARSED_DATA_EXCHANGE_NAME, routing_key=topic, body=msg)

    def consume_parsed_data_exchange_by_topic(self, callback, topic):
        self.declare_parsed_data_exchange()
        res = self.channel.queue_declare('', exclusive=True)
        self.channel.queue_bind(exchange=PARSED_DATA_EXCHANGE_NAME, queue=res.method.queue, routing_key=topic)
        self.channel.basic_consume(queue=res.method.queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

