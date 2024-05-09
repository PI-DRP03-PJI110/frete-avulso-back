import hashlib

from config.database import get_connection

db = get_connection()


cursor = db.cursor(dictionary=True)


# Função para criar o hash da senha
def hash_password(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()


def get_all_users():
    try:
        # Exibir todos os registros do banco de dados

        cursor.execute("SELECT CPF_user as cpf, nome, funcao, endereco, email FROM usuario")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None


def get_user(cpf):
    try:
        # Exibir todos os registros do banco de dados
        cursor.execute("SELECT CPF_user as cpf, nome, funcao, endereco, email FROM usuario WHERE CPF_user = %s", (cpf,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


def get_user_login(cpf):
    try:
        # Exibir todos os registros do banco de dados
        cursor.execute("SELECT CPF_user as cpf, senha FROM usuario WHERE CPF_user = %s", (cpf,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None

def add_user(cpf, nome, funcao, endereco, senha, email):
    try:
        # Adicionar um novo registro ao banco de dados
        cursor.execute(
            "INSERT INTO usuario (CPF_user, nome, funcao, endereco, senha, email) VALUES (%s, %s, %s, %s, %s, %s)",
            (cpf, nome, funcao, endereco, senha, email))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False


def update_user(cpf, nome, funcao, endereco, senha, email):
    try:
        # Atualize o registro no banco de dados
        cursor.execute(
            "UPDATE usuario SET email = %s, endereco = %s, funcao = %s, nome = %s, senha = %s where CPF_user = %s",
            (email, endereco, funcao, nome, senha, cpf)
        )
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False


def delete_usuario(cpf):
    try:
        # Deletar um registro do banco de dados
        cursor.execute("UPDATE usuario SET senha = 'excluido' WHERE CPF_user = %s", (cpf,))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False
