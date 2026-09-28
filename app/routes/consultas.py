from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Consulta, Paciente, Profissional
from app.utils.decorators import tipo_requerido
from flask_jwt_extended import get_jwt, get_jwt_identity
from datetime import datetime

consultas_bp = Blueprint("consultas", __name__)


@consultas_bp.route("", methods=["POST"])
@tipo_requerido("paciente")
def criar_consulta():
    usuario_id = get_jwt_identity()
    paciente = Paciente.query.filter_by(usuario_id=usuario_id).first()

    if not paciente:
        return jsonify({"erro": "Perfil de paciente não encontrado"}), 404

    dados = request.get_json()
    profissional_id = dados.get("profissional_id")
    data_hora_str = dados.get("data_hora")  # formato ISO: "2026-10-01T14:00:00"

    if not profissional_id or not data_hora_str:
        return jsonify({"erro": "profissional_id e data_hora são obrigatórios"}), 400

    profissional = Profissional.query.get(profissional_id)
    if not profissional or not profissional.ativo:
        return jsonify({"erro": "Profissional não encontrado ou inativo"}), 404

    try:
        data_hora = datetime.fromisoformat(data_hora_str)
    except ValueError:
        return jsonify({"erro": "data_hora inválida, use formato ISO 8601"}), 400

    if data_hora < datetime.now():
        return jsonify({"erro": "Não é possível agendar em uma data no passado"}), 400

    # Checa conflito de horário manualmente (já que não usamos a exclusion constraint)
    duracao = dados.get("duracao_minutos", 50)
    conflito = Consulta.query.filter(
        Consulta.profissional_id == profissional_id,
        Consulta.status != "cancelada",
        Consulta.data_hora == data_hora
    ).first()

    if conflito:
        return jsonify({"erro": "Este profissional já tem uma consulta nesse horário"}), 409

    consulta = Consulta(
        paciente_id=paciente.id,
        profissional_id=profissional_id,
        data_hora=data_hora,
        duracao_minutos=duracao,
        valor=dados.get("valor", profissional.valor_consulta),
        observacoes=dados.get("observacoes"),
        status="agendada",
    )

    db.session.add(consulta)
    db.session.commit()

    return jsonify({"mensagem": "Consulta agendada com sucesso", "consulta_id": consulta.id}), 201


@consultas_bp.route("", methods=["GET"])
@tipo_requerido("paciente", "profissional")
def listar_consultas():
    usuario_id = get_jwt_identity()
    tipo = get_jwt().get("tipo")

    if tipo == "paciente":
        paciente = Paciente.query.filter_by(usuario_id=usuario_id).first()
        consultas = Consulta.query.filter_by(paciente_id=paciente.id).order_by(Consulta.data_hora).all()
    else:
        profissional = Profissional.query.filter_by(usuario_id=usuario_id).first()
        consultas = Consulta.query.filter_by(profissional_id=profissional.id).order_by(Consulta.data_hora).all()

    resultado = [{
        "id": c.id,
        "data_hora": c.data_hora.isoformat(),
        "duracao_minutos": c.duracao_minutos,
        "status": c.status,
        "valor": float(c.valor) if c.valor else None,
        "observacoes": c.observacoes,
        "paciente": c.paciente.nome_completo,
        "profissional": c.profissional.nome_completo,
    } for c in consultas]

    return jsonify(resultado), 200


@consultas_bp.route("/<int:consulta_id>", methods=["GET"])
@tipo_requerido("paciente", "profissional")
def obter_consulta(consulta_id):
    consulta = Consulta.query.get(consulta_id)
    if not consulta:
        return jsonify({"erro": "Consulta não encontrada"}), 404

    if not _usuario_pode_acessar(consulta):
        return jsonify({"erro": "Você não tem permissão para ver esta consulta"}), 403

    dados = {
        "id": consulta.id,
        "data_hora": consulta.data_hora.isoformat(),
        "status": consulta.status,
        "valor": float(consulta.valor) if consulta.valor else None,
        "observacoes": consulta.observacoes,
        "paciente": consulta.paciente.nome_completo,
        "profissional": consulta.profissional.nome_completo,
    }

    # anotações privadas só aparecem pro profissional dono da consulta
    tipo = get_jwt().get("tipo")
    if tipo == "profissional":
        dados["anotacoes_privadas"] = consulta.anotacoes_privadas

    return jsonify(dados), 200


@consultas_bp.route("/<int:consulta_id>/status", methods=["PATCH"])
@tipo_requerido("paciente", "profissional")
def atualizar_status(consulta_id):
    consulta = Consulta.query.get(consulta_id)
    if not consulta:
        return jsonify({"erro": "Consulta não encontrada"}), 404

    if not _usuario_pode_acessar(consulta):
        return jsonify({"erro": "Você não tem permissão para alterar esta consulta"}), 403

    dados = request.get_json()
    novo_status = dados.get("status")

    tipo = get_jwt().get("tipo")
    transicoes_permitidas = {
        "paciente": {"cancelada"},
        "profissional": {"confirmada", "realizada", "cancelada", "faltou"},
    }

    if novo_status not in transicoes_permitidas.get(tipo, set()):
        return jsonify({"erro": f"'{tipo}' não pode alterar status para '{novo_status}'"}), 403

    consulta.status = novo_status
    if tipo == "profissional" and "anotacoes_privadas" in dados:
        consulta.anotacoes_privadas = dados["anotacoes_privadas"]

    db.session.commit()
    return jsonify({"mensagem": "Status atualizado", "status": consulta.status}), 200


def _usuario_pode_acessar(consulta):
    usuario_id = get_jwt_identity()
    tipo = get_jwt().get("tipo")

    if tipo == "paciente":
        return consulta.paciente.usuario_id == int(usuario_id)
    else:
        return consulta.profissional.usuario_id == int(usuario_id)