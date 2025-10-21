"""
Script simple para verificar la conexion a MySQL (compatible con Windows)
"""
import sys

def verificar():
    print("=" * 50)
    print("VERIFICANDO CONEXION A MYSQL")
    print("=" * 50)
    
    # 1. Verificar config.py
    try:
        import config
        print("[OK] Archivo config.py encontrado")
    except ImportError:
        print("[ERROR] No se encontro config.py")
        return False
    
    # 2. Verificar contraseña
    if config.MYSQL_PASSWORD == 'tu_contraseña_aqui':
        print("[ADVERTENCIA] Debes cambiar la contraseña en config.py")
        return False
    else:
        print("[OK] Contraseña configurada")
    
    # 3. Verificar PyMySQL
    try:
        import pymysql
        print("[OK] PyMySQL instalado")
    except ImportError:
        print("[ERROR] PyMySQL no esta instalado")
        return False
    
    # 4. Conectar a MySQL
    try:
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        print("[OK] Conexion exitosa a MySQL")
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"    Version de MySQL: {version[0]}")
        cursor.close()
        
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a MySQL: {e}")
        print("\nPosibles soluciones:")
        print("  1. Verifica que MySQL este corriendo")
        print("  2. Verifica la contraseña en config.py")
        print("  3. Verifica que existe la base de datos 'gimnasio_db'")
        return False
    
    # 5. Verificar tablas
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        connection.close()
        
        tablas_encontradas = [table[0] for table in tables]
        tablas_esperadas = ['bloques', 'entrenadores', 'reservas', 'usuarios']
        
        print("\nTablas encontradas:")
        todas_ok = True
        for tabla in tablas_esperadas:
            if tabla in tablas_encontradas:
                print(f"  [OK] {tabla}")
            else:
                print(f"  [X] {tabla} (falta)")
                todas_ok = False
        
        if not todas_ok:
            print("\n[ADVERTENCIA] Faltan tablas. Ejecuta database.sql en MySQL Workbench")
            return False
            
    except Exception as e:
        print(f"[ERROR] No se pudieron verificar las tablas: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("TODO ESTA CONFIGURADO CORRECTAMENTE!")
    print("=" * 50)
    print("\nProximos pasos:")
    print("  1. Ejecuta: python app_simple.py")
    print("  2. Abre index.html en tu navegador")
    print("  3. Disfruta tu aplicacion!")
    print()
    
    return True

if __name__ == '__main__':
    try:
        exito = verificar()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\nVerificacion cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR INESPERADO: {e}")
        sys.exit(1)

