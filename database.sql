-- ==========================================
-- BASE DE DATOS: GIMNASIO PRO FUNCIONAL
-- ==========================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS gimnasio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gimnasio_db;

-- ==========================================
-- TABLA: USUARIOS
-- ==========================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    rol ENUM('cliente', 'admin', 'entrenador') NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- TABLA: ENTRENADORES
-- ==========================================
CREATE TABLE IF NOT EXISTS entrenadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    especialidad VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- TABLA: RESERVAS
-- ==========================================
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    actividad ENUM('Cardio', 'Fuerza') NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    entrenador_id INT NOT NULL,
    estado ENUM('activa', 'cancelada') DEFAULT 'activa',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (entrenador_id) REFERENCES entrenadores(id) ON DELETE CASCADE,
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha (fecha),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- TABLA: BLOQUES (para administrador)
-- ==========================================
CREATE TABLE IF NOT EXISTS bloques (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actividad ENUM('Cardio', 'Fuerza') NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    entrenador_id INT NOT NULL,
    cupos_totales INT NOT NULL,
    cupos_disponibles INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrenador_id) REFERENCES entrenadores(id) ON DELETE CASCADE,
    INDEX idx_fecha (fecha),
    INDEX idx_entrenador (entrenador_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- DATOS INICIALES: ENTRENADORES
-- ==========================================
INSERT INTO entrenadores (nombre, especialidad) VALUES
('Ricardo Meruane', 'Entrenamiento Funcional'),
('George Harris', 'Fuerza y Acondicionamiento');

-- ==========================================
-- DATOS DE PRUEBA (OPCIONAL)
-- ==========================================

-- Usuarios de ejemplo
INSERT INTO usuarios (username, rol) VALUES
('admin1', 'admin'),
('cliente1', 'cliente'),
('entrenador1', 'entrenador');

-- Reservas de ejemplo
INSERT INTO reservas (usuario_id, actividad, fecha, hora, entrenador_id, estado) VALUES
(2, 'Cardio', '2025-10-25', '10:00:00', 1, 'activa'),
(2, 'Fuerza', '2025-10-26', '15:00:00', 2, 'activa');

-- Bloques de ejemplo
INSERT INTO bloques (actividad, fecha, hora, entrenador_id, cupos_totales, cupos_disponibles) VALUES
('Cardio', '2025-10-25', '10:00:00', 1, 10, 9),
('Fuerza', '2025-10-26', '15:00:00', 2, 8, 7);

-- ==========================================
-- CONSULTAS ÚTILES PARA VERIFICACIÓN
-- ==========================================

-- Ver todos los usuarios
-- SELECT * FROM usuarios;

-- Ver todas las reservas con información del entrenador
-- SELECT r.*, u.username, e.nombre as entrenador 
-- FROM reservas r 
-- JOIN usuarios u ON r.usuario_id = u.id 
-- JOIN entrenadores e ON r.entrenador_id = e.id;

-- Ver bloques disponibles
-- SELECT b.*, e.nombre as entrenador 
-- FROM bloques b 
-- JOIN entrenadores e ON b.entrenador_id = e.id
-- WHERE b.cupos_disponibles > 0;

