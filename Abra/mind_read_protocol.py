import requests
from requests.exceptions import HTTPError

ERROR_OCCURRED = -1
SUCCESS = 0


class ProtocolHandler:

    def __init__(self, host='localhost', port=8000, path=''):
        self.host = host
        self.port = port
        self.path = path
        self.num_msg = -1

    def post(self, data):
        tag = "user" if self.num_msg < 0 else "new_msg"
        try:
            response = requests.post(f'http://{self.host}:{self.port}/{tag}',
                                     headers={'Content-Type': 'application/protobuf'}, data=data)
            response.raise_for_status()
            return SUCCESS
        except HTTPError as err:
            print(f'HTTP error occurred: {err}')
            return ERROR_OCCURRED

    def get(self):
        try:
            response = requests.get(f'http://{self.host}:{self.port}/new_msg')
            if response.status_code != 200:
                raise HTTPError
            return response.text
        except HTTPError as err:
            print(f'HTTP error occurred: {err}')
            return ERROR_OCCURRED
