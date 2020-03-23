import click
from utils.mq_handlers import MQHandler

UNDEFINED = -1
parser_names = ["pose", "c_image", "d_image", "feelings"]


@click.group()
def main():
    pass


class Parser(MQHandler):

    def __init__(self, mq_exchange='', name='', file_path=None, queue_url=None):
        super().__init__(name, mq_exchange, queue_url, publish_to=f'{"saver" if file_path is None else file_path}')
        self.data = None
        self.name = name
        self.channel.queue_declare(queue=self.name)
        if file_path is not None:
            self.publish = self.write_to_file
        # begin listening on queue
        self.start_consuming()

    def write_to_file(self, msg):
        pass


class PoseParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Pose", queue_url=queue_url)
        self.translation = None
        self.rotation = None

    def callback(self, channel, method, properties, body):
        pass


class CImageParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Color Image", queue_url=queue_url)
        self.c_image_path = None

    def callback(self, channel, method, properties, body):
        pass


class DImageParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Depth Image", queue_url=queue_url)
        self.d_image_path = None

    def callback(self, channel, method, properties, body):
        pass


class FeelingsParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Feelings", queue_url=queue_url)
        self.hunger = UNDEFINED
        self.thirst = UNDEFINED
        self.exhaustion = UNDEFINED
        self.happiness = UNDEFINED

    def callback(self, channel, method, properties, body):
        pass


@main.command()
@click.argument('parser', help="Name of requested parser")
@click.argument('data_path', help="Path to data for parsing")
@click.argument('publish_to', help="URL of your Message Queue or File")
def parse(parser: str, data_path: str, publish_to=None):
    pass


@main.command()
@click.argument('parser', help="Name of requested parser")
@click.argument('mq_url', help="URL of your Message Queue")
def run_parser(parser: str, mq_url: str):
    pass


def get_parser_type(string: str):
    if string.lower() == "pose":
        return PoseParser
    elif string.lower() == "color image" or string.lower() == "c_image" or string.lower() == "color_image":
        return CImageParser
    elif string.lower() == "depth image" or string.lower() == "d_image" or string.lower() == "depth_image":
        return DImageParser
    elif string.lower() == "feelings":
        return FeelingsParser
    else:
        print(f"Unknown parser! please choose one of the following:\n{parser_names!r}")
        return None
