import os
from flask import Flask
from flask_mysqldb import MySQL

# Configuración de la aplicación y la base de datos
def create_app():
    app = Flask(__name__)

    # Configuración de conexión a la base de datos
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')  # 'localhost' como valor por defecto
    app.config['MYSQL_USER'] = os.getenv('DB_USER', 'user_api_inventario')  # Usuario creado
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'secure_password_123')  # Contraseña segura
    app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'db_api_inventario')  # Nombre de la base de datos
    app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))  # Puerto por defecto 3306

    mysql = MySQL(app)
    
    return app, mysql

class DBError(Exception):
    """Clase para manejar errores personalizados de la base de datos."""
    pass

