


-- Seleccionar la base de datos
USE db_api_inventario;

-- Crear tabla de usuarios (administradores o usuarios del sistema)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL UNIQUE
);

-- Crear tabla de categorías de productos
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Crear tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    categoria_id INT NOT NULL,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_categoria 
    FOREIGN KEY (categoria_id) 
    REFERENCES categorias (id)
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    CONSTRAINT fk_usuario 
    FOREIGN KEY (id_usuario) 
    REFERENCES usuarios (id)
    ON DELETE CASCADE 
    ON UPDATE CASCADE
);

-- Crear tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    correo_contacto VARCHAR(255),
    telefono_contacto VARCHAR(50)
);

-- Crear tabla de relaciones entre productos y proveedores
CREATE TABLE IF NOT EXISTS producto_proveedor (
    producto_id INT NOT NULL,
    proveedor_id INT NOT NULL,
    PRIMARY KEY (producto_id, proveedor_id),
    CONSTRAINT fk_producto 
    FOREIGN KEY (producto_id) 
    REFERENCES productos (id)
    ON DELETE CASCADE,
    CONSTRAINT fk_proveedor 
    FOREIGN KEY (proveedor_id) 
    REFERENCES proveedores (id)
    ON DELETE CASCADE
);

-- Crear tabla de órdenes de compra
CREATE TABLE IF NOT EXISTS ordenes_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega_estimada DATE,
    estado ENUM('pendiente', 'completada', 'cancelada') NOT NULL,
    usuario_id INT NOT NULL,
    CONSTRAINT fk_producto_orden 
        FOREIGN KEY (producto_id) 
        REFERENCES productos (id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_usuario_orden 
        FOREIGN KEY (usuario_id) 
        REFERENCES usuarios (id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Crear un nuevo usuario con una contraseña segura para localhost
CREATE USER 'user_api_inventario'@'localhost' IDENTIFIED BY 'secure_password_123';

-- Conceder todos los privilegios en la base de datos
GRANT ALL PRIVILEGES ON db_api_inventario.* TO 'user_api_inventario'@'localhost' WITH GRANT OPTION;

-- Crear un nuevo usuario con una contraseña segura para 127.0.0.1
CREATE USER 'user_api_inventario'@'127.0.0.1' IDENTIFIED BY 'secure_password_123';

-- Conceder todos los privilegios en la base de datos
GRANT ALL PRIVILEGES ON db_api_inventario.* TO 'user_api_inventario'@'127.0.0.1' WITH GRANT OPTION;

-- Aplicar los cambios de privilegios (opcional, pero recomendable)
FLUSH PRIVILEGES;

-- Verificar los privilegios del nuevo usuario
SHOW GRANTS FOR 'user_api_inventario'@'localhost';
SHOW GRANTS FOR 'user_api_inventario'@'127.0.0.1';
