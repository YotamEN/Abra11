import click
from furl import furl
from utils.mq_handlers import MQHandler


@click.group()
def main():
    pass


class Saver:

    def __init__(self, db_url):
        self.database_url = db_url
        furl_url = furl(db_url)
        if furl_url.scheme == 'postgresql':
            pass
        self.queue_handlers = []

    def register_to_topic(self, topic):
        pass

    def save(self, topic, data):
        pass


@main.command()
@click.option("--database", "-d")
@click.argument('topic', help="Topic name")
def save(self, db_url, topic, data):
    furl_url = furl(db_url)
    if furl_url.scheme == 'postgresql':
        pass


@main.command()
@click.option("--database", "-d")
@click.argument('topic', help="Topic name")
def run_saver(db_url, mq_url):
    furl_url = furl(db_url)
    if furl_url.scheme == 'postgresql':
        pass
    if furl_url.scheme == 'rabbitmq':
        pass
