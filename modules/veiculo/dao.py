from config.database import get_connection


def get_all_veiculos():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT placa, ID_veiculo as descricao, CPF_moto as cpf_motorista FROM veiculo")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def get_veiculo(placa: str):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT placa, ID_veiculo as descricao, CPF_moto as cpf_motorista FROM veiculo WHERE placa = %s",
                       (placa,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def add_veiculo(placa, descricao, cpf_motorista: None):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        if not cpf_motorista:
            cursor.execute("INSERT INTO veiculo (placa, ID_veiculo) VALUES (%s, %s)", (placa, descricao))
        else:
            cursor.execute("INSERT INTO veiculo (placa, ID_veiculo, CPF_moto) VALUES (%s, %s, %s)",
                           (placa, descricao, cpf_motorista))
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


def update_veiculo(placa, descricao, cpf_motorista: None):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("UPDATE veiculo SET ID_veiculo = %s, CPF_moto = %s WHERE placa = %s",
                       (descricao, cpf_motorista, placa))
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
