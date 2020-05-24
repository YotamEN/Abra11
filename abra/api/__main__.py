from abra.common import *
from .api import run_api_server
import click


@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default=API_SERVER_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
@click.option("--database", "-d", default=DATABASE_DEFAULT_URL)
def run_server(host, port, database):
    run_api_server(host, port, database)


if __name__ == '__main__':
    main()
