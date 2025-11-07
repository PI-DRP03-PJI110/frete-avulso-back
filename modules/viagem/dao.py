from config.database import get_connection



def get_all_viagens():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT ID_viagem as id, solicitante, origem, destino, valor, NF as nf, data_viagem, carga, despesa, placa, CPF_moto as cpf_motorista, CPF_user as cpf_usuario FROM viagens")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def get_viagem(id: int):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT ID_viagem as id, solicitante, origem, destino, valor, NF as nf, data_viagem, carga, despesa, placa, CPF_moto as cpf_motorista, CPF_user as cpf_usuario FROM viagens where ID_viagem = %s",
            (id,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def add_viagem(solicitante, origem, destino, valor, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO viagens (solicitante, origem, destino, NF, data_viagem, carga, despesa, placa, CPF_moto, CPF_user, valor) "+
            " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (solicitante, origem, destino, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario, valor))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def update_viagem(id, solicitante, origem, destino, valor, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "UPDATE viagens SET solicitante = %s, origem = %s, destino = %s, NF = %s, data_viagem = %s, carga = %s, despesa = %s, placa = %s, CPF_moto = %s, CPF_user = %s, valor = %s WHERE ID_viagem = %s ",
            (solicitante, origem, destino, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario, valor, id)
        )
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def excluir_viagem(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("DELETE FROM viagens  WHERE ID_viagem = %s ", (id,))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()
