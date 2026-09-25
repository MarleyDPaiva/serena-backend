from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models import Usuario, Paciente, Profissional
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["POST"])
def registro():
    dados = request.get_json()

    campos_obrigatorios = ["email", "senha", "tipo", "nome_completo"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios: email, senha, tipo, nome_completo"}), 400

    if dados["tipo"] not in ("paciente", "profissional"):
        return jsonify({"erro": "tipo deve ser 'paciente' ou 'profissional'"}), 400

    if Usuario.query.filter_by(email=dados["email"]).first():
        return jsonify({"erro": "E-mail já cadastrado"}), 409

    senha_hash = bcrypt.generate_password_hash(dados["senha"]).decode("utf-8")

    try:
        usuario = Usuario(email=dados["email"], senha_hash=senha_hash, tipo=dados["tipo"])
        db.session.add(usuario)
        db.session.flush()  # gera o usuario.id sem precisar commitar ainda

        if dados["tipo"] == "paciente":
            perfil = Paciente(
                usuario_id=usuario.id,
                nome_completo=dados["nome_completo"],
                cpf=dados.get("cpf"),
                data_nascimento=dados.get("data_nascimento"),
                telefone=dados.get("telefone"),
            )
        else:
            if not dados.get("crp"):
                return jsonify({"erro": "crp é obrigatório para profissionais"}), 400
            perfil = Profissional(
                usuario_id=usuario.id,
                nome_completo=dados["nome_completo"],
                crp=dados["crp"],
                telefone=dados.get("telefone"),
                bio=dados.get("bio"),
                valor_consulta=dados.get("valor_consulta"),
            )

        db.session.add(perfil)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha ao registrar usuário", "detalhe": str(e)}), 500

    return jsonify({"mensagem": "Usuário registrado com sucesso", "usuario_id": usuario.id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    email = dados.get("email")
    senha = dados.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not bcrypt.check_password_hash(usuario.senha_hash, senha):
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

    if not usuario.ativo:
        return jsonify({"erro": "Usuário inativo"}), 403

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"tipo": usuario.tipo}
    )

    return jsonify({"access_token": token, "tipo": usuario.tipo}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "ativo": usuario.ativo,
    }), 200