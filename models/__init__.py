from flask_login import UserMixin
from iniciar import get_db_conexao


class User(UserMixin):
    def __init__(self, id, nome_usuario, senha):
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conn = get_db_conexao()
        user_data = conn.execute(
            "SELECT nome_usuario, senha FROM usuarios WHERE nome_usuario = ?",
            (user_id,),
        ).fetchone()
        conn.close()
        if user_data:
            return cls(user_data["nome_usuario"], user_data["senha"])
        return None
