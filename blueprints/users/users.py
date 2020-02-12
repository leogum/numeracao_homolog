from flask import request, redirect, url_for, render_template, flash, Blueprint

from DAO import DAO
from db_models import Users
from helpers import login_required

users = Blueprint("users", __name__, template_folder='../users/templates')


# *********************************************************************************************************************
# *************************************************PARTE DE Usuários**************************************************
# *********************************************************************************************************************

# rota para renderizar uma tabela com todos os usuários ja inseridas no banco de dados
@users.route('/users_list')
@login_required
def userList():
    # if 'logged_user' not in session.keys():
    #     return redirect(url_for('login', next=url_for('userList')))
    results = DAO.list(Users)

    return render_template('userList.html', titulo='Lista de Usuários', results=results)


@users.route('/form_insert_user')
@login_required
def userC():
    # if 'logged_user' not in session.keys():
    #     return redirect(url_for('login', next=url_for('userC')))

    return render_template('userC.html', titulo='Cadastro de Usuarios')


# rota para renderizar a pagina da view de numeração e trazer os campos preenchidos para um certo ID da tabela do DB
@users.route('/view_user', methods=['POST', ])
@login_required
def userR():
    id_user = request.form['id_user']
    user = DAO.search_by_id(id_user, Users)

    return render_template('userR.html', titulo='Visualização de Usuário', user=user,
                           id_user=id_user)


# rota para renderizar a pagina de edição de numeração e trazer os campos preenchidos para um certo ID da tabela do DB
@users.route('/form_edit_user', methods=['POST', ])
@login_required
def userU():
    id_user = request.form['id_user']
    user = DAO.search_by_id(id_user, Users)

    return render_template('userU.html', titulo='Edição de Usuário', user=user,
                           id_user=id_user)


# -------------------------------------------------------------------------------------------------------------------

# rota para atualização dos dados no banco de dados, no caso na tabela de Usuários
@users.route('/update_user', methods=['POST', ])
@login_required
def update_user():
    form_data = request.form
    id_user = request.form['id_user']

    DAO.update(form_data, id_user, Users)
    flash('O Usuário foi atualizado com sucesso!')
    return redirect(url_for('users.userList'))


# rota para inserção no banco de dados, no caso na tabela de Usuários
@users.route('/insert_users', methods=['POST', ])
@login_required
def insert_user():
    if request.method == 'POST':
        form_data = request.form
        DAO.insert(form_data, Users)
        flash('Um novo usuário foi cadastrado no sistema com sucesso!')
        return redirect(url_for('users.userList'))
