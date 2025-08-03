from flask import *
from flask_login import *
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, get_db_conexao
from iniciar import init_db
import os

app = Flask(__name__)

login_manager = LoginManager()
app.secret_key = "guilherme"
login_manager.init_app(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_conexao()
    user_data = conn.execute('SELECT nome_usuario, senha FROM usuarios WHERE nome_usuario = ?', (user_id,)).fetchone()
    conn.close()
    if user_data is None:
        return None
    return User(user_data['nome_usuario'], user_data['nome_usuario'], user_data['senha'])

# -- Rotas da aplicação --


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    conn = get_db_conexao()
    user_products = conn.execute('SELECT * FROM produtos WHERE usuario_id = ?', (current_user.id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', user_products=user_products)

@app.route('/adicionar_produto', methods=['POST'])
@login_required
def adicionar_produto():
    name = request.form.get('name')
    description = request.form.get('description')
    user_id = current_user.id

    conn = get_db_conexao()
    conn.execute('INSERT INTO products (user_id, name, description) VALUES (?, ?, ?)', (user_id, name, description))
    conn.commit()
    conn.close()
    flash('Produto adicionado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == "POST":
        nome_usuario = request.form['nome_usuario']
        senha_usuario = request.form['senha_usuario']

        conn = get_db_conexao()
        user_data = conn.execute('SELECT nome_usuario, senha FROM usuarios WHERE nome_usuario = ?', (nome_usuario,)).fetchone()
        conn.close()

        if user_data and check_password_hash(user_data['senha'], senha_usuario):
            user = User(user_data['nome_usuario'], user_data['nome_usuario'], user_data['senha'])
            login_user(user)
            flash('Login realizado com sucesso', 'success')
            # reedirecionamento para o dashboard
            prox_pag = request.args.get('next')
            return redirect(prox_pag or url_for('dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos', 'error')        

    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome_usuario = request.form['nome_usuario']
        senha_usuario = request.form['senha_usuario']

        if not nome_usuario or not senha_usuario:
            flash('Preencha todos os campos', 'error')
            return redirect(url_for('dashboard'))

        senha_hash = generate_password_hash(senha_usuario)
        conn = get_db_conexao()
        try:
            conn.execute('INSERT INTO usuarios (nome_usuario, senha) VALUES (?, ?)',(nome_usuario, senha_hash))
            conn.commit()
        except conn.IntegrityError:
            flash('Nome de usuário já existe', 'error')
            return redirect(url_for('cadastro'))
        finally:
            conn.close()
        flash('Cadastro realizado com sucesso', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')  

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('index'))



@app.route("/produtos")
def produtos_page():
    conn = get_db_conexao()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('produtos.html', produtos=produtos)

def produtos_populares():
    conn = get_db_conexao()
    produtos_count = conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
    if produtos_count == 0:
        # exemplo qualquer aq, to corigando pai 
        produtos_data = [
            ('Produto 1', 10.99, 'Descrição do Produto 1'),
            ('Produto 2', 15.49, 'Descrição do Produto 2'),
            ('Produto 3', 7.99, 'Descrição do Produto 3'),

        ]
        conn.executemany('INSERT INTO produtos (nome, preco, descricao) VALUES (?, ?, ?)', produtos_data)
        conn.commit()
    conn.close()

    return render_template('produtos.html')

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True)
