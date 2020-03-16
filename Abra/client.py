import click
import socket
import struct
import time
import http.client


@click.group()
def main():
    pass


@main.command()
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('path')
def upload_sample(address, user, thought):
    try:
        # create socket
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(ip_port_extract(address))
        # encode data by given protocol
        thought_size = len(thought)
        curr_time = int(time.time())
        data_packet = struct.pack(f'<QQi{thought_size}s', int(user), curr_time, thought_size, thought.encode())
        conn.sendall(data_packet)
        print('done')
    except Exception as e:
        print(f'Error: {e!r}')
    

def ip_port_extract(address):
    i = 0
    while address[i] != ':':
        i += 1
    ip = address[:i]
    port = int(address[i+1:])
    return ip, port


if __name__ == '__main__':
    pass
