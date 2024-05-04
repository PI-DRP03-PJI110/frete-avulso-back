import mysql.connector

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="univesp547",
    database="viagens_avulsas"
)

cursor = db.cursor(dictionary=True)


def get_all_viagens():
    try:
        # Exibir todos os registros do banco de dados

        cursor.execute(
            "SELECT ID_viagem as id, origem, destino, valor, NF as nf, data_viagem, carga, despesa, placa, CPF_moto as cpf_motorista, CPF_user as cpf_usuario FROM viagens")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None


def get_viagem(id: int):
    try:
        # Exibir todos os registros do banco de dados
        cursor.execute(
            "SELECT ID_viagem as id, origem, destino, valor, NF as nf, data_viagem, carga, despesa, placa, CPF_moto as cpf_motorista, CPF_user as cpf_usuario FROM viagens where ID_viagem = %s",
            (id,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


def add_viagem(origem, destino, valor, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario):
    try:
        cursor.execute(
            "INSERT INTO viagens (origem, destino, NF, data_viagem, carga, despesa, placa, CPF_moto, CPF_user, valor) "+
            " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (origem, destino, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario, valor))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return None


def update_viagem(id, origem, destino, valor, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario):
    try:
        # Atualize o registro no banco de dados
        cursor.execute(
            "UPDATE viagens SET origem = %s, destino = %s, NF = %s, data_viagem = %s, carga = %s, despesa = %s, placa = %s, CPF_moto = %s, CPF_user = %s, valor = %s WHERE ID_viagem = %s ",
            (origem, destino, NF, data_viagem, carga, despesa, placa, cpf_motorista, cpf_usuario, valor, id)
        )
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False
