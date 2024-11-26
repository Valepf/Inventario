# Backend/api/__init__.py
from flask import Flask
from Backend.api.routes.productos import producto_bp

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia esto por tu clave secreta real

    # Registrar el blueprint de productos
    app.register_blueprint(producto_bp, url_prefix='/api')

    return app



