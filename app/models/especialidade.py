from app.extensions import db

# Tabela associativa N:N (não precisa virar uma classe própria,
# só usamos pra declarar o relationship "secondary" abaixo)
profissional_especialidades = db.Table(
    "profissional_especialidades",
    db.Column("profissional_id", db.Integer, db.ForeignKey("profissionais.id", ondelete="CASCADE"), primary_key=True),
    db.Column("especialidade_id", db.Integer, db.ForeignKey("especialidades.id", ondelete="CASCADE"), primary_key=True),
)

class Especialidade(db.Model):
    __tablename__ = "especialidades"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)