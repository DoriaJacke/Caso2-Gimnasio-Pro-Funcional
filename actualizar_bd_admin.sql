-- Script para actualizar la base de datos con las nuevas funcionalidades
-- Gimnasio Pro Funcional - Panel de Administrador

USE gimnasio_db;

-- 1. Crear tabla de administradores
CREATE TABLE IF NOT EXISTS administradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Agregar campos adicionales a la tabla usuarios (si no existen)
ALTER TABLE usuarios 
ADD COLUMN email VARCHAR(100);

ALTER TABLE usuarios 
ADD COLUMN telefono VARCHAR(20);

ALTER TABLE usuarios 
ADD COLUMN direccion VARCHAR(200);

ALTER TABLE usuarios 
ADD COLUMN fecha_nacimiento DATE;

ALTER TABLE usuarios 
ADD COLUMN peso DECIMAL(5,2);

ALTER TABLE usuarios 
ADD COLUMN altura DECIMAL(5,2);

ALTER TABLE usuarios 
ADD COLUMN objetivo TEXT;

-- 3. Crear tabla de cupos/slots disponibles
CREATE TABLE IF NOT EXISTS cupos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    entrenador_nombre VARCHAR(100),
    actividad VARCHAR(100) NOT NULL,
    capacidad_maxima INT DEFAULT 10,
    disponible BOOLEAN DEFAULT TRUE,
    creado_por VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrenador_nombre) REFERENCES entrenadores(nombre) ON DELETE SET NULL,
    UNIQUE KEY cupo_unico (fecha, hora, entrenador_nombre)
);

-- 4. Insertar administrador por defecto
INSERT INTO administradores (username, password, nombre, email)
VALUES ('admin', 'admin123', 'Administrador Principal', 'admin@gimnasio.com')
ON DUPLICATE KEY UPDATE username = username;

-- 5. Crear tabla de progreso del cliente (mejorada)
CREATE TABLE IF NOT EXISTS progreso_cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    peso DECIMAL(5,2),
    notas TEXT,
    entrenador_nombre VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (entrenador_nombre) REFERENCES entrenadores(nombre) ON DELETE SET NULL
);

-- Mostrar confirmación
SELECT 'Base de datos actualizada correctamente' AS mensaje;

