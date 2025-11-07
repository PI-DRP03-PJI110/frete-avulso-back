from config.database import get_connection


def get_all_despesa():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT ID_despesa as ID, descricao, valor, viagem as ID_viagem FROM despesas")
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao buscar todas as despesa: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def get_despesa(ID_despesa: str):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT ID_despesa as ID, descricao, valor, viagem as ID_viagem FROM despesas "
                       "WHERE ID_despesa = %s", (ID_despesa,))
        return cursor.fetchone()

    except Exception as e:
        print(f"Erro ao buscar a despesa de id {ID_despesa}: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def get_all_despesas_from_viagem(ID_viagem: str):

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT ID_despesa as ID, descricao, valor, viagem as ID_viagem FROM despesas "
                       "WHERE viagem = %s", (ID_viagem,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao buscar despesas para a viagem {ID_viagem}: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def add_despesa(descricao, valor, viagem):

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO despesas (descricao, valor, viagem) VALUES (%s, %s, %s)",
            (descricao, valor, viagem)
        )
        db.commit()
        return True

    except Exception as e:
        print(f"Erro ao adicionar nova despesa: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


def update_despesa(id, descricao, valor, viagem):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "UPDATE despesas SET descricao = %s, valor = %s, viagem = %s WHERE ID_despesa = %s ",
            (descricao, valor, viagem, id)
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


def excluir_despesa_de_viagem(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("DELETE FROM despesas  WHERE ID_despesa = %s ", (id,))
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
