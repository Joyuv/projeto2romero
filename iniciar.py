import sqlite3
import os
from flask import current_app


def get_db_conexao():
    db_path = os.path.join(current_app.root_path, "database.db")
    print(f"Conectando ao banco em: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    with app.app_context():
        db_path = os.path.join(app.root_path, "database.db")
        print(f"Criando banco em: {db_path}")
        schema_path = os.path.join(app.root_path, "schema.sql")

        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"schema.sql não encontrado em: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            schema = f.read()

        conn = sqlite3.connect(db_path)
        conn.executescript(schema)
        conn.commit()
        conn.close()
        print("Banco de dados criado com sucesso!")
