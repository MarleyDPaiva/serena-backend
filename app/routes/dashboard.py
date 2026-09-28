from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Consulta, Paciente, Profissional
from app.utils.decorators import tipo_requerido
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/resumo", methods=["GET"])
@tipo_requerido("profissional")
def resumo_profissional():
    usuario_id = get_jwt_identity()
    profissional = Profissional.query.filter_by(usuario_id=usuario_id).first()

    if not profissional:
        return jsonify({"erro": "Perfil não encontrado"}), 404

    agora = datetime.now()
    daqui_7_dias = agora + timedelta(days=7)

    proximas_consultas = Consulta.query.filter(
        Consulta.profissional_id == profissional.id,
        Consulta.data_hora >= agora,
        Consulta.data_hora <= daqui_7_dias,
        Consulta.status.in_(["agendada", "confirmada"]),
    ).order_by(Consulta.data_hora).all()

    total_pacientes = db.session.query(
        func.count(func.distinct(Consulta.paciente_id))
    ).filter(Consulta.profissional_id == profissional.id).scalar()

    total_consultas_realizadas = Consulta.query.filter_by(
        profissional_id=profissional.id, status="realizada"
    ).count()

    return jsonify({
        "total_pacientes": total_pacientes or 0,
        "total_consultas_realizadas": total_consultas_realizadas,
        "proximas_consultas": [{
            "id": c.id,
            "data_hora": c.data_hora.isoformat(),
            "paciente": c.paciente.nome_completo,
            "status": c.status,
        } for c in proximas_consultas],
    }), 200


@dashboard_bp.route("/pacientes", methods=["GET"])
@tipo_requerido("profissional")
def meus_pacientes():
    usuario_id = get_jwt_identity()
    profissional = Profissional.query.filter_by(usuario_id=usuario_id).first()

    if not profissional:
        return jsonify({"erro": "Perfil não encontrado"}), 404

    # Pacientes distintos que já tiveram consulta com esse profissional
    pacientes = (
        db.session.query(Paciente)
        .join(Consulta, Consulta.paciente_id == Paciente.id)
        .filter(Consulta.profissional_id == profissional.id)
        .distinct()
        .all()
    )

    resultado = []
    for p in pacientes:
        total_consultas = Consulta.query.filter_by(
            paciente_id=p.id, profissional_id=profissional.id
        ).count()

        ultima_consulta = (
            Consulta.query.filter_by(paciente_id=p.id, profissional_id=profissional.id)
            .order_by(Consulta.data_hora.desc())
            .first()
        )

        resultado.append({
            "id": p.id,
            "nome_completo": p.nome_completo,
            "telefone": p.telefone,
            "total_consultas": total_consultas,
            "ultima_consulta": ultima_consulta.data_hora.isoformat() if ultima_consulta else None,
        })

    return jsonify(resultado), 200


@dashboard_bp.route("/pacientes/<int:paciente_id>", methods=["GET"])
@tipo_requerido("profissional")
def detalhe_paciente(paciente_id):
    usuario_id = get_jwt_identity()
    profissional = Profissional.query.filter_by(usuario_id=usuario_id).first()

    # Garante que esse paciente realmente já consultou com esse profissional
    tem_consulta = Consulta.query.filter_by(
        paciente_id=paciente_id, profissional_id=profissional.id
    ).first()

    if not tem_consulta:
        return jsonify({"erro": "Paciente não encontrado ou sem consultas com você"}), 404

    paciente = Paciente.query.get(paciente_id)

    consultas = (
        Consulta.query.filter_by(paciente_id=paciente_id, profissional_id=profissional.id)
        .order_by(Consulta.data_hora.desc())
        .all()
    )

    return jsonify({
        "id": paciente.id,
        "nome_completo": paciente.nome_completo,
        "telefone": paciente.telefone,
        "data_nascimento": paciente.data_nascimento.isoformat() if paciente.data_nascimento else None,
        "genero": paciente.genero,
        "consultas": [{
            "id": c.id,
            "data_hora": c.data_hora.isoformat(),
            "status": c.status,
            "anotacoes_privadas": c.anotacoes_privadas,
            "observacoes": c.observacoes,
        } for c in consultas],
    }), 200