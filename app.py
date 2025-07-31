from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import User

app = Flask(__name__)
app.secret_key = 'dev'
lm = LoginManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


@lm.user_loader
def load_user(id):
    usuario_logado = db.session.query(User).filter_by(id=id).first()
    return usuario_logado

#@app.route('/criar_conta', methods=['GET', 'POST'])
#def criar_conta():
#    if request.method == 'GET':
#        return render_template('criar.html')
#    
#    elif request.method == 'POST':
#        nome = request.form['nome']
#        crm = request.form['crm']
#        senha = request.form['senha']
#        novo_user = User(nome=nome, crm=crm, password=senha)
#        db.session.add(novo_user)
#        db.session.commit()
#        login_user(novo_user)
#    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        crm = request.form['crm']
        senha = request.form['senha']
        usuario = db.session.query(User).filter_by(crm=crm).first()
        
        if usuario and usuario.password == senha:
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash('crm ou senha incorretos.')
            return redirect(url_for('login'))
            
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.nome != 'dev.admin':
        flash('Você não tem permissão para acessar esta página.', 'error')
        return redirect(url_for('index'))
            
    elif request.method == 'GET': 
        usuarios_lista = db.session.query(User).all()
        return render_template('adm.html', usuario_consulta=usuarios_lista)
    
# (adicionar as condiçoes para as requisições GET e POST) 
    elif request.method == 'POST':
         nome_usuario = request.form['nome']
         crm_usuario = request.form['crm']
         senha_usuario = request.form['senha']
         novo_user = User(nome=nome_usuario, crm=crm_usuario, password=senha_usuario)
         db.session.add(novo_user)
         db.session.commit()
    return redirect(url_for('admin'))
       
        

@app.route('/pagina_principal')
@login_required
def index():
    load_user(current_user.nome)
    return render_template('index.html')







if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)