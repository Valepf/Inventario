from api.db.db_config import get_db_connection, DBError
from datetime import datetime

class OrdenCompra():
    schema = {
        "producto_id": int,
        "cantidad": int,
        "fecha_pedido": str,  # Formato: YYYY-MM-DD
        "fecha_recepcion": str,  # Formato: YYYY-MM-DD
        "estado": str  # 'pendiente', 'completada', 'cancelada'
    }

    @classmethod
    def validate(cls, data):
        if data is None or type(data) != dict:
            return False
        for key in cls.schema:
            if key not in data:
                return False
            if type(data[key]) != cls.schema[key]:
                return False
        return True

    def __init__(self, data):
        self._id = data[0]
        self._producto_id = data[1]
        self._cantidad = data[2]
        self._fecha_pedido = data[3]
        self._fecha_recepcion = data[4]
        self._estado = data[5]

    def to_json(self):
        return {
            "id": self._id,
            "producto_id": self._producto_id,
            "cantidad": self._cantidad,
            "fecha_pedido": self._fecha_pedido,
            "fecha_recepcion": self._fecha_recepcion,
            "estado": self._estado
        }

    @classmethod
    def obtener_todas_ordenes(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM ordenes_compra')
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if len(data) > 0:
            ordenes = []
            for row in data:
                orden = OrdenCompra(row).to_json()
                ordenes.append(orden)
            return ordenes

        raise DBError("No existen órdenes de compra disponibles")

    @classmethod
    def crear_orden(cls, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO ordenes_compra (producto_id, cantidad, fecha_pedido, fecha_recepcion, estado) VALUES (%s, %s, %s, %s, %s)', 
                       (data["producto_id"], data["cantidad"], data["fecha_pedido"], data["fecha_recepcion"], data["estado"]))
        connection.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]

        cursor.execute('SELECT * FROM ordenes_compra WHERE id = %s', (id,))
        nueva_orden = cursor.fetchone()

        cursor.close()
        connection.close()

        return OrdenCompra(nueva_orden).to_json()

    @classmethod
    def actualizar_orden(cls, id, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM ordenes_compra WHERE id = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe la orden de compra solicitada")

        cursor.execute('UPDATE ordenes_compra SET producto_id = %s, cantidad = %s, fecha_pedido = %s, fecha_recepcion = %s, estado = %s WHERE id = %s', 
                       (data["producto_id"], data["cantidad"], data["fecha_pedido"], data["fecha_recepcion"], data["estado"], id))
        connection.commit()

        cursor.execute('SELECT * FROM ordenes_compra WHERE id = %s', (id,))
        orden_actualizada = cursor.fetchone()

        cursor.close()
        connection.close()

        return OrdenCompra(orden_actualizada).to_json()

    @classmethod
    def eliminar_orden(cls, id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ordenes_compra WHERE id = %s', (id,))
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        connection.close()

        if rowcount > 0:
            return {"id elemento eliminado": id}

        raise DBError("No existe el recurso solicitado")
