# main.py
from flask import jsonify
from Backend.api import create_app

# Crear la aplicación utilizando la fábrica de aplicaciones
app = create_app()

# Ruta de prueba
@app.route('/')
def test():
    return jsonify({"message": "Sistema de gestión de inventario en funcionamiento"})

# Ejecutar la aplicación en modo de desarrollo
if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)

