from abra.common import *
from abra.db.dbhandlers import PostgresDBHandler
from abra.errors import UnsupportedTopic
from flask import Flask, jsonify
import json
from termcolor import cprint

app = Flask(__name__)
_db_h = None


def run_api_server(host=LOCAL_HOST, port=API_SERVER_PORT, database_url=DATABASE_DEFAULT_URL):
    global _db_h
    _db_h = PostgresDBHandler(database_url)

    cprint('Creating your api Server!', 'white', 'on_blue', attrs=['bold'])
    cprint(f'host: {host}\nport: {port}', 'red')
    app.run(host, port)


@app.route('/users', methods=['GET'])
def get_all_users():
    users = _db_h.get_all_users()
    print(users)
    return jsonify([json.dumps({USERNAME_KEY: user.name, USER_ID_KEY: user.id}) for user in users])


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = _db_h.get_user(user_id)
    print(f"API user: {user}")
    return jsonify({USER_ID_KEY: user.id, USERNAME_KEY: user.name, BIRTHDAY_KEY: user.birthday,
                    GENDER_KEY: user.gender})


@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_user_snapshots(user_id):
    print(f"API yo yo yo!!")
    snapshots = _db_h.get_user_snapshots(user_id)
    print(f"API snapshots: {snapshots}")
    l = []
    for snap in snapshots:
        l.append({SNAPSHOT_ID_KEY: snap.id, DATETIME_KEY: snap.datetime})
    return jsonify(l)


@app.route('/users/<user_id>/snapshots/<snapshot_id>', methods=['GET'])
def get_snapshot(user_id, snapshot_id):
    snap_data = _db_h.get_snapshot(snapshot_id)
    avail_res = _db_h.available_res(snapshot_id)
    return jsonify({USER_ID_KEY: user_id, DATETIME_KEY: snap_data.datetime,
                    AVAILABLE_RESULTS_KEY: avail_res, SNAPSHOT_ID_KEY: snapshot_id})


""" 
*** 'get_snapshot_result' assumes the user made sure the result is indeed available! *** 
"""
@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>', methods=['GET'])
def get_snapshot_result(user_id, snapshot_id, result_name):
    snap_info_data = _db_h.get_snapshot_result(snapshot_id, result_name)
    if result_name == "pose":
        res = {TRANS_X_KEY: snap_info_data.translation_x,
               TRANS_Y_KEY: snap_info_data.translation_y,
               TRANS_Z_KEY:  snap_info_data.translation_z,
               ROT_X_KEY: snap_info_data.rotation_x,
               ROT_Y_KEY: snap_info_data.rotation_y,
               ROT_Z_KEY: snap_info_data.rotation_z}
    elif result_name == "color-image":
        res = {WIDTH_KEY: snap_info_data.width,
               HEIGHT_KEY: snap_info_data.height,
               RESULT_URL_KEY: snap_info_data.data_path}
    elif result_name == "depth-image":
        res = {WIDTH_KEY: snap_info_data.width,
               HEIGHT_KEY: snap_info_data.height,
               RESULT_URL_KEY: snap_info_data.data_path}
    elif result_name == "feelings":
        res = {HUNGER_KEY: snap_info_data.hunger,
               THIRST_KEY: snap_info_data.thirst,
               EXHAUSTION_KEY: snap_info_data.exhaustion,
               HAPPINESS_KEY: snap_info_data.happiness,
               RESULT_URL_KEY: snap_info_data.path}
    else:
        raise UnsupportedTopic(f"ERROR: '{result_name}' is unknown. Use only one of: {TOPICS!r}")
    return jsonify(res)

