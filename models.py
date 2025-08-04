from db import db
from flask_login import UserMixin
 
class User(UserMixin, db.Model):
    __tablename__ = 'medicos_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    crm = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
class paciente(UserMixin, db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.String(3), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)