"""
Script para actualizar la base de datos y agregar el estado pendiente_pago
"""
import pymysql
import config

try:
    connection = pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )
    
    cursor = connection.cursor()
    
    print("Actualizando tabla reservas...")
    cursor.execute("""
        ALTER TABLE reservas 
        MODIFY COLUMN estado ENUM('activa', 'cancelada', 'pendiente_pago') DEFAULT 'activa'
    """)
    
    connection.commit()
    print("[OK] Tabla actualizada exitosamente!")
    print("     Ahora la tabla reservas acepta el estado 'pendiente_pago'")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"[ERROR] {e}")

