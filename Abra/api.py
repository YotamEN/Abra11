import click
from .common import *
from datetime import datetime
from .db.dbhandlers import DBHandler
from utils.errors import UnsupportedTopic
from flask import Flask, request, jsonify
import json
from termcolor import cprint

app = Flask(__name__)
_db_h = None


@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default=LOCAL_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
@click.option("--database", "-d", default=DATABASE_DEFAULT_URL)
def run_server(host, port, database):
    run_api_server(host, port, database)


def run_api_server(host=LOCAL_HOST, port=API_SERVER_PORT, database_url=DATABASE_DEFAULT_URL):
    global _db_h
    _db_h = DBHandler(database_url)

    app.run(host, port)

    cprint('Created your api Server!', 'white', 'on_blue', attrs=['bold'])
    cprint(f'host: {host}\nport: {port}', 'red')


@app.route('/users', methods=['GET'])
def get_all_users():
    users = _db_h.get_all_users()
    return jsonify([json.dumps({USERNAME_KEY: user.name, USER_ID_KEY: user.id}) for user in users])


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = _db_h.get_user(user_id)
    return jsonify({USER_ID_KEY: user.id, USERNAME_KEY: user.name, BIRTHDAY_KEY: user.birthday,
                    GENDER_KEY: user.gender})


@app.route('/users/<user_id>/snapshots', methods=['GET'])
def get_user_snapshots(user_id):  # TODO
    snapshots = _db_h.get_user_snapshots(user_id)
    l = []
    for snap in snapshots:
        l.append({SNAPSHOT_ID_KEY: create_snapshot_id(user_id, datetime), DATETIME_KEY: snap.datetime})
    return jsonify(l)


@app.route('/users/<user_id>/snapshots/<snapshot_id>', methods=['GET'])
def get_snapshot(user_id, snapshot_id):
    date = snapshot_id
    snap_data = _db_h.get_snapshot(user_id, date)
    avail_res = []
    if snap_data.pose is not None:
        avail_res.append("pose")
    if snap_data.color_image is not None:
        avail_res.append("color-image")
    if snap_data.depth_image is not None:
        avail_res.append("depth-image")
    if snap_data.feelings is not None:
        avail_res.append("feelings")
    return jsonify({USER_ID_KEY: user_id, DATETIME_KEY: date, AVAILABLE_RESULTS_KEY: avail_res})


""" *** 'get_snapshot_result' assumes the user made sure the result is indeed available! *** """
@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>', methods=['GET'])
def get_snapshot_result(user_id, snapshot_id, result_name):
    date = snapshot_id
    snap_info_data = _db_h.get_snapshot_result(user_id, date, result_name)
    if result_name == "pose":
        res = {TRANS_X_KEY: snap_info_data.translation.x,
               TRANS_Y_KEY: snap_info_data.translation.y,
               TRANS_Z_KEY:  snap_info_data.translation.z,
               ROT_X_KEY: snap_info_data.rotation.x,
               ROT_Y_KEY: snap_info_data.rotation.y,
               ROT_Z_KEY: snap_info_data.rotation.z}
    elif result_name == "color-image":
        res = {WIDTH_KEY: snap_info_data.width,
               HEIGHT_KEY: snap_info_data.height,
               C_IMG_DATA_DIR: snap_info_data.data_path}
    elif result_name == "depth-image":
        res = {WIDTH_KEY: snap_info_data.width,
               HEIGHT_KEY: snap_info_data.height,
               D_IMG_DATA_DIR: snap_info_data.data_path}
    elif result_name == "feelings":
        res = {HUNGER_KEY: snap_info_data.hunger,
               THIRST_KEY: snap_info_data.thirst,
               EXHAUSTION_KEY: snap_info_data.exhaustion,
               HAPPINESS_KEY: snap_info_data.happiness}
    else:
        raise UnsupportedTopic(f"ERROR: '{result_name}' is unknown. Use only one of: {TOPICS!r}")
    return jsonify(res)


if __name__ == '__main__':
    main()

