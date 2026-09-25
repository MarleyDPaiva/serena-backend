from app.extensions import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = "consultas"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey("profissionais.id", ondelete="CASCADE"), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao_minutos = db.Column(db.Integer, default=50)
    status = db.Column(db.String(20), nullable=False, default="agendada")
    valor = db.Column(db.Numeric(10, 2))
    observacoes = db.Column(db.Text)
    anotacoes_privadas = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)