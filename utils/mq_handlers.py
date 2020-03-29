from functools import partial
import os
import pika

TO_Q = 0
TO_FILE = 1


class RabbitMQHandler:

    def __init__(self, queue_name, exchange_name='', queue_url=None, publish_to=''):
        self.conn = None
        self.channel = None
        self.queue_url = queue_url
        self.exchange = exchange_name
        self.consume_queue = queue_name
        self.msg_num = 0
        if publish_to == '':
            self.publish_queue = self.consume_queue
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
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.publish_queue, body=msg)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.consume_queue, auto_ack=True, on_message_callback=self.callback)
        self.channel.start_consuming()

    #  should be changed by parsers in order to publish the parsed data
    def on_callback(self, msg):
        return msg

    def callback(self, channel, method, properties, body):
        parsed_data = self.on_callback(body)
        self.publish(msg=parsed_data)
