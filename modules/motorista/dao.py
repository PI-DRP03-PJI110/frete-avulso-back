from config.database import get_connection


def get_all_motoristas():
    try:

        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT CPF_moto as cpf, nome_moto as nome FROM motorista")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def get_motorista(cpf):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT CPF_moto as cpf, nome_moto as nome FROM motorista WHERE CPF_moto = %s", (cpf,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def add_motorista(cpf, nome):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO motorista (CPF_moto, nome_moto) VALUES (%s, %s)", (cpf, nome))
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


def update_motorista(cpf, nome):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE motorista SET nome_moto = %s WHERE CPF_moto = %s", (nome, cpf))
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

