import socket
import time
import datetime
import struct
import threading
import os
from _thread import *
import pathlib
import click


lock = threading.Lock()


def write_data(date_repr, user_id, thought, data_dir):
    path = pathlib.Path(data_dir)
    dir_p = path / str(user_id)
    fn = date_repr + '.txt'
    if not dir_p.is_dir():
        dir_p.mkdir(parents=True)
    try:
        file_p  = dir_p / fn
        file_exists = file_p.exists()
        with open(file_p, 'a') as file:
            if file_exists: thought = '\n' + thought
            file.write(thought)
    finally:
        lock.release()


@click.command()
def run(address, data):
    try:
        address = ip_port_extract(address)
        if not 0 <= address[1] <= 65535:
            print(f'Address {address[1]} illegal')
            raise ValueError
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(100)
        if not os.path.exists(data):
            os.makedirs(data)
        while True:
            client, add = server.accept()
            start_new_thread(threaded, (client, add, data))
    except Exception as e:
        print(f'ERROR: {e!r}')
        return 1
        
    
def threaded(client, address, data_dir):
    #recieve data
    lock.acquire()
    data = bytes()
    while True:
        rec = client.recv(1024)
        if not rec:
            break
        data += rec
    #decode data
    data = struct.unpack(f'<qqi{len(data)-20}s', data)
    user_id = data[0]
    timestamp = data[1]
    thought_size = data[2]
    thought = data[3].decode('utf-8')
    date_repr = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
    write_data(date_repr, user_id, thought, data_dir)
    client.close()


    
def ip_port_extract(address):
    i = 0
    while address[i] != ':':
        i += 1
        if i == len(address):
            raise ValueError
    ip = address[:i]
    port = int(address[i+1:])
    return(ip, port)
    

if __name__ == '__main__':
    run()

