import click
from furl import furl
from .reader import MindReader
from utils.mq_handlers import RabbitMQHandler

UNDEFINED = -1
parser_names = ["pose", "c_image", "d_image", "feelings"]


@click.group()
def main():
    pass


class Parser:

    def __init__(self, mq_exchange='', name='', file_path=None, queue_url=None):
        if queue_url is not None:
            self._with_queue = True
            furl_path = furl(queue_url)
            if furl_path.scheme == 'rabbitmq':
                self.mq_handler = RabbitMQHandler(queue_name=name, exchange_name=mq_exchange, queue_url=queue_url)
            self.mq_handler.on_callback = self.parse
        else:
            self._with_queue = False
            # self.publish = self.write_to_file
            self._file = open(file_path, "w+")
        # self.data = None
        self.name = name

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file is not None:
            self._file.close()

    def write_to_file(self, msg):
        self._file.write(msg)

    # each parser must implement this function
    # 'msg' input is of type "bytes"
    # output muse be type "bytes" as well
    def parse(self, msg):
        pass


class PoseParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Pose", queue_url=queue_url)
        self.translation = None
        self.rotation = None

    def parse(self, msg):
        pass


class CImageParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Color Image", queue_url=queue_url)
        self.c_image_path = None

    def parse(self, msg):
        pass


class DImageParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Depth Image", queue_url=queue_url)
        self.d_image_path = None

    def parse(self, msg):
        pass


class FeelingsParser(Parser):

    def __init__(self, mq_exchange='', queue_url=None):
        super().__init__(mq_exchange=mq_exchange, name="Feelings", queue_url=queue_url)
        self.hunger = UNDEFINED
        self.thirst = UNDEFINED
        self.exhaustion = UNDEFINED
        self.happiness = UNDEFINED

    def parse(self, msg):
        pass


@main.command()
@click.argument('parser', help="Name of requested parser")
@click.argument('data_path', help="Path to data for parsing")
@click.argument('publish_to', help="URL of your Message Queue or File")
def parse(parser: str, data_path: str, publish_to=None):
    parser_class = get_parser_type(parser)
    parser_h = parser_class(name=parser)


@main.command()
@click.argument('parser', help="Name of requested parser")
@click.argument('mq_url', help="URL of your Message Queue")
def run_parser(parser: str, mq_url: str):
    parser_class = get_parser_type(parser)
    parser_h = parser_class(name=parser, queue_url=mq_url)
    parser_h.mq_handler.start_consuming()


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
