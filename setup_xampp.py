"""
Script para crear la base de datos en XAMPP
"""
import pymysql
import sys

print("=" * 60)
print("CONFIGURACIÓN BASE DE DATOS - XAMPP")
print("=" * 60)

# Conectar a MySQL (XAMPP sin contraseña)
print("\n[1/4] Conectando a MySQL (XAMPP)...")
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',  # XAMPP no tiene contraseña por defecto
        charset='utf8mb4'
    )
    print("✓ Conectado a MySQL")
except pymysql.Error as e:
    print(f"❌ Error: {e}")
    print("\n¿XAMPP está corriendo?")
    print("  1. Abre el Panel de Control de XAMPP")
    print("  2. Clic en 'Start' junto a MySQL")
    print("  3. Espera a que muestre 'Running'")
    print("  4. Ejecuta este script nuevamente")
    sys.exit(1)

cursor = connection.cursor()

# Crear base de datos
print("\n[2/4] Creando base de datos 'gimnasio_db'...")
cursor.execute("CREATE DATABASE IF NOT EXISTS gimnasio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
print("✓ Base de datos creada")

cursor.close()
connection.close()

# Conectar a la base de datos específica
print("\n[3/4] Conectando a gimnasio_db...")
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='gimnasio_db',
    charset='utf8mb4'
)
cursor = connection.cursor()
print("✓ Conectado a gimnasio_db")

# Leer y ejecutar database.sql
print("\n[4/4] Ejecutando database.sql...")
try:
    with open('database.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Remover comentarios y líneas vacías
    lines = []
    for line in sql_content.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            lines.append(line)
    
    sql_content = ' '.join(lines)
    
    # Ejecutar cada comando SQL separado por punto y coma
    commands = sql_content.split(';')
    
    for comando in commands:
        comando = comando.strip()
        if not comando:
            continue
        
        # Saltar USE gimnasio_db ya que ya estamos conectados
        if 'USE gimnasio_db' in comando.upper():
            continue
        
        # Saltar CREATE DATABASE ya que ya lo hicimos
        if 'CREATE DATABASE' in comando.upper():
            continue
        
        try:
            cursor.execute(comando)
            connection.commit()
        except pymysql.Error as e:
            error_code = e.args[0]
            # Ignorar errores de "ya existe"
            if error_code not in (1050, 1007, 1062):
                print(f"  ⚠ Advertencia en comando: {e}")
    
    print("✓ Estructura y datos creados")
    
except FileNotFoundError:
    print("❌ No se encontró database.sql")
    cursor.close()
    connection.close()
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    cursor.close()
    connection.close()
    sys.exit(1)

# Verificar tablas
print("\n[VERIFICACIÓN] Tablas en la base de datos:")
cursor.execute("SHOW TABLES")
tablas = cursor.fetchall()
for tabla in tablas:
    cursor.execute(f"SELECT COUNT(*) FROM {tabla[0]}")
    count = cursor.fetchone()[0]
    print(f"  ✓ {tabla[0]:20s} ({count} registros)")

cursor.close()
connection.close()

print("\n" + "=" * 60)
print("✅ BASE DE DATOS CONFIGURADA EXITOSAMENTE")
print("=" * 60)
print("\nPróximos pasos:")
print("  1. python backend.py")
print("  2. Abre index.html en tu navegador")
print("=" * 60)
