from flask import *
from flask_login import *
from werkzeug.security import check_password_hash, generate_password_hash
from models import User

app = Flask(__name__)

login_manager = LoginManager() 
app.secret_key = 'guilherme'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id, usuarios)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return "Nada ainda"

@app.route('/cadastro')
def cadastro():
    return "Nada ainda"

@app.route('/produtos')
def produtos_page():
    return "Nada ainda"

if __name__ == "__main__":
    app.run(debug=True)
