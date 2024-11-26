from flask import request, jsonify, current_app
import jwt
from functools import wraps

# Función decoradora que verifica que el usuario tenga un token válido para acceder a rutas protegidas
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        # La solicitud debe incluir una cabecera 'x-access-token' con el token
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({"message": "Falta el token"}), 401
        
        id_user = kwargs.get('id_user') or request.headers.get('id_user')
        if id_user is None:
            return jsonify({"message": "Falta el usuario"}), 401

        # Decodificar el token para verificar el id del usuario
        try:
            # Usar la configuración de Flask directamente
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            token_id = data['id']  # ID del usuario en el token

            if int(id_user) != int(token_id):
                return jsonify({"message": "No tienes permiso para acceder a este recurso"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        # Si el token es válido, permitir la ejecución de la ruta
        return func(*args, **kwargs)

    return decorated


