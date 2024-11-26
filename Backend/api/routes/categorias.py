from flask import Blueprint, request, jsonify
from Backend.api.utils.security import token_required
from api.db.db_config import get_db_connection

categoria_bp = Blueprint('categoria_bp', __name__)

# Ruta para obtener todas las categorías
@categoria_bp.route('/categorias/<int:id_user>', methods=['GET'])
@token_required
def get_categorias(id_user):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM categories')
    categorias = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({"categorias": categorias})

# Ruta para crear una nueva categoría
@categoria_bp.route('/categorias/<int:id_user>', methods=['POST'])
@token_required
def crear_categoria(id_user):
    data = request.get_json()

    name = data['name']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO categories (name)
        VALUES (%s)
    ''', (name,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Categoría creada con éxito."}), 201
