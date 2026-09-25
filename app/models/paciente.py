from app.extensions import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    data_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20))
    genero = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    consultas = db.relationship("Consulta", backref="paciente", cascade="all, delete-orphan")


