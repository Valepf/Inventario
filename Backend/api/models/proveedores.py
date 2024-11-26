from api.db.db_config import get_db_connection, DBError

class Proveedor():
    schema = {
        "nombre": str,
        "contacto": str
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
        self._nombre = data[1]
        self._contacto = data[2]

    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "contacto": self._contacto
        }

    @classmethod
    def obtener_todos_proveedores(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM proveedores')
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if len(data) > 0:
            proveedores = []
            for row in data:
                proveedor = Proveedor(row).to_json()
                proveedores.append(proveedor)
            return proveedores

        raise DBError("No existen proveedores disponibles")

    @classmethod
    def crear_proveedor(cls, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO proveedores (nombre, contacto) VALUES (%s, %s)', 
                       (data["nombre"], data["contacto"]))
        connection.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]

        cursor.execute('SELECT * FROM proveedores WHERE id = %s', (id,))
        nuevo_proveedor = cursor.fetchone()

        cursor.close()
        connection.close()

        return Proveedor(nuevo_proveedor).to_json()

    @classmethod
    def actualizar_proveedor(cls, id, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM proveedores WHERE id = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe el proveedor solicitado")

        cursor.execute('UPDATE proveedores SET nombre = %s, contacto = %s WHERE id = %s', 
                       (data["nombre"], data["contacto"], id))
        connection.commit()

        cursor.execute('SELECT * FROM proveedores WHERE id = %s', (id,))
        proveedor_actualizado = cursor.fetchone()

        cursor.close()
        connection.close()

        return Proveedor(proveedor_actualizado).to_json()

    @classmethod
    def eliminar_proveedor(cls, id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        connection.close()

        if rowcount > 0:
            return {"id elemento eliminado": id}

        raise DBError("No existe el recurso solicitado")
