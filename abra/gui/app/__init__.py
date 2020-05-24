from .app import app_bp
from flask import Flask


def config_app(flaskapp, host, port, api_host, api_port):
    flaskapp.config['gui_host'] = host
    flaskapp.config['gui_port'] = port
    flaskapp.config['api_host'] = api_host
    flaskapp.config['api_port'] = api_port


def create_gui_app():
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    return app


def run_server(host, port, api_host, api_port):
    app = create_gui_app()
    config_app(app, host=host, port=port, api_host=api_host, api_port=api_port)
    app.run(host=host, port=port)

