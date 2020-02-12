from flask import request, redirect, url_for, render_template, flash, Blueprint, session

from DAO import DAO
from configs import Configs
from db_models import Numeracao, Files, NumeracaoRetificada, NumeracaoSchema
from helpers import login_required, return_files_numeracao, retificacao_numeracao

numeracao = Blueprint("numeracao", __name__, template_folder='../numeracao/templates')


# rota para renderizar a pagina de inserção de numeração
@numeracao.route('/create_numeracao')
@login_required
def numeracaoC():
    return render_template('numeracaoC.html', titulo='Cadastro de Numeração', retificacao=False, insert=True)


# rota para renderizar a pagina da view de numeração e trazer os campos preenchidos para um certo ID da tabela do DB
@numeracao.route('/view_numeracao?id=<id_numeracao>', methods=['GET', ])
@login_required
def numeracaoR(id_numeracao):
    numeracao = DAO.search_by_id(id_numeracao, Numeracao)
    file_list = return_files_numeracao(id_numeracao, Files)
    file_path = Configs.get_file_path()
    return render_template('numeracaoR.html', titulo='Visualização de Numeração', numeracao=numeracao,
                           id_numeracao=id_numeracao, files=file_list, retificada=False, file_path=file_path)


# rota para renderizar a pagina de edição de numeração e trazer os campos preenchidos para um certo ID da tabela do DB
@numeracao.route('/edit_numeracao?id=<id_numeracao>', methods=['GET', ])
@login_required
def numeracaoU(id_numeracao):
    numeracao = DAO.search_by_id(id_numeracao, Numeracao)
    file_list = return_files_numeracao(id_numeracao, Files)
    file_path = Configs.get_file_path()
    return render_template('numeracaoU.html', titulo='Edição de Numeração', numeracao=numeracao,
                           id_numeracao=id_numeracao, files=file_list, retificacao=False, file_path=file_path,
                           insert=True)


# rota para renderizar a pagina de edição de numeração e trazer os campos preenchidos para um certo ID da tabela do DB
@numeracao.route('/retificar_numeracao?id=<id_numeracao>', methods=['GET', ])
@login_required
def numeracaoRET(id_numeracao):
    numeracao = DAO.search_by_id(id_numeracao, Numeracao)
    file_list = return_files_numeracao(id_numeracao, Files)
    return render_template('numeracaoRET.html', titulo='Retificação de Numeração', numeracao=numeracao,
                           id_numeracao=id_numeracao, files=file_list, retificacao=True)


@numeracao.route('/numeracao_retificada?=id<id_numeracao>', methods=['GET', ])
@login_required
def numeracao_retificada(id_numeracao):
    cross_ret = DAO.search_numeracao_retificada(id_numeracao)
    id_numeracao_retificada = cross_ret.fk_numeracao_retificada
    numeracao_retificada = DAO.search_by_id(id_numeracao_retificada, NumeracaoRetificada)

    flash('Se trata de uma numeração que foi retificada, conteudo apenas para historico!')
    return render_template('numeracaoR.html', titulo='Numeracao antes da retificação de Numeração',
                           numeracao=numeracao_retificada, id_numeracao=id_numeracao, retificada=True)


# -------------------------------------------------------------------------------------------------------------------

# rota para inserção no banco de dados, no caso na tabela de Numeração
@numeracao.route('/insert_numeracao', methods=['POST', ])
@login_required
def insert_numeracao():
    form_data = request.form

    id_numeracao = DAO.insert(form_data, Numeracao)
    flash('Uma nova numeração foi cadastrada com sucesso!')
    return redirect(url_for('numeracao.numeracaoU', id_numeracao=id_numeracao))


# rota para atualização dos dados no banco de dados, no caso na tabela de Numeração
@numeracao.route('/update_numeracao', methods=['POST', ])
@login_required
def update_numeracao():
    form_data = request.form
    id_numeracao = request.form['id_numeracao']

    DAO.update(form_data, id_numeracao, Numeracao)
    flash('A numeração foi atualizada com sucesso!')
    return redirect(url_for('index'))


# rota para retificação, no caso na tabela de Numeração uma numeração retificada
@numeracao.route('/retificar', methods=['POST', ])
@login_required
def retificar():
    form_data = request.form
    id_numeracao = request.form['id_numeracao']
    login = session['logged_user']

    fk_numeracao = retificacao_numeracao(id_numeracao, Numeracao, form_data, NumeracaoRetificada, login)
    flash('Numeração foi retificada com sucesso!')
    return redirect(url_for('numeracao.numeracaoU', id_numeracao=fk_numeracao))
