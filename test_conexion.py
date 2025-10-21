"""
Script para verificar la conexión a MySQL
Ejecuta este archivo para verificar que todo está configurado correctamente
"""
import sys

def test_conexion():
    print("=" * 50)
    print("🔍 VERIFICANDO CONEXIÓN A MYSQL")
    print("=" * 50)
    
    # 1. Verificar que config.py existe
    try:
        import config
        print("✅ Archivo config.py encontrado")
    except ImportError:
        print("❌ ERROR: No se encontró config.py")
        return False
    
    # 2. Verificar que la contraseña fue cambiada
    if config.MYSQL_PASSWORD == 'tu_contraseña_aqui':
        print("⚠️  ADVERTENCIA: Debes cambiar la contraseña en config.py")
        print("   Abre config.py y modifica MYSQL_PASSWORD")
        return False
    else:
        print("✅ Contraseña configurada")
    
    # 3. Intentar importar Flask y MySQL
    try:
        from flask import Flask
        from flask_mysqldb import MySQL
        print("✅ Flask instalado correctamente")
        print("✅ Flask-MySQLdb instalado correctamente")
    except ImportError as e:
        print(f"❌ ERROR: Falta instalar dependencias: {e}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    # 4. Intentar conectar a MySQL
    try:
        app = Flask(__name__)
        app.config['MYSQL_HOST'] = config.MYSQL_HOST
        app.config['MYSQL_USER'] = config.MYSQL_USER
        app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
        app.config['MYSQL_DB'] = config.MYSQL_DB
        
        mysql = MySQL(app)
        
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            cur.close()
            
            print(f"✅ Conexión exitosa a MySQL")
            print(f"   Versión de MySQL: {version[0]}")
    except Exception as e:
        print(f"❌ ERROR al conectar a MySQL: {e}")
        print("\n📋 Posibles soluciones:")
        print("   1. Verifica que MySQL esté corriendo")
        print("   2. Verifica la contraseña en config.py")
        print("   3. Verifica que existe la base de datos 'gimnasio_db'")
        return False
    
    # 5. Verificar tablas
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            cur.close()
            
            expected_tables = ['bloques', 'entrenadores', 'reservas', 'usuarios']
            found_tables = [table[0] for table in tables]
            
            print("\n📊 Tablas encontradas:")
            for table in expected_tables:
                if table in found_tables:
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table} (falta)")
            
            if all(table in found_tables for table in expected_tables):
                print("\n✅ Todas las tablas están creadas correctamente")
            else:
                print("\n⚠️  Faltan tablas. Ejecuta database.sql en MySQL Workbench")
                return False
    except Exception as e:
        print(f"❌ ERROR al verificar tablas: {e}")
        return False
    
    # 6. Verificar entrenadores
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM entrenadores")
            count = cur.fetchone()[0]
            cur.close()
            
            if count >= 2:
                print(f"✅ Entrenadores registrados: {count}")
            else:
                print(f"⚠️  Solo hay {count} entrenadores. Debería haber al menos 2")
    except Exception as e:
        print(f"❌ ERROR al verificar entrenadores: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ¡TODO ESTÁ CONFIGURADO CORRECTAMENTE!")
    print("=" * 50)
    print("\n📝 Próximos pasos:")
    print("   1. Ejecuta: python app_simple.py")
    print("   2. Abre index.html en tu navegador")
    print("   3. ¡Disfruta tu aplicación!")
    print("\n")
    
    return True

if __name__ == '__main__':
    try:
        success = test_conexion()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERROR INESPERADO: {e}")
        sys.exit(1)

