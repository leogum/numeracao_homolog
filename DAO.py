from sqlalchemy.exc import IntegrityError

from db_models import db, FilesCrossNumeracao as CrossFiles, NumeracaoCrossRetificada as CrossRet


class DAO:

    # busca por id em quaisquer tabela do banco de dados e retorna um valor.
    @staticmethod
    def search_by_id(table_id, table_obj):
        query_result = None
        try:
            query_result = table_obj.query.filter_by(id=table_id).first()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
        return query_result

    # retorna uma numeração de casa que foi retificada.
    @staticmethod
    def search_numeracao_retificada(fk_numeracao):
        query_result = None
        try:
            query_result = CrossRet.query.filter_by(fk_numeracao=fk_numeracao).first()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
        return query_result

    @staticmethod
    def search_by_id_all(table_id, table_obj):
        query_result = None
        try:
            query_result = table_obj.query.filter_by(id=table_id).all()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
        return query_result

    # procura pelos arquivos utilizando a tabela CROSS
    @staticmethod
    def search_files_numeracao(fk_numeracao):
        query_result = None
        try:
            query_result = CrossFiles.query.filter_by(fk_numeracao=fk_numeracao).all()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
        return query_result

    # lista tudo da tabela que for passada
    @staticmethod
    def list(table_obj):
        query_result = db.session.query(table_obj).all()
        return query_result

    # insere em quaisquer tabela os dados do formulario que foi enviado
    @staticmethod
    def insert(form_data, table_obj):
        table = table_obj()
        try:
            for attr_name, attr_value in form_data.items():
                if attr_name != 'id':
                    setattr(table, attr_name, attr_value)
            db.session.add(table)
            db.session.commit()
            return table.id
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()

    # atualiza a tabela pelo ID com os dados inseridos no formulario de edição
    @staticmethod
    def update(form_data, table_id, table_obj):
        datas_to_change = table_obj.query.filter_by(id=table_id).first()
        try:
            for attr_name, attr_value in form_data.items():
                if attr_name != 'id':
                    setattr(datas_to_change, attr_name, attr_value)
            db.session.merge(datas_to_change)
            db.session.commit()
            return datas_to_change.id
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()

    # procura pelo atributo name em quaisquer tabela que tenha esse atributo
    @staticmethod
    def search_by_name(name, table_obj):
        query_result = None
        try:
            query_result = table_obj.query.filter_by(nm_name=name).first()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
        return query_result

    # busca por login em quaisquer tabela que tenha o atributo login
    @staticmethod
    def search_by_login(login, table_obj):
        query_result = None
        try:
            query_result = table_obj.query.filter_by(nm_login=login).first()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
        return query_result.nm_nome

    #  deleta os dados cadastrados em quaisquer tabela por um id especifico
    @staticmethod
    def delete(table_id, table_obj):
        try:
            data = db.session.query(table_obj).filter_by(id=table_id).first()
            db.session.delete(data)
            db.session.commit()
            return print('deleted')
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()

# deleta os dados cadastrados na tabela Cross de arquivos pelo id da tabela de arquivos
    @staticmethod
    def delete_cross_files(id_files):
        try:
            data = db.session.query(CrossFiles).filter_by(fk_files=id_files).first()
            db.session.delete(data)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        finally:
            db.close_all_sessions()
