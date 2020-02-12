from flask import request, redirect, url_for, render_template, session, flash

from DAO import DAO
from app import app
from db_models import Numeracao, Users
from helpers import validar_AD, validar_db, login_required


# *********************************************************************************************************************
# **************************************************PARTES GERAIS**************************************************
# *********************************************************************************************************************


# rota da pagina inicial com a tabela com todas as numerações ja inseridas no banco de dados
@app.route('/index')
@login_required
def index():
    results = DAO.list(Numeracao)
    return render_template('numeracaoList.html', titulo='Lista de Numeração', numeracao=results)


# rota para logar no sistema
@app.route('/')
def login():
    return render_template('login.html')


# rota para deslogar do sistema, limpando a sessao
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# *********************************************************************************************************************
# ***************************************PARTE DE AUTENTICAÇÃO NO LOGIN************************************************
# *********************************************************************************************************************

# rota de autenticação de login
@app.route('/authenticate', methods=['POST', ])
def authenticate():
    login = request.form['user']
    passw = request.form['passw']

    validacao_db = validar_db(login)
    validacao_ad = validar_AD(login, passw)

    # verifica no banco de dados e no LDAP da prodam se o usuario existe
    if validacao_ad and validacao_db:
        session['logged_user'] = login
        session.permanent = True
        username = DAO.search_by_login(login, Users)
        flash('Bem vindo(a), ' + username + '!')
        next = request.form['next']
        return redirect(next)

    # verifica apenas no LDAP da prodam se o usuario existe
    elif validacao_ad:
        session['logged_user'] = login
        session.permanent = True
        flash('Bem vindo(a), ' + login + '!')
        next = request.form['next']
        return redirect(next)
    else:
        flash('Nao foi possivel fazer login')
        return redirect(url_for('login'))
