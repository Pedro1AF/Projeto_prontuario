from db import db
from flask_login import UserMixin
 
class User(UserMixin, db.Model):
    __tablename__ = 'medicos_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    crm = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)