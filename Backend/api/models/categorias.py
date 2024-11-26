from api.db.db_config import get_db_connection, DBError

class Categorias():
    schema = {
        "nombre": str,
        "descripcion": str
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
        self._descripcion = data[2]

    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "descripcion": self._descripcion
        }

    @classmethod
    def obtener_todas_categorias(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categorias')
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if len(data) > 0:
            categorias = []
            for row in data:
                categoria = Categorias(row).to_json()
                categorias.append(categoria)
            return categorias

        raise DBError("No existen categorías disponibles")

    @classmethod
    def crear_categoria(cls, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)', 
                       (data["nombre"], data["descripcion"]))
        connection.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]

        cursor.execute('SELECT * FROM categorias WHERE id = %s', (id,))
        nueva_categoria = cursor.fetchone()

        cursor.close()
        connection.close()

        return Categorias(nueva_categoria).to_json()

    @classmethod
    def actualizar_categoria(cls, id, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM categorias WHERE id = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe la categoría solicitada")

        cursor.execute('UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s', 
                       (data["nombre"], data["descripcion"], id))
        connection.commit()

        cursor.execute('SELECT * FROM categorias WHERE id = %s', (id,))
        categoria_actualizada = cursor.fetchone()

        cursor.close()
        connection.close()

        return Categorias(categoria_actualizada).to_json()

    @classmethod
    def eliminar_categoria(cls, id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM categorias WHERE id = %s', (id,))
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        connection.close()

        if rowcount > 0:
            return {"id elemento eliminado": id}

        raise DBError("No existe el recurso solicitado")
