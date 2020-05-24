from abra.abra_pb2 import User
from abra.client import upload_sample, read_snapshot
from abra.common import *
from flask import Flask
import random
import string


def create_user():
    user = User()
    user.user_id = random.randint(1, 2**32)
    length = random.randint(1, 25)
    letters = string.ascii_lowercase
    user.username = ''.join(random.choice(letters) for i in range(length))
    user.birthday = user.user_id = random.randint(1, 2**32)
    user.gender = random.randint(0, 2)
    return user


def test_upload_sample(tmp_path, requests_mock):
    f = tmp_path / "snap.mind"
    user = create_user()
    f.write_bytes(user)
    host, port = APP_SERVER_HOST, APP_SERVER_PORT
    upload_sample(host=host, port=port, path=tmp_path)
    requests_mock.get()
