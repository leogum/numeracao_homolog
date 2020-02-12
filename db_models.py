from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from configs import config_app

app = config_app()
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    __table_args__ = {'schema': 'dle'}

    id = db.Column(db.Integer, primary_key=True)
    nm_login = db.Column(db.String(10))
    nm_nome = db.Column(db.String(100))
    nr_rf = db.Column(db.String(20))
    nm_email = db.Column(db.String(50))
    dthr_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    login_atualizacao = db.Column(db.String(20))


class Numeracao(db.Model):
    __table_args__ = {'schema': 'dle'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cd_codlog = db.Column(db.String)
    cd_setor = db.Column(db.String, nullable=True)
    cd_quadra = db.Column(db.String, nullable=True)
    cd_lote = db.Column(db.String, nullable=True)
    nr_numeral_novo = db.Column(db.String, nullable=True)
    nr_numeral_antigo = db.Column(db.String, nullable=True)
    dt_publicacao = db.Column(db.String(15), nullable=True)
    nr_pagina = db.Column(db.String(5), nullable=True)
    nm_prefeitura_regional = db.Column(db.String, nullable=True)
    cd_expediente = db.Column(db.String, nullable=True)
    ds_despacho = db.Column(db.String, nullable=True)
    ds_endereco = db.Column(db.String, nullable=True)
    cd_decreto = db.Column(db.String, nullable=True)
    nm_interessados = db.Column(db.String, nullable=True)
    cd_solicitacao_numeracao = db.Column(db.String, nullable=True)
    ds_doc = db.Column(db.Text, nullable=True)
    retificada = db.Column(db.String(10), nullable=True)
    nm_login = db.Column(db.String(10))
    dthr_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


# terá sempre os dados da numeracao antiga( antes de ser retificada), os dados após retificação estarao na
# tabela original da numeração
class NumeracaoRetificada(db.Model):
    __table_args__ = {'schema': 'dle'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cd_codlog = db.Column(db.String)
    cd_setor = db.Column(db.String, nullable=True)
    cd_quadra = db.Column(db.String, nullable=True)
    cd_lote = db.Column(db.String, nullable=True)
    nr_numeral_novo = db.Column(db.String, nullable=True)
    nr_numeral_antigo = db.Column(db.String, nullable=True)
    dt_publicacao = db.Column(db.String(15), nullable=True)
    nr_pagina = db.Column(db.String(5), nullable=True)
    nm_prefeitura_regional = db.Column(db.String, nullable=True)
    cd_expediente = db.Column(db.String, nullable=True)
    ds_despacho = db.Column(db.String, nullable=True)
    ds_endereco = db.Column(db.String, nullable=True)
    cd_decreto = db.Column(db.String, nullable=True)
    nm_interessados = db.Column(db.String, nullable=True)
    cd_solicitacao_numeracao = db.Column(db.String, nullable=True)
    ds_doc = db.Column(db.Text, nullable=True)
    nm_login = db.Column(db.String(10))
    dthr_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class NumeracaoCrossRetificada(db.Model):
    __table_args__ = {'schema': 'dle'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_numeracao = db.Column(db.Integer, db.ForeignKey('dle.numeracao.id'))
    fk_numeracao_retificada = db.Column(db.Integer, db.ForeignKey('dle.numeracao_retificada.id'))
    nm_login = db.Column(db.String(10))
    dthr_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class Files(db.Model):
    __table_args__ = {'schema': 'dle'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nm_file = db.Column(db.String)
    nm_directory = db.Column(db.String)
    nm_extension = db.Column(db.String)
    nm_login = db.Column(db.String(10))
    dthr_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class FilesCrossNumeracao(db.Model):
    __table_args__ = {'schema': 'dle'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_files = db.Column(db.Integer, db.ForeignKey('dle.files.id'))
    fk_numeracao = db.Column(db.Integer, db.ForeignKey('dle.numeracao.id'))
    nm_login = db.Column(db.String(10))
    dthr_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class NumeracaoSchema(ma.ModelSchema):
    class Meta:
        model = Numeracao


class UsersSchema(ma.ModelSchema):
    class Meta:
        model = Users
