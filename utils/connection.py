import socket


class Connection:

    def __init__(self, sock):
        self.conn = sock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    @classmethod
    def connect(cls, ip_address, port):
        sock = socket.socket()
        sock.connect((ip_address, port))
        return Connection(sock)

    def __repr__(self):
        host = self.conn.getsockname()
        peer = self.conn.getpeername()
        rpr = f'<Connection from {host[0]}:{host[1]!r} to {peer[0]}:{peer[1]!r}>'
        return rpr

    def send(self, data):
        self.conn.sendall(data)

    def receive(self, size):
        data = self.conn.recv(size)
        if len(data) != size:
            raise socket.error(f'Expected {size} bytes, only {len(data)} bytes received')
        return data

    def close(self):
        self.conn.close()
