from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from blueprints.bdt.bdt import bdt
from blueprints.file.file_routes import files_part
from blueprints.numeracao.numeracao import numeracao
from blueprints.users.users import users

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(numeracao)
app.register_blueprint(bdt)
app.register_blueprint(files_part)
app.config.from_pyfile('app_config.py')

db = SQLAlchemy(app)

from views import *

# sexta feira - deletar uma numeracao*--condições!

if __name__ == "__main__":
    app.run(debug=True, host='10.75.19.181', port='8084')
