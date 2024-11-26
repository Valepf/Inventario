# Backend/api/routes/orden_compra.py
from flask import Blueprint, request, jsonify
from api.models.orden_compra import OrdenCompra
from api.db.db_config import DBError

orden_compra_bp = Blueprint('orden_compra_bp', __name__)

@orden_compra_bp.route('/ordenes_compra', methods=['GET'])
def obtener_ordenes_compra():
    try:
        ordenes = OrdenCompra.obtener_todas_ordenes()
        return jsonify(ordenes), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": e.args[0]}), 400

@orden_compra_bp.route('/orden_compra', methods=['POST'])
def crear_orden_compra():
    data = request.get_json()
    try:
        orden = OrdenCompra.crear_orden(data)
        return jsonify(orden), 201
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": e.args[0]}), 400

@orden_compra_bp.route('/orden_compra/<int:id>', methods=['GET'])
def obtener_orden_compra(id):
    try:
        orden = OrdenCompra.obtener_orden(id)
        return jsonify(orden), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": e.args[0]}), 400

@orden_compra_bp.route('/orden_compra/<int:id>', methods=['PUT'])
def actualizar_orden_compra(id):
    data = request.get_json()
    try:
        orden = OrdenCompra.actualizar_orden(id, data)
        return jsonify(orden), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": e.args[0]}), 400

@orden_compra_bp.route('/orden_compra/<int:id>', methods=['DELETE'])
def eliminar_orden_compra(id):
    try:
        respuesta = OrdenCompra.eliminar_orden(id)
        return jsonify(respuesta), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": e.args[0]}), 400
