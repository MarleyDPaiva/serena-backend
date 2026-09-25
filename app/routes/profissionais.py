from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Profissional, Especialidade
from app.utils.decorator import tipo_requerido
from flask_jwt_extended import get_jwt_identity

profissionais_bp = Blueprint("profissionais", __name__)


@profissionais_bp.route("", methods=["GET"])
def listar_profissionais():
    """Rota pública — pacientes navegam aqui antes de agendar."""
    especialidade_id = request.args.get("especialidade_id", type=int)

    query = Profissional.query.filter_by(ativo=True)
    if especialidade_id:
        query = query.join(Profissional.especialidades).filter(Especialidade.id == especialidade_id)

    profissionais = query.all()

    resultado = [{
        "id": p.id,
        "nome_completo": p.nome_completo,
        "crp": p.crp,
        "bio": p.bio,
        "valor_consulta": float(p.valor_consulta) if p.valor_consulta else None,
        "especialidades": [e.nome for e in p.especialidades],
    } for p in profissionais]

    return jsonify(resultado), 200


@profissionais_bp.route("/<int:profissional_id>", methods=["GET"])
def obter_profissional(profissional_id):
    """Também pública — detalhe de um profissional específico."""
    p = Profissional.query.get(profissional_id)
    if not p or not p.ativo:
        return jsonify({"erro": "Profissional não encontrado"}), 404

    return jsonify({
        "id": p.id,
        "nome_completo": p.nome_completo,
        "crp": p.crp,
        "bio": p.bio,
        "telefone": p.telefone,
        "valor_consulta": float(p.valor_consulta) if p.valor_consulta else None,
        "especialidades": [e.nome for e in p.especialidades],
    }), 200


@profissionais_bp.route("/perfil", methods=["PUT"])
@tipo_requerido("profissional")
def atualizar_perfil():
    usuario_id = get_jwt_identity()
    profissional = Profissional.query.filter_by(usuario_id=usuario_id).first()

    if not profissional:
        return jsonify({"erro": "Perfil não encontrado"}), 404

    dados = request.get_json()
    campos_editaveis = ["nome_completo", "telefone", "bio", "valor_consulta"]

    for campo in campos_editaveis:
        if campo in dados:
            setattr(profissional, campo, dados[campo])

    if "especialidade_ids" in dados:
        especialidades = Especialidade.query.filter(Especialidade.id.in_(dados["especialidade_ids"])).all()
        profissional.especialidades = especialidades

    db.session.commit()
    return jsonify({"mensagem": "Perfil atualizado com sucesso"}), 200