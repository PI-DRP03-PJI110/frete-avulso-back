import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

VARS = ("DB_HOST","DB_USER","DB_PASS","DB_DATABASE")

def get_connection():
    missing = [k for k in VARS if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Variáveis ausentes: {', '.join(missing)}")
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DATABASE"),
        connection_timeout=10,
    )