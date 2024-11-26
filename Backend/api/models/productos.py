from api.db.db_config import get_db_connection, DBError

class Producto():
    schema = {
        "nombre": str,
        "descripcion": str,
        "precio": float,
        "cantidad_en_stock": int,
        "categoria_id": int,
        "proveedor_id": int
    }

    @classmethod
    def validate(cls, data):
        if data is None or type(data) != dict:
            return False
        # Control: data contiene todas las claves?
        for key in cls.schema:
            if key not in data:
                return False
            # Control: cada valor es del tipo correcto?
            if type(data[key]) != cls.schema[key]:
                return False
        return True

    def __init__(self, data):
        self._id = data[0]
        self._nombre = data[1]
        self._descripcion = data[2]
        self._precio = data[3]
        self._cantidad_en_stock = data[4]
        self._categoria_id = data[5]
        self._proveedor_id = data[6]

    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "precio": self._precio,
            "cantidad_en_stock": self._cantidad_en_stock,
            "categoria_id": self._categoria_id,
            "proveedor_id": self._proveedor_id
        }

    @classmethod
    def obtener_todos_productos(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM productos')
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if len(data) > 0:
            productos = []
            for row in data:
                producto = Producto(row).to_json()
                productos.append(producto)
            return productos

        raise DBError("No existen productos disponibles")

    @classmethod
    def crear_producto(cls, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO productos (nombre, descripcion, precio, cantidad_en_stock, categoria_id, proveedor_id) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (data["nombre"], data["descripcion"], data["precio"], data["cantidad_en_stock"], data["categoria_id"], data["proveedor_id"]))
        connection.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]

        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        nuevo_producto = cursor.fetchone()

        cursor.close()
        connection.close()

        return Producto(nuevo_producto).to_json()

    @classmethod
    def actualizar_producto(cls, id, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe el producto solicitado")

        cursor.execute('UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, cantidad_en_stock = %s, categoria_id = %s, proveedor_id = %s WHERE id = %s', 
                       (data["nombre"], data["descripcion"], data["precio"], data["cantidad_en_stock"], data["categoria_id"], data["proveedor_id"], id))
        connection.commit()

        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        producto_actualizado = cursor.fetchone()

        cursor.close()
        connection.close()

        return Producto(producto_actualizado).to_json()

    @classmethod
    def eliminar_producto(cls, id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        connection.close()

        if rowcount > 0:
            return {"id elemento eliminado": id}

        raise DBError("No existe el recurso solicitado")
