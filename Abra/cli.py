import click
from .common import *
import pathlib
import requests
from requests.exceptions import HTTPError


@click.group()
def main():
    pass


@main.command("get-users")
@click.option("--host", "-h", default=LOCAL_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
def get_users(host, port):
    try:
        response = requests.get(f'http://{host}:{port}/users')
        if response.status_code != 200:
            raise HTTPError
        return response.json()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')
        return FAIL


@main.command("get-users")
@click.option("--host", "-h", default=LOCAL_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
@click.argument('user_id')
def get_user(host, port, user_id):
    try:
        response = requests.get(f'http://{host}:{port}/users/{user_id}')
        if response.status_code != 200:
            raise HTTPError
        return response.json()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')
        return FAIL


@main.command("get-users")
@click.option("--host", "-h", default=LOCAL_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
@click.argument('user_id')
def get_snapshots(host, port, user_id):
    try:
        response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
        if response.status_code != 200:
            raise HTTPError
        return response.json()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')
        return FAIL


@main.command("get-users")
@click.option("--host", "-h", default=LOCAL_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
@click.argument('user_id')
@click.argument('snapshot_id', help="The unique datetime of the target snapshot")
def get_snapshot(host, port, user_id, snapshot_id):
    try:
        response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
        if response.status_code != 200:
            raise HTTPError
        return response.json()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')
        return FAIL


@main.command("get-users")
@click.option("--host", "-h", default=LOCAL_HOST)
@click.option("--port", "-p", default=API_SERVER_PORT)
@click.argument('user_id')
@click.argument('snapshot_id', help="The unique datetime of the target snapshot")
@click.argument('result_name')
@click.option("--save", "-s")
def get_result(host, port, user_id, snapshot_id, result_name, save):
    try:
        response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}')
        if response.status_code != 200:
            raise HTTPError
        if save:
            path = pathlib.Path(save)
            path.write_text(response.text)
        return response.json()
    except HTTPError as err:
        print(f'HTTP error occurred: {err}')
        return FAIL
