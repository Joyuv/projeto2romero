from flask_login import UserMixin
import sqlite3
import os
from flask import current_app


class User(UserMixin):
    def __init__(self, id, nome_usuario, senha):
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conn = get_db_conexao()
        user_data = conn.execute(
            "SELECT id, senha FROM usuarios WHERE email = ?",
            (user_id,),
        ).fetchone()
        conn.close()
        if user_data:
            return cls(user_data["id"], user_data["senha"])
        return None


def get_db_conexao():
    conn = sqlite3.connect('database.db')
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
