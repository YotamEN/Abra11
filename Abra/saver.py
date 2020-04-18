import click
from furl import furl
from utils.db.dbhandlers import DBHandler


@click.group()
def main():
    pass


class Saver:

    def __init__(self, db_url):
        self.db_handler = DBHandler(db_url)

    def register_to_topic(self, topic):
        pass

    def save(self, topic, data):
        pass


@main.command("save")
@click.option("--database", "-d")
@click.argument('topic', help="Topic name")
def save_cli(self, db_url, topic, data):
    furl_url = furl(db_url)
    if furl_url.scheme == 'postgresql':
        pass


@main.command("run-saver")
@click.option("--database", "-d")
@click.argument('topic', help="Topic name")
def run_saver(db_url, mq_url):
    furl_url = furl(db_url)
    if furl_url.scheme == 'postgresql':
        pass
    if furl_url.scheme == 'rabbitmq':
        pass
