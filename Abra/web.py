_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
_USER_DIR_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {user_thoughts}
        </table>
    </body>
</html>
'''
_USER_THOUGHT = '''
<tr>
    <td>{date}</td>
    <td>{thought}</td>
</tr>
'''
_NOT_FOUND = '''
<html>
    <body>
        <p> Path Not Found </p>
    </body>
</html>
'''

from http.server import *
import socket
import time
import datetime
import struct
import threading
import os
from _thread import *
import pathlib
from website import Website
DIR_PATH = ""



class ReqHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def index_page(self):
        dirs = []
        #for directory in os.listdir(DIR_PATH):
        for directory in DIR_PATH.iterdir():
            dirs.append(_USER_LINE_HTML.format(user_id=directory.name))
        all_dirs = "\n".join(dirs)
        index = (_INDEX_HTML.format(users = all_dirs)).encode('utf8')
        return index

    def user_page(self):
        req_path = self.path.split("/")

        if len(req_path) != 3:
            return _NOT_FOUND.encode('utf8')
        user_path = pathlib.Path(str(DIR_PATH) + "/" + req_path[2])

        if not user_path.is_dir():
            return _NOT_FOUND.encode('utf8')

        thoughts = []
        for file in user_path.iterdir():
            time_repr = file.stem.split("_")
            time_repr[1] = time_repr[1].replace("-", ":")
            thoughts.append(_USER_THOUGHT.format(date=str(time_repr[0] + " " + time_repr[1]),
                                                 thought=file.read_text()))
        user_html = _USER_DIR_HTML.format(user_id=req_path[2],
                                          user_thoughts=('\n'.join(thoughts))).encode('utf8')
        return user_html


    def do_GET(self):
        self._set_headers()
        if (self.path == '/' or self.path == '/favicon.ico'):
            self.wfile.write(self.index_page())
        else:
            self.wfile.write(self.user_page())

    def do_HEAD(self):
        self._set_headers()


    def do_POST(self):
        self._set_headers()
        self.wfile.write(self._html(""))


def run_webserver(address, data_dir):
    global DIR_PATH
    DIR_PATH = data_dir
    httpd = HTTPServer((address[0], address[1]), ReqHandler)
    httpd.serve_forever()


def ip_port_extract(address):
    i = 0
    while address[i] != ':':
        i += 1
        if i == len(address):
            raise ValueError
    ip = address[:i]
    port = int(address[i+1:])
    return(ip, port)


def main(argv): 
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        address = ip_port_extract(argv[1])
        socket.inet_aton(address[0])
        if not 0 <= address[1] <= 65535:
            print(f'Address {address[1]} illegal')
            raise ValueError
        data_dir = pathlib.Path(argv[2])
        run_webserver(address, data_dir)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
