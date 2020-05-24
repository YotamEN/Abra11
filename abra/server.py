from abra.abra_pb2 import User, SnapshotWrapper
import click
from abra.common import *
from flask import Flask, request
import json
import os
import random
from termcolor import cprint
from pathlib import Path
from abra.mq.mq_handlers import RabbitMQHandler

DEBUG = 0
_WORK_DIR = "state_of_minds"
app = Flask(__name__)
_publish = None
dbg_num = 0

# FIXME add errors everywhere
@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default=APP_SERVER_HOST)
@click.option("--port", "-p", default=APP_SERVER_PORT)
@click.argument('publish')
def run_server_cli(host, port, publish):
    run_server(host, port, publish)


def run_server(host=APP_SERVER_HOST, port=APP_SERVER_PORT, publish=None):
    global _publish
    _publish = publish

    cprint('Creating your Server!', 'white', 'on_blue', attrs=['bold'])
    app.run(host, port)
        

@app.route('/msg', methods=['POST'])
def new_msg():
    snapshot_wrapper = SnapshotWrapper()
    msg = request.data
    snapshot_wrapper.ParseFromString(msg)
    user, snapshot, msg_num = snapshot_wrapper.user, snapshot_wrapper.snapshot, snapshot_wrapper.msg_num
    unique_path = Path(VOLUME_PATH) / f'{_WORK_DIR}/{user.user_id}_{msg_num}_{random.random()}'
    f_path = save_snapshot(snapshot, unique_path)
    while f_path is None:
        unique_path = Path(VOLUME_PATH) / f'{_WORK_DIR}/{user.user_id}_{msg_num}_{random.random()}'
        f_path = save_snapshot(snapshot, unique_path)

    snap_path_json = json.dumps({
        USER_ID_KEY: user.user_id,
        USERNAME_KEY: user.username,
        USER_SNAPSHOTS_URL_KEY: f_path,
        SNAPSHOT_ID_KEY: create_snapshot_id(user, snapshot.datetime)
    })

    if callable(_publish):
        _publish(snap_path_json)
        return

    publish_msg(snap_path_json)
    return snap_path_json


@app.route('/user', methods=['POST'])
def register_new_user():
    user = User()
    user_data = request.data
    user.ParseFromString(user_data)

    if callable(_publish):
        _publish(user)
        return

    json_user = jsonify_user(user)
    publish_user(json_user)
    return json_user


def publish_msg(msg):
    mq_handler = RabbitMQHandler(_publish)
    mq_handler.publish_to_parsers(msg)


def publish_user(user):
    print(user)
    mq_handler = RabbitMQHandler(_publish)
    mq_handler.publish_to_parsed_data_exchange(msg=user, topic="user")


def save_snapshot(snapshot, path):
    if os.path.isdir(path):
        return None
    try:
        path = Path(path)
        Path(path).mkdir(parents=True, exist_ok=True)
        f = path / SNAPSHOT_JSON_FILE_NAME
        f.write_bytes(snapshot.SerializeToString())
        return str(f.absolute())
    except OSError as err:
        print(f"Error: {err}")
        return None
    except ValueError as err:
        print(f"Error: {err}")
        return None


def jsonify_user(user):
    json_user = {
        TOPIC_KEY: USER_TOPIC,
        USER_ID_KEY: user.user_id,
        USERNAME_KEY: user.username,
        BIRTHDAY_KEY: user.birthday,
        GENDER_KEY: user.gender
    }
    return json.dumps(json_user)


def create_snapshot_id(user_id, date):
    st = str(user_id)+str(date)
    hashed = int(hash(st)) + random.randint(1, 1e+18)
    return abs(hashed & 0xffffffff)


if __name__ == '__main__':
    main()
