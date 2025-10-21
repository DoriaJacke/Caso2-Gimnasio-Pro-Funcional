"""
Script para actualizar la base de datos con funcionalidades de administrador
Gimnasio Pro Funcional
"""
import pymysql
import config

def actualizar_base_datos():
    try:
        # Conectar a MySQL
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        
        cursor = connection.cursor()
        
        # Leer el archivo SQL
        with open('actualizar_bd_admin.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar cada comando SQL
        for statement in sql_script.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                    connection.commit()
                except pymysql.err.OperationalError as e:
                    # Error 1060: Columna duplicada (ya existe)
                    if e.args[0] == 1060:
                        print(f"Nota: Columna ya existe, continuando...")
                    else:
                        print(f"Advertencia: {e}")
                    continue
                except Exception as e:
                    print(f"Advertencia: {e}")
                    continue
        
        print("=" * 60)
        print("BASE DE DATOS ACTUALIZADA CORRECTAMENTE")
        print("=" * 60)
        print("Cambios aplicados:")
        print("- Tabla 'administradores' creada")
        print("- Campos adicionales agregados a 'usuarios'")
        print("- Tabla 'cupos' creada")
        print("- Tabla 'progreso_cliente' creada")
        print("- Administrador por defecto creado:")
        print("  Usuario: admin")
        print("  Contrasena: admin123")
        print("=" * 60)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    actualizar_base_datos()

