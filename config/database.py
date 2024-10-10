import os
import mysql.connector

conn_host = "DB_Host"
conn_user = "DB_USER"
conn_password = "DB_PASS"
conn_database = "DB_DATABASE"


def get_connection():
    #host = os.environ[conn_host]
    #user = os.environ[conn_user]
    #password = os.environ[conn_password]
    #database = os.environ[conn_database]
    host = "sql.freedb.tech"
    user = "freedb_teste111_user"
    password = "pfXsJ4J#qUm@dBd"
    database = "freedb_teste111"

    # Configurações do banco de dados
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return db
