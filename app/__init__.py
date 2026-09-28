from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, bcrypt, jwt
from app.routes.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # em produção, restrinja: CORS(app, origins=["https://seu-dominio.com"])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app import models  # noqa: F401

    from app.routes.auth import auth_bp
    from app.routes.pacientes import pacientes_bp
    from app.routes.profissionais import profissionais_bp
    from app.routes.consultas import consultas_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(pacientes_bp, url_prefix="/api/pacientes")
    app.register_blueprint(profissionais_bp, url_prefix="/api/profissionais")
    app.register_blueprint(consultas_bp, url_prefix="/api/consultas")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"erro": "Rota não encontrada"}), 404

    @app.errorhandler(500)
    def erro_interno(e):
        db.session.rollback()
        return jsonify({"erro": "Erro interno do servidor"}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "servico": "Serena API"}), 200

    return app