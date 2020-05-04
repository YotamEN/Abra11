from abra.common import *
from flask import render_template, url_for, Blueprint, request, current_app
from json import loads
import requests
import sys


app_bp = Blueprint('app_bp', __name__, template_folder='templates', static_folder='static')


@app_bp.route('/', methods=['GET'])
def homepage():
    return render_template("main.html")


@app_bp.route(f'/users/', methods=['GET'])
def users_page():
    gui_url, api_url = get_urls()

    users = []
    if request.method == 'GET':
        response = requests.get(api_url + f'/users')
        users_json = response.json()
        for user_json in users_json:
            users.append({
                USER_ID_KEY: user_json[USER_ID_KEY],
                USERNAME_KEY: user_json[USERNAME_KEY],
                USER_URL_KEY: f'{gui_url}/users/{user_json[USER_ID_KEY]}',
                USER_SNAPSHOTS_URL_KEY: f'{gui_url}/users/{user_json[USER_ID_KEY]}/snapshots'
            })
    return render_template("users.html", users=users)


@app_bp.route("/users/<int:user_id>/", methods=['GET'])
def user_page(user_id):
    gui_url, api_url = get_urls()

    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}')
        user_info_json = response.json()
        user_info = loads(user_info_json)
        user_info[USER_SNAPSHOTS_URL_KEY] = f'/users/{user_id}/snapshots'
        return render_template("user.html", user_info=user_info)


@app_bp.route("/users/<int:user_id>/snapshots/", methods=['GET'])
def user_snapshots(user_id):
    gui_url, api_url = get_urls()

    if request.method == 'GET':
        response = requests.get(api_url + f'/users/{user_id}/snapshots/')
        user_snapshots_json = response.json()
        snapshots = loads(user_snapshots_json)

        res = {USER_URL_KEY: f'/users/{user_id}', SNAPSHOTS_LIST_KEY: snapshots}
        return res  # FIXME and the rest of this


@app_bp.route("/users/<int:user_id>/snapshots/<snapshot_id>/", methods=['GET'])
def snapshot_page(user_id, snapshot_id):
    gui_url, api_url = get_urls()

    return f"snapshot page for {user_id}:{snapshot_id}!!"


@app_bp.route("/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>/", methods=['GET'])
def result_page(user_id, snapshot_id, result_name):
    gui_url, api_url = get_urls()

    return f"snapshot page for {user_id}:{snapshot_id}:{result_name}!!"


def get_urls():
    gui_host = current_app.config['gui_host']
    gui_port = current_app.config['gui_port']
    api_host = current_app.config['api_host']
    api_port = current_app.config['api_port']
    gui_url = f'http://{gui_host}:{gui_port}'
    api_url = f'http://{api_host}:{api_port}'
    return gui_url, api_url
