import os

from flask import Flask


class Configs:

    @staticmethod
    def get_conn_str():
        CONN_STR = 'postgresql://x369482:x369482@10.75.19.181/case'
        return CONN_STR

    @staticmethod
    def get_upload_path():
        PATH_STR = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'
        return PATH_STR

    @staticmethod
    def get_file_path():
        FILE_PATH = os.path.relpath(Configs.get_upload_path())

        return FILE_PATH


def config_app():
    app = Flask(__name__)
    app.config.from_pyfile('app_config.py')

    # app.register_blueprint(auth)
    return app
