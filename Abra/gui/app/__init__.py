from abra.common import *
from .app import app_bp
from flask import Flask
import sys


def config_app(flaskapp):
    flaskapp.config['gui_host'] = GUI_SERVER_HOST
    flaskapp.config['gui_port'] = GUI_SERVER_PORT
    flaskapp.config['api_host'] = API_SERVER_HOST
    flaskapp.config['api_port'] = API_SERVER_PORT


def create_gui_app():
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    config_app(app)
    return app


#  DEBUG
app = create_gui_app(host=GUI_SERVER_HOST, port=GUI_SERVER_PORT)
