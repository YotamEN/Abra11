import click
from .reader import MindReader
from .mind_read_protocol import ProtocolHandler


@click.group()
def main():
    pass


@main.command()
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('path')
def upload_sample(host, port, path):
    # TODO add context manager for errors
    reader = MindReader(path)
    protocol_h = ProtocolHandler(host=host, port=port, path=path)
    protocol_h.post(reader.user.SerializeToString())
    while not reader.done:
        message = next(reader)
        ret = protocol_h.post(message.SerializeToString())
        if ret != 0:
            print("Error Occurred!")  # FIXME ERRORs


if __name__ == '__main__':
    main()
