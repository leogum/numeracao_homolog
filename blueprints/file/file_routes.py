import os

from flask import request, redirect, url_for, flash, Blueprint, session

from DAO import DAO
from configs import Configs
from db_models import Files, FilesCrossNumeracao as Cross
from helpers import login_required, file_delete

files_part = Blueprint("files_part", __name__, template_folder='../file/templates')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'gif', 'xls', 'xlsx', 'doc', 'docx', 'dwg', 'tiff'])


# *********************************************************************************************************************
# **********************************************PARTE DE UPLOAD DE ARQUIVOS********************************************
# *********************************************************************************************************************

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@files_part.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    id_numeracao = request.form['id_numeracao']
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('numeracaoU', id_numeracao=id_numeracao))

        file = request.files['file']

        if file and allowed_file(file.filename):
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = file.filename

            file.save(os.path.join(Configs.get_upload_path(), filename))
            file_path = os.path.abspath(Configs.get_upload_path() + '\\' + filename)

            file_data = {'nm_file': filename, 'nm_extension': str(extension), 'nm_directory': str(file_path),
                         'nm_login': session['logged_user']}
            id_files = DAO.insert(file_data, Files)

            cross_data = {'fk_files': str(id_files), 'fk_numeracao': str(id_numeracao),
                          'nm_login': session['logged_user']}
            id_cross = DAO.insert(cross_data, Cross)

            flash(f'File {file.filename} successfully uploaded')
            return redirect(url_for('numeracao.numeracaoU', id_numeracao=id_numeracao))

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif, xls, xlsx, doc, docx')
            return redirect(url_for('numeracao.numeracaoU', id_numeracao=id_numeracao))


@files_part.route('/delete_file', methods=['POST', ])
def delete_file():
    filename = request.form['nm_file']
    id_files = request.form['id_files']
    id_numeracao = request.form['id_numeracao']

    msg = file_delete(id_files, filename)

    flash(msg)
    return redirect(url_for('numeracao.numeracaoU', id_numeracao=id_numeracao))
