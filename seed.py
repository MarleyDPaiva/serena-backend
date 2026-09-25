from app import create_app
from app.extensions import db
from app.models import Especialidade

app = create_app()

especialidades = [
    "Terapia Cognitivo-Comportamental",
    "Psicanálise",
    "Terapia Familiar",
    "Psicologia Infantil",
    "Ansiedade e Pânico",
    "Dependência Química",
]

with app.app_context():
    for nome in especialidades:
        if not Especialidade.query.filter_by(nome=nome).first():
            db.session.add(Especialidade(nome=nome))
    db.session.commit()
    print("Especialidades cadastradas com sucesso.")