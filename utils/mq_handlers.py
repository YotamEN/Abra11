from functools import partial
import os
import pika

TO_Q = 0
TO_FILE = 1


class MQHandler:

    def __init__(self, queue_name, exchange_name='', queue_url=None, publish_to=''):
        self.conn = None
        self.channel = None
        self.queue_url = queue_url
        self.exchange = exchange_name
        self.c_queue = queue_name
        self.msg_num = 0
        if publish_to == '':
            self.p_queue = queue_name
        self.set_mq_conn()

    def set_mq_conn(self):
        if self.queue_url is None:
            self.queue_url = os.environ['AMQP_URL']
        parameters = pika.URLParameters(self.queue_url)
        conn = pika.SelectConnection(parameters)

        self.conn = conn
        self.channel = conn.channel()

    def close(self):
        self.conn.close()

    def publish(self, msg):
        # print(msg)
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.p_queue, body=msg)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.c_queue, auto_ack=True, on_message_callback=self.callback)
        self.channel.start_consuming()

    def callback(self, channel, method, properties, body):
        pass
