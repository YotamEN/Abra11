import click
from .saver import Saver



@click.group()
def main():
    pass


@main.command("save")
@click.option("--database", "-d")
@click.argument('topic')
def save_cli(db_url, topic, data):
    saver = Saver(db_url)
    saver.save(topic=topic, data=data)


@main.command("run-saver")
@click.option("--database", "-d")
@click.argument('topic')
def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    saver.register_to_all_topics(mq_url)