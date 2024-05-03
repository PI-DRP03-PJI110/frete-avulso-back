import mysql.connector

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="univesp547",
    database="viagens_avulsas"
)

cursor = db.cursor(dictionary=True)


def get_all_motoristas():
    try:
        # Exibir todos os registros do banco de dados

        cursor.execute("SELECT CPF_moto as cpf, nome_moto as nome FROM motorista")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None


def get_motorista(cpf):
    try:
        # Exibir todos os registros do banco de dados
        cursor.execute("SELECT CPF_moto as cpf, nome_moto as nome FROM motorista WHERE CPF_moto = %s", (cpf,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


def add_motorista(cpf, nome):
    try:
        # Adicionar um novo registro ao banco de dados
        cursor.execute("INSERT INTO motorista (CPF_moto, nome_moto) VALUES (%s, %s)", (cpf, nome))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False


def update_motorista(cpf, nome):
    try:
        # Atualize o registro no banco de dados
        cursor.execute("UPDATE motorista SET nome_moto = %s WHERE CPF_moto = %s", (nome, cpf))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False

