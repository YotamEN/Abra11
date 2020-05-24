from abra.common import *
from .app import run_server
import click


@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default=GUI_SERVER_HOST)
@click.option("--port", "-p", default=GUI_SERVER_PORT)
@click.option("--api-host", "-H", default=API_SERVER_HOST)
@click.option("--api-port", "-P", default=API_SERVER_PORT)
def run_cli_server(host, port, api_host, api_port):
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    main()


