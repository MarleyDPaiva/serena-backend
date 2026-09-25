from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Paciente
from app.utils.decorator import tipo_requerido
from flask_jwt_extended import get_jwt_identity

pacientes_bp = Blueprint("pacientes", __name__)


@pacientes_bp.route("/perfil", methods=["GET"])
@tipo_requerido("paciente")
def meu_perfil():
    usuario_id = get_jwt_identity()
    paciente = Paciente.query.filter_by(usuario_id=usuario_id).first()

    if not paciente:
        return jsonify({"erro": "Perfil não encontrado"}), 404

    return jsonify({
        "id": paciente.id,
        "nome_completo": paciente.nome_completo,
        "cpf": paciente.cpf,
        "data_nascimento": paciente.data_nascimento.isoformat() if paciente.data_nascimento else None,
        "telefone": paciente.telefone,
        "genero": paciente.genero,
        "endereco": paciente.endereco,
    }), 200


@pacientes_bp.route("/perfil", methods=["PUT"])
@tipo_requerido("paciente")
def atualizar_perfil():
    usuario_id = get_jwt_identity()
    paciente = Paciente.query.filter_by(usuario_id=usuario_id).first()

    if not paciente:
        return jsonify({"erro": "Perfil não encontrado"}), 404

    dados = request.get_json()
    campos_editaveis = ["nome_completo", "telefone", "genero", "endereco", "data_nascimento"]

    for campo in campos_editaveis:
        if campo in dados:
            setattr(paciente, campo, dados[campo])

    db.session.commit()
    return jsonify({"mensagem": "Perfil atualizado com sucesso"}), 200