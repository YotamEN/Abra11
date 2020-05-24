from .common import FAIL, SUCCESS, APP_SERVER_HOST, APP_SERVER_PORT
import requests
from requests.exceptions import HTTPError


class ProtocolHandler:

    def __init__(self, host=APP_SERVER_HOST, port=APP_SERVER_PORT, path=''):
        self.host = host
        self.port = port
        self.path = path
        self.num_msg = -1

    def post(self, data):
        tag = "user" if self.num_msg < 0 else "msg"
        try:
            response = requests.post(f'http://{self.host}:{self.port}/{tag}',
                                     headers={'Content-Type': 'application/protobuf'}, data=data)
            response.raise_for_status()
            self.num_msg += 1
            return SUCCESS
        except HTTPError as err:
            print(err)
            return FAIL

    def get(self):
        try:
            response = requests.get(f'http://{self.host}:{self.port}/new_msg')
            if response.status_code != 200:
                raise HTTPError
            return response.text
        except HTTPError as err:
            print(f'HTTP error occurred: {err}')
            return FAIL

