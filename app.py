from flask import *
from flask_login import *
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, get_db_conexao
from werkzeug.utils import secure_filename
import os

try:
    with open("database.db", "r"):
        print("Banco já existe")
except:
    with open("schema.sql", "r") as f:
        conn = get_db_conexao()
        conn.executescript(f.read())
        conn.commit()
        conn.close()


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["MAX_CONTENT_LENGHT"] = 4 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

login_manager = LoginManager()
app.secret_key = "guilherme"
login_manager.init_app(app)
login_manager.login_view = "index"


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_conexao()
    user_data = conn.execute(
        "SELECT * FROM usuarios WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if user_data is None:
        return None
    return User(user_data["id"], user_data["nome_usuario"], user_data["senha"])


# -- Rotas da aplicação --


@app.route("/uploads/<filename>")
def imagem(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    conn = get_db_conexao()
    user_products = conn.execute(
        "SELECT * FROM produtos WHERE usuario_id = ?", (current_user.id,)
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", user_products=user_products)


@app.route("/produtos/adicionar", methods=["POST"])
@login_required
def adicionar_produto():
    name = request.form.get("name")
    description = request.form.get("description")
    preco = request.form.get("preco")
    imagem = request.files["image"]

    if imagem:
        filename_base = secure_filename(name)
        ext = imagem.filename.rsplit(".", 1)[1].lower()
        filename = f"{filename_base}.{ext}"

        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        imagem.save(image_path)

    user_id = current_user.id
    conn = get_db_conexao()
    try:
        conn.execute(
            "INSERT INTO produtos(imagem, usuario_id, nome, descricao, preco) VALUES (?, ?, ?, ?, ?)",
            (filename, user_id, name, description, preco),
        )
    except:
        print("Erro ao adicionar")
    conn.commit()
    conn.close()
    flash("Produto adicionado com sucesso!", "success")
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email_usuario = request.form.get("email_usuario")
        senha_usuario = request.form.get("senha_usuario")
        conn = get_db_conexao()
        user_data = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email_usuario,)
        ).fetchone()
        conn.close()

        if user_data and check_password_hash(user_data["senha"], senha_usuario):
            user = User(user_data["id"], user_data["nome_usuario"], user_data["senha"])
            login_user(user)
            flash("Login realizado com sucesso", "success")
            # reedirecionamento para o dashboard
            return redirect(url_for("dashboard"))
        else:
            print("erro")
            flash("Nome de usuário ou senha incorretos", "error")

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email_usuario = request.form["email_usuario"]
        nome_usuario = request.form["nome_usuario"]
        senha_usuario = request.form["senha_usuario"]

        if not nome_usuario or not senha_usuario or not email_usuario:
            flash("Preencha todos os campos", "error")
            return redirect(url_for("cadastro"))

        senha_hash = generate_password_hash(senha_usuario)
        conn = get_db_conexao()
        try:
            conn.execute(
                "INSERT INTO usuarios (email, nome_usuario, senha) VALUES (?, ?, ?)",
                (email_usuario, nome_usuario, senha_hash),
            )
            conn.commit()
        except conn.IntegrityError:
            flash("Nome de usuário já existe", "error")
            return redirect(url_for("cadastro"))
        finally:
            conn.close()
        flash("Cadastro realizado com sucesso", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logout realizado com sucesso", "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


def produtos_populares():
    conn = get_db_conexao()
    produtos_count = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    if produtos_count == 0:
        # exemplo qualquer aq, to corigando pai
        produtos_data = [
            ("Produto 1", 10.99, "Descrição do Produto 1"),
            ("Produto 2", 15.49, "Descrição do Produto 2"),
            ("Produto 3", 7.99, "Descrição do Produto 3"),
        ]
        conn.executemany(
            "INSERT INTO produtos (nome, preco, descricao) VALUES (?, ?, ?)",
            produtos_data,
        )
        conn.commit()
    conn.close()

    return render_template("produtos.html")


@app.route("/produtos/editar", methods=["POST", "GET"])
@login_required
def editar_produto():
    if request.method == "POST":
        nome = request.form.get("name")
        descricao = request.form.get("description")
        preco = request.form.get("preco")
        id = request.form.get("id")

        conn = get_db_conexao()
        cursor = conn.cursor()
        if nome:
            cursor.execute("UPDATE produtos SET nome = ? WHERE id = ?", (nome, id))
        if preco:
            cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (preco, id))
        if descricao:
            cursor.execute(
                "UPDATE produtos SET descricao = ? WHERE id = ?", (descricao, id)
            )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    else:
        id = request.args.get("product_id")
        conn = get_db_conexao()
        user_products = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (id,)
        ).fetchone()
        conn.close()
        return render_template("editar.html", id=id, produto=user_products)


@app.route("/produtos/remover")
@login_required
def remover_produto():
    produto_id = request.args.get("product_id")

    conn = get_db_conexao()
    conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/produtos")
def produtos():
    conn = get_db_conexao()
    cursor = conn.cursor()
    if current_user.is_authenticated:
        produtos = cursor.execute(
            "SELECT * FROM produtos WHERE usuario_id != ? ", (current_user.id,)
        ).fetchall()
    else:
        produtos = cursor.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return render_template("produtos.html", produtos=produtos)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=False)
