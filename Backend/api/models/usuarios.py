from api.db.db_config import get_db_connection, DBError

class Usuario():
    schema = {
        "nombre": str,
        "email": str,
        "contraseña": str,
        "rol": str  # 'admin' o 'usuario'
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
        self._email = data[2]
        self._contraseña = data[3]
        self._rol = data[4]

    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "email": self._email,
            "rol": self._rol
        }

    @classmethod
    def obtener_todos_usuarios(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM usuarios')
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if len(data) > 0:
            usuarios = []
            for row in data:
                usuario = Usuario(row).to_json()
                usuarios.append(usuario)
            return usuarios

        raise DBError("No existen usuarios disponibles")

    @classmethod
    def crear_usuario(cls, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)', 
                       (data["nombre"], data["email"], data["contraseña"], data["rol"]))
        connection.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]

        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        nuevo_usuario = cursor.fetchone()

        cursor.close()
        connection.close()

        return Usuario(nuevo_usuario).to_json()

    @classmethod
    def actualizar_usuario(cls, id, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        row = cursor.fetchone()

        if row is None:
            raise DBError("No existe el usuario solicitado")

        cursor.execute('UPDATE usuarios SET nombre = %s, email = %s, contraseña = %s, rol = %s WHERE id = %s', 
                       (data["nombre"], data["email"], data["contraseña"], data["rol"], id))
        connection.commit()

        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        usuario_actualizado = cursor.fetchone()

        cursor.close()
        connection.close()

        return Usuario(usuario_actualizado).to_json()

    @classmethod
    def eliminar_usuario(cls, id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        connection.close()

        if rowcount > 0:
            return {"id elemento eliminado": id}

        raise DBError("No existe el recurso solicitado")
