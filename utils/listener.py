from .connection import Connection
import socket
import threading
from _thread import *


class Listener:

    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.server = None

    def __enter__(self):
        self.server = socket.socket()
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (self.host, self.port)
        self.server.bind(address)
        self.server.listen(self.backlog)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()

    def __repr__(self):
        rpr = f'Listener(port={self.port}, host={self.host!r},' \
              f' backlog={self.backlog}, reuseaddr={self.reuseaddr})'
        return rpr

    def accept(self):
        client, add = self.server.accept()
        return Connection(client)

