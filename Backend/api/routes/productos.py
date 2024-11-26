# Backend/api/routes/productos.py
from flask import Blueprint, request, jsonify
from Backend.api.utils.security import token_required
from api.db.db_config import get_db_connection

producto_bp = Blueprint('producto_bp', __name__)

# Helper function to format product rows into dictionaries
def format_product(product):
    return {
        "id": product[0],
        "name": product[1],
        "price": product[2],
        "stock": product[3],
        "category_id": product[4],
        "id_user": product[5]
    }

# Ruta para obtener todos los productos
@producto_bp.route('/productos/<int:id_user>', methods=['GET'])
@token_required
def get_productos(id_user):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM products WHERE id_user = %s', (id_user,))
        productos = cursor.fetchall()
        cursor.close()
        connection.close()

        # Format the data before returning
        formatted_products = [format_product(prod) for prod in productos]
        return jsonify({"productos": formatted_products})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para crear un nuevo producto
@producto_bp.route('/productos/<int:id_user>', methods=['POST'])
@token_required
def crear_producto(id_user):
    try:
        data = request.get_json()

        name = data['name']
        price = data['price']
        stock = data['stock']
        category_id = data['category_id']

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO products (name, price, stock, category_id, id_user)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, price, stock, category_id, id_user))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Producto creado con éxito."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un producto
@producto_bp.route('/productos/<int:id_user>/<int:product_id>', methods=['PUT'])
@token_required
def actualizar_producto(id_user, product_id):
    try:
        data = request.get_json()

        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        category_id = data.get('category_id')

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''
            UPDATE products
            SET name = %s, price = %s, stock = %s, category_id = %s
            WHERE id = %s AND id_user = %s
        ''', (name, price, stock, category_id, product_id, id_user))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Producto actualizado con éxito."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un producto
@producto_bp.route('/productos/<int:id_user>/<int:product_id>', methods=['DELETE'])
@token_required
def eliminar_producto(id_user, product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''
            DELETE FROM products WHERE id = %s AND id_user = %s
        ''', (product_id, id_user))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Producto eliminado con éxito."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

