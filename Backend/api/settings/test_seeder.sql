-- Seleccionar la base de datos
USE flask_app_db;

-- Borrar datos existentes en las tablas
DELETE FROM usuarios;
DELETE FROM categorias;
DELETE FROM productos;
DELETE FROM proveedores;
DELETE FROM producto_proveedor;
DELETE FROM ordenes_compra;

-- Insertar datos de prueba en la tabla de usuarios (administradores o usuarios del sistema)
INSERT INTO usuarios (nombre_usuario, contraseña, correo) VALUES
('admin', 'adminpassword', 'admin@mail.com'),
('jdoe', 'password123', 'jdoe@mail.com'),
('msmith', 'mypassword', 'msmith@mail.com'),
('jdoe2', 'password456', 'jdoe2@mail.com');

-- Insertar datos de prueba en la tabla de categorías
INSERT INTO categorias (nombre) VALUES
('Electrónica'),
('Ropa'),
('Hogar'),
('Alimentos');

-- Insertar datos de prueba en la tabla de productos
INSERT INTO productos (nombre, precio, stock, categoria_id, id_usuario) VALUES
('Laptop', 799.99, 50, 1, 1),
('Camiseta', 19.99, 100, 2, 2),
('Sofá', 399.99, 20, 3, 3),
('Arroz', 2.99, 500, 4, 4);

-- Insertar datos de prueba en la tabla de proveedores
INSERT INTO proveedores (nombre, correo_contacto, telefono_contacto) VALUES
('Proveedor 1', 'proveedor1@mail.com', '555-1234'),
('Proveedor 2', 'proveedor2@mail.com', '555-5678'),
('Proveedor 3', 'proveedor3@mail.com', '555-9876'),
('Proveedor 4', 'proveedor4@mail.com', '555-0000');

-- Insertar datos de prueba en la tabla de relaciones entre productos y proveedores
INSERT INTO producto_proveedor (producto_id, proveedor_id) VALUES
(1, 1),  -- Laptop con Proveedor 1
(2, 2),  -- Camiseta con Proveedor 2
(3, 3),  -- Sofá con Proveedor 3
(4, 4);  -- Arroz con Proveedor 4

-- Insertar datos de prueba en la tabla de órdenes de compra
INSERT INTO ordenes_compra (producto_id, cantidad, fecha_entrega_estimada, estado, usuario_id) VALUES
(1, 5, '2024-12-15', 'pendiente', 1),
(2, 10, '2024-12-10', 'completada', 2),
(3, 2, '2024-12-20', 'pendiente', 3),
(4, 100, '2024-12-05', 'cancelada', 4);

