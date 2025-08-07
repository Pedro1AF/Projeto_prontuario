#esta file é o app principal do sistema de prontuário, onde estão as rotas e a lógica de autenticação

#este sistema funciona com um banco de dados onde somente o adimin pode criar os usuarios -
#onde no caso são os medicos da clinica, e os pacientes são adicionados por esses medicos,
# e os pacientes apenas podem ser exluidos pelo admin.

#abaixo encontramos as importações necessárias para o funcionamento do sistema
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import User, paciente

#inicializando o Flask, LoginManager e SQLAlchemy
app = Flask(__name__)
app.secret_key = 'dev'
lm = LoginManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data_sistem.db"
db.init_app(app)

# Configurando o LoginManager
@lm.user_loader
def load_user(id):
    usuario_logado = db.session.query(User).filter_by(id=id).first()
    return usuario_logado

#toda esta rota esta inativa pois foi apenas utilizada para criar o primeiro ususario do sistema o 'dev.admin'
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

#esta rota é a rota de login do sistema, onde o usuario pode se autenticar 
@app.route('/', methods=['GET', 'POST'])
def login():
# condição para caso nao seja enviado nenhuma requisição, ou seja, o usuario acessar a rota sem envio de dados
    if request.method == 'GET':
        return render_template('login.html')
#condição para caso seja enviado uma requisição POST, ou seja, o usuario enviar os dados de login
    if request.method == 'POST':
        crm = request.form['crm']
        senha = request.form['senha']
        usuario = db.session.query(User).filter_by(crm=crm).first()
        
#verifica se o usuario existe e se a senha está correta       
        if usuario and usuario.password == senha:
            login_user(usuario)
#caso o usuario autenticado seja o 'dev.admin', ele é redirecionado para a página de admin
            if current_user.nome == 'dev.admin':
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
# caso contrário, é redirecionado para a página principal
        else:
            flash('crm ou senha incorretos.')
            return redirect(url_for('login'))
        
#esta rota é a rota do adminstrador      
@app.route('/admin', methods=['GET', 'POST'])
#login required permite que apenas usuarios autenticados acessem a rota
@login_required
def admin():
#nao permite a entrada de usuarios que nao sejam o 'dev.admin' na rota de admin
    if current_user.nome != 'dev.admin':
        return redirect(url_for('index'))
#condição para caso seja enviado uma requisição GET, ou seja, o usuario acessar a rota sem envio de dados          
    elif request.method == 'GET': 
        usuarios_lista = db.session.query(User).all()
        pacientes_lista = db.session.query(paciente).all()
        return render_template("adm.html", usuarios_banco=usuarios_lista, pacientes_banco =pacientes_lista)
        
    
#condição para caso seja enviado uma requisição POST, ou seja, o usuario enviar os dados de criação de um novo usuario 
    elif request.method == 'POST':
         nome_usuario = request.form['nome']
         crm_usuario = request.form['crm']
         senha_usuario = request.form['senha']
         novo_user = User(nome=nome_usuario, crm=crm_usuario, password=senha_usuario)
         db.session.add(novo_user)
         db.session.commit()
    return redirect(url_for('admin'))
#rota especifica para a exclusão de usuarios medicos, onde o usuario é excluido do banco de dados
@app.route('/delete_medicos/<int:id>')
def delete_medicos(id):
    usuario = db.session.query(User).filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('admin'))
#rota especifica para a exclusão de pacientes, onde o paciente é excluido do banco de dados
@app.route('/delete_pacientes/<int:id>')
def delete_paciente(id):
    pacientes = db.session.query(paciente).filter_by(id=id).first()
    db.session.delete(pacientes)
    db.session.commit()
    return redirect(url_for('admin'))
    
#rota  da pagina prinicipal do sistema
@app.route('/pagina_principal', methods=['GET', 'POST'])
@login_required
def index():
    
    if request.method == 'GET':
        load_user(current_user.nome)
        pacientes_lista = db.session.query(paciente).all()
        return render_template('index.html', pacientes_consulta = pacientes_lista)
#condição para requisição POST, onde o usuario envia os dados de criação de um novo paciente   
    elif request.method == 'POST':
        nome_paciente = request.form['nome']
        idade_paciente = request.form['idade']
        sexo_paciente = request.form['sexo']
        descricao_paciente = request.form['descricao']
        novo_paciente = paciente(nome = nome_paciente, idade = idade_paciente, sexo = sexo_paciente, descricao = descricao_paciente)
        db.session.add(novo_paciente)
        db.session.commit()
        login_user(novo_paciente)
        
    return redirect(url_for('index'))

#rota de logout do sistema, onde o usuario é deslogado e redirecionado para a página de login
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




#esse if roda o debug do flask, e caso nao exista o banco de dados, ele cria um novo
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)