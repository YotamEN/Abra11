from .abra_pb2 import User, Snapshot, SnapshotWrapper, SnapshotPathWrapper
import click
from .common import *
from flask import Flask, request
import json
import os
import random
from termcolor import cprint
from utils.mq_handlers import MQHandler


_WORK_DIR = "/state_of_minds"
SUCCESS = 0
FAIL = 1
app = Flask(__name__)
_publish = None


#FIXME add errors everywhere
@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('publish', help="URL to message queue")
def run_server(host, port, publish=None):
    global _publish
    _publish = publish

    app.run(host, port)

    cprint('Created your Server!', 'white', 'on_blue', attrs=['bold'])
    cprint(f'host: {host}\nport: {port}', 'red')
        

@app.route('/msg', methods=['POST'])
def new_msg():
    snapshot_wrapper = Snapshot()
    msg = request.data
    snapshot_wrapper.ParseFromString(msg)

    user, snapshot, msg_num = snapshot_wrapper.user, snapshot_wrapper.snapshot, snapshot_wrapper.msg_num
    unique_path = f'{user.id}_{msg_num}_{random.random()}'
    while save_snapshot(snapshot, unique_path):
        unique_path = f'{user.id}_{msg_num}_{random.random()}'

    snapshot_path_wrapper = SnapshotPathWrapper()
    snapshot_path_wrapper.path = unique_path
    snapshot_path_wrapper.user = user
    if callable(_publish):
        _publish(snapshot_path_wrapper)
        return

    publish_msg(snapshot_path_wrapper)


@app.route('/user', methods=['POST'])
def register_new_user():
    user_data = request.data
    user = User.ParseFromString(user_data)

    if callable(_publish):
        _publish(user)
        return

    json_user = jsonify_user(user)
    publish_user(json_user)


def publish_msg(msg):
    mq_handler = MQHandler(_publish)
    mq_handler.publish_to_parsers(msg)


def publish_user(user):
    mq_handler = MQHandler(_publish)
    mq_handler.publish_to_saver_queue(user)


def save_snapshot(snapshot: Snapshot, path: str):
    if os.path.isdir(path):
        return FAIL
    try:
        with open(path, "wb") as f:
            f.write(snapshot.SerializeToString())
    except OSError:
        return FAIL
    except ValueError:
        return FAIL
    return SUCCESS


def jsonify_user(user):
    json_user = {
        USER_ID_KEY: user.user_id,
        USERNAME_KEY: user.username,
        BIRTHDAY_KEY: user.birthday,
        GENDER_KEY: user.gender
    }
    return json.dumps(json_user)


if __name__ == '__main__':
    main()

