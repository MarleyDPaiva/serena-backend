from app.extensions import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    paciente = db.relationship("Paciente", backref="usuario", uselist=False, cascade="all, delete-orphan")
    profissional = db.relationship("Profissional", backref="usuario", uselist=False, cascade="all, delete-orphan")

