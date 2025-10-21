-- Agregar el estado 'pendiente_pago' a la tabla reservas
USE gimnasio_db;

ALTER TABLE reservas 
MODIFY COLUMN estado ENUM('activa', 'cancelada', 'pendiente_pago') DEFAULT 'activa';

-- Verificar el cambio
DESCRIBE reservas;

