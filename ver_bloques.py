import pymysql
from datetime import datetime

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='gimnasio_db',
    cursorclass=pymysql.cursors.DictCursor
)

cur = conn.cursor()
cur.execute('''
    SELECT b.id, b.fecha, b.hora, b.actividad, b.cupos_disponibles, e.nombre as entrenador 
    FROM bloques b 
    LEFT JOIN entrenadores e ON b.entrenador_id = e.id 
    ORDER BY b.fecha, b.hora
''')

bloques = cur.fetchall()
print(f'Fecha actual: {datetime.now().date()}')
print(f'\nTotal bloques: {len(bloques)}')
print('\nBloques registrados:')

for b in bloques:
    print(f'  #{b["id"]}: {b["fecha"]} {b["hora"]} - {b["actividad"]} con {b["entrenador"]} ({b["cupos_disponibles"]} cupos)')

cur.close()
conn.close()
