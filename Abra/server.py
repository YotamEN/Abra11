import click
from flask import Flask, escape, request
import threading
from termcolor import cprint
import pathlib


lock = threading.Lock()
app = Flask(__name__)
_publish = None

#FIXME add errors everywhere
@click.group()
def main():
    pass


@main.command()
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('publish', help="URL to message queue")
def run_server(host, port, publish=None):
    global _publish
    if publish is None:
        publish = publish_data
    _publish = publish

    app.run(host, port)

    cprint('Created your Server!', 'white', 'on_blue', attrs=['bold'])
    cprint(f'host: {host}\nport: {port}', 'red')
        

@app.route('/new_msg', methods=['POST'])
def publish_data():
    pass


if __name__ == '__main__':
    main()

