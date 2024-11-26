from flask import Blueprint, request, jsonify
from Backend.api.utils.security import token_required
from api.db.db_config import get_db_connection

proveedor_bp = Blueprint('proveedor_bp', __name__)

# Ruta para obtener todos los proveedores
@proveedor_bp.route('/proveedores/<int:id_user>', methods=['GET'])
@token_required
def get_proveedores(id_user):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM suppliers')
    proveedores = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({"proveedores": proveedores})

# Ruta para agregar un nuevo proveedor
@proveedor_bp.route('/proveedores/<int:id_user>', methods=['POST'])
@token_required
def crear_proveedor(id_user):
    data = request.get_json()

    name = data['name']
    contact_email = data.get('contact_email')
    contact_phone = data.get('contact_phone')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO suppliers (name, contact_email, contact_phone)
        VALUES (%s, %s, %s)
    ''', (name, contact_email, contact_phone))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Proveedor creado con éxito."}), 201
