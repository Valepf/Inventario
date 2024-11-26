from flask import Flask
from flask_mysqldb import MySQL

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_api_inventario'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db_api_inventario'

# Inicializar el conector de MySQL
mysql = MySQL(app)

# Un ejemplo de ruta que usa la base de datos
@app.route('/usuarios')
def usuarios():
    # Crear un cursor para interactuar con la base de datos
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')  # Suponiendo que tienes una tabla 'usuarios'
    usuarios = cur.fetchall()  # Obtener todos los resultados
    cur.close()
    
    # Renderizar los resultados (aquí simplemente los estamos retornando como un ejemplo)
    return str(usuarios)

if __name__ == '__main__':
    app.run(debug=True)
