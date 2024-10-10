from config.database import get_connection

def get_all_despesa():
    """
    Função para recuperar todas as despesas no banco de dados.
    """
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        
        # Exibir todos os registros da tabela "Despesas"
        cursor.execute("SELECT ID_despesa as ID, descricao, valor, viagem, FROM despesa")
        return cursor.fetchall()
    
    except Exception as e:
        print(f"Erro ao buscar todas as despesa: {e}")
        return None
    
    finally:
        # Fechar o cursor e a conexão de forma segura
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()

def get_despesa(ID_viagem: str):
    """
    Função para recuperar as despesas de uma viagem específica.
    :param ID_viagem: O identificador da viagem
    """
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        
        # Buscar despesas por ID da viagem
        cursor.execute("SELECT ID_despesa as ID, descricao, valor FROM despesa WHERE ID_viagem = %s", (ID_viagem,))
        return cursor.fetchone()
    
    except Exception as e:
        print(f"Erro ao buscar despesas para a viagem {ID_viagem}: {e}")
        return None
    
    finally:
        # Fechar o cursor e a conexão de forma segura
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()

def add_despesa(ID_despesa, descricao, valor, viagem):
    """
    Função para adicionar uma nova despesa ao banco de dados.
    :param ID: Identificador da despesa
    :param descricao: Descrição da despesa
    :param valor: Valor da despesa
    """
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        
        # Inserir uma nova despesa na tabela "Despesas"
        cursor.execute(
            "INSERT INTO despesa (ID_despesa, descricao, valor, viagem) VALUES (%s, %s, %s)",
            (ID_despesa, descricao, valor, viagem)
        )
        db.commit()
        return True

    except Exception as e:
        print(f"Erro ao adicionar nova despesa: {e}")
        return None
    
    finally:
        # Fechar o cursor e a conexão de forma segura
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()

def excluir_despesa_de_viagem(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        # Atualize o registro no banco de dados
        cursor.execute("DELETE FROM despesa  WHERE descricao = %s ", (id,))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        # Fechar o cursor e a conexão de forma segura
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None:
            db.close()


