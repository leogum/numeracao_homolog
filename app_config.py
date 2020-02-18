from datetime import timedelta

from configs import Configs

conn_str = Configs.get_conn_str()
SECRET_KEY = Configs.get_secret_key()
UPLOAD_PATH = Configs.get_upload_path()
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = conn_str
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
