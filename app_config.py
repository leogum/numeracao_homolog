from datetime import timedelta

from configs import Configs

conn_str = Configs.get_conn_str()
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = conn_str
UPLOAD_PATH = Configs.get_upload_path()
# UPLOAD_FOLDER = 'c:\\uploads_numeracao'
SECRET_KEY = "case"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
