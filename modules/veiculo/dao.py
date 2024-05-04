import mysql.connector

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="univesp547",
    database="viagens_avulsas"
)

cursor = db.cursor(dictionary=True)


def get_all_veiculos():
    try:
        # Exibir todos os registros do banco de dados

        cursor.execute("SELECT placa, ID_veiculo as descricao, CPF_moto as cpf_motorista FROM veiculo")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None


def get_veiculo(placa: str):
    try:
        # Exibir todos os registros do banco de dados
        cursor.execute("SELECT placa, ID_veiculo as descricao, CPF_moto as cpf_motorista FROM veiculo WHERE placa = %s",
                       (placa,))
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None


def add_veiculo(placa, descricao, cpf_motorista: None):
    try:
        if cpf_motorista is None:
            cursor.execute("INSERT INTO veiculo (placa, ID_veiculo) VALUES (%s, %s)", (placa, descricao))
        else:
            cursor.execute("INSERT INTO veiculo (placa, ID_veiculo, CPF_moto) VALUES (%s, %s, %s)",
                           (placa, descricao, cpf_motorista))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False


def update_veiculo(placa, descricao, cpf_motorista: None):
    try:
        # Atualize o registro no banco de dados
        cursor.execute("UPDATE veiculo SET ID_veiculo = %s, CPF_moto = %s WHERE placa = %s",
                       (descricao, cpf_motorista, placa))
        db.commit()
        return True

    except Exception as e:
        print(e)
        return False
