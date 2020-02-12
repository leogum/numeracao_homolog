import functools
import json
import os

import requests
from flask import session, redirect, url_for

from DAO import *
from configs import Configs
from db_models import Users, Files


def validar_AD(user, passw):
    # a linha abaixo pode virar uma função separada depois de construção de URL para GET com PARAM
    # url = 'http://10.75.16.175:8084/conexao_ldap/?user={user}&passw={passw}'.format(user=user, passw=passw) #pc henriq
    url = 'http://10.75.19.181:8083/conexao_ldap/?user={user}&passw={passw}'.format(user=user, passw=passw)  # pc leo

    # a linha abaixo pode virar uma função separada depois de resolução de proxy
    proxies = {'http': 'http://{user}:{passw}@10.10.193.25:3128'.format(user=user, passw=passw),
               'https': 'https://{user}:{passw}@10.10.193.25:3128'.format(user=user, passw=passw)}

    # with requests.get(url, proxies=proxies) as f:
    with requests.get(url) as f:
        json_resp = f.text

    return json.loads(json_resp)


# valida o login do sistema com o login cadastrado no banco de dados na tabela de usuarios
def validar_db(login):
    query_result = Users.query.filter_by(nm_login=login).first()

    if query_result is not None:
        return True
    else:
        return False


# verificar na sessao se o usuario ja está logado, se nao estiver ele sera redirecionado para pagina de login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'logged_user' in session.keys():
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


# função para retornar os arquivos de uma numeração especifica que foram feitos upload no sistema
def return_files_numeracao(id_numeracao, table_files_obj):
    fk_files = DAO.search_files_numeracao(id_numeracao)
    file_list = {}
    for r in fk_files:
        fk_files = r.fk_files,
        files = DAO.search_by_id_all(fk_files, table_files_obj)
        for f in files:
            file_list[f] = {}
    return file_list


# deleta um arquivo que tinha sido feito upload pelo sistema
def file_delete(id_files, filename):
    file = os.path.join(Configs.get_upload_path(), filename)
    if os.path.isfile(file):
        os.remove(file)
    # primeiro deve ser deletado da tabela cross pq no db tem constraints que ligam as primary keys com as
    # foreigns keys, entao o db nao deixa deletar da tabela files enquanto ainda houver ligação com a tabela cross
    DAO.delete_cross_files(id_files)
    DAO.delete(id_files, Files)
    msg = 'Arquivo deletado'
    return msg


# retifica uma numeração especifica e salva o historico da retificação
def retificacao_numeracao(id_numeracao, numeracao_obj, form_data, numeracao_retificada_obj, login):
    numeracao = DAO.search_by_id(id_numeracao, numeracao_obj)

    numeracao_data = {
        'cd_codlog': numeracao.cd_codlog,
        'cd_setor': numeracao.cd_setor,
        'cd_quadra': numeracao.cd_quadra,
        'cd_lote': numeracao.cd_lote,
        'nr_numeral_novo': numeracao.nr_numeral_novo,
        'nr_numeral_antigo': numeracao.nr_numeral_antigo,
        'dt_publicacao': numeracao.dt_publicacao,
        'nr_pagina': numeracao.nr_pagina,
        'nm_prefeitura_regional': numeracao.nm_prefeitura_regional,
        'cd_expediente': numeracao.cd_expediente,
        'ds_despacho': numeracao.ds_despacho,
        'ds_endereco': numeracao.ds_endereco,
        'cd_decreto': numeracao.cd_decreto,
        'nm_interessados': numeracao.nm_interessados,
        'cd_solicitacao_numeracao': numeracao.cd_solicitacao_numeracao,
        'ds_doc': numeracao.ds_doc,
        'nm_login': numeracao.nm_login,
    }

    # segundo- fazer o insert na tabela de numeracoes retificadas com os dados da busca acima
    id_numeracao_retificada = DAO.insert(numeracao_data, numeracao_retificada_obj)

    # terceiro- fazer update na numeração que vai ser retificada com os dados novos na tabela de Numeracao
    fk_numeracao = DAO.update(form_data, id_numeracao, numeracao_obj)

    # quarto- fazer insert na tabela NumeracaoCrossRetificaçao com o id da numeracao retificada e a atualizada(update)
    cross_data = {
        'fk_numeracao': fk_numeracao,
        'fk_numeracao_retificada': id_numeracao_retificada,
        'nm_login': login
    }
    id_cross = DAO.insert(cross_data, CrossRet)
    return fk_numeracao
