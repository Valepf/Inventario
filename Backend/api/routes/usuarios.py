from flask import Blueprint, request, jsonify
from api.db.db_config import get_db_connection
from Backend.api.utils.security import token_required
import bcrypt
import jwt

usuario_bp = Blueprint('usuario_bp', __name__)

# Ruta para crear un nuevo usuario (registrarse)
@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    username = data['username']
    password = data['password']
    email = data['email']

    # Hash de la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO users (username, password, email)
        VALUES (%s, %s, %s)
    ''', (username, hashed_password, email))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Usuario creado con éxito."}), 201

# Ruta para el login (autenticación)
@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # Verificar contraseña
        # Generar token
        token = jwt.encode({'id': user[0]}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401
