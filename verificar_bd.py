"""
Script para verificar los datos en MySQL
"""
import pymysql
import config

def verificar():
    print("=" * 60)
    print("VERIFICANDO DATOS EN MYSQL")
    print("=" * 60)
    
    try:
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        
        cursor = connection.cursor()
        
        # Usuarios
        print("\n[USUARIOS]")
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        for u in usuarios:
            print(f"  ID: {u[0]} | Usuario: {u[1]} | Rol: {u[2]}")
        
        # Reservas
        print("\n[RESERVAS]")
        cursor.execute("""
            SELECT 
                r.id,
                u.username,
                r.actividad,
                r.fecha,
                r.hora,
                e.nombre,
                r.estado
            FROM reservas r
            JOIN usuarios u ON r.usuario_id = u.id
            JOIN entrenadores e ON r.entrenador_id = e.id
            ORDER BY r.id
        """)
        reservas = cursor.fetchall()
        for r in reservas:
            print(f"  ID: {r[0]} | Usuario: {r[1]} | {r[2]} | {r[3]} {r[4]} | {r[5]} | Estado: {r[6]}")
        
        # Bloques
        print("\n[BLOQUES]")
        cursor.execute("""
            SELECT 
                b.id,
                b.actividad,
                b.fecha,
                b.hora,
                e.nombre,
                b.cupos_disponibles,
                b.cupos_totales
            FROM bloques b
            JOIN entrenadores e ON b.entrenador_id = e.id
            ORDER BY b.id
        """)
        bloques = cursor.fetchall()
        for b in bloques:
            print(f"  ID: {b[0]} | {b[1]} | {b[2]} {b[3]} | {b[4]} | Cupos: {b[5]}/{b[6]}")
        
        # Entrenadores
        print("\n[ENTRENADORES]")
        cursor.execute("SELECT * FROM entrenadores")
        entrenadores = cursor.fetchall()
        for e in entrenadores:
            print(f"  ID: {e[0]} | {e[1]} | {e[2]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("VERIFICACION COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    verificar()

