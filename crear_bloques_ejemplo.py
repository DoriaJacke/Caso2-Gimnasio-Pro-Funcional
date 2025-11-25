import pymysql
from datetime import datetime, timedelta

# Conectar a la base de datos
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='gimnasio_db'
)

cur = conn.cursor()

# Obtener IDs de entrenadores
cur.execute("SELECT id, nombre FROM entrenadores")
entrenadores = cur.fetchall()

if not entrenadores:
    print("❌ No hay entrenadores en la base de datos")
    exit(1)

print(f"✓ Entrenadores encontrados: {[e[1] for e in entrenadores]}")

# Generar bloques para los próximos 7 días
fecha_inicio = datetime.now().date()
actividades = ['Cardio', 'Fuerza']
horas = ['08:00:00', '10:00:00', '12:00:00', '15:00:00', '17:00:00', '19:00:00']

bloques_creados = 0

for dia in range(7):
    fecha = fecha_inicio + timedelta(days=dia)
    
    for hora in horas:
        for actividad in actividades:
            # Alternar entrenadores
            entrenador = entrenadores[bloques_creados % len(entrenadores)]
            entrenador_id = entrenador[0]
            entrenador_nombre = entrenador[1]
            
            try:
                cur.execute("""
                    INSERT INTO bloques (actividad, fecha, hora, entrenador_id, cupos_disponibles)
                    VALUES (%s, %s, %s, %s, %s)
                """, (actividad, fecha, hora, entrenador_id, 10))
                
                bloques_creados += 1
                print(f"✓ Creado: {fecha} {hora} - {actividad} con {entrenador_nombre}")
                
            except Exception as e:
                print(f"⚠ Error al crear bloque: {e}")

conn.commit()
cur.close()
conn.close()

print(f"\n{'='*60}")
print(f"✅ Total bloques creados: {bloques_creados}")
print(f"📅 Fechas: desde {fecha_inicio} hasta {fecha_inicio + timedelta(days=6)}")
print(f"{'='*60}")
