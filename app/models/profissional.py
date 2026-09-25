from app.extensions import db
from app.models.especialidade import profissional_especialidades
from datetime import datetime

class Profissional(db.Model):
    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    crp = db.Column(db.String(20), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    valor_consulta = db.Column(db.Numeric(10, 2))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    consultas = db.relationship("Consulta", backref="profissional", cascade="all, delete-orphan")
    especialidades = db.relationship(
        "Especialidade",
        secondary=profissional_especialidades,
        backref="profissionais"
    )
