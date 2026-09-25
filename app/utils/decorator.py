from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required

def tipo_requerido(*tipos_permitidos):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("tipo") not in tipos_permitidos:
                return jsonify({"erro": "Acesso não autorizado para este tipo de usuário"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator