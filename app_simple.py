"""
Backend simplificado que usa config.py en lugar de .env
Versión compatible con Windows usando PyMySQL
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime
import config  # Importar configuración

app = Flask(__name__)
CORS(app)

# Configuración de MySQL desde config.py usando PyMySQL
def get_db_connection():
    return pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

# ==================== USUARIOS ====================
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        role = data.get('role')
        
        if not username or not role:
            return jsonify({'error': 'Usuario y rol son requeridos'}), 400
        
        connection = get_db_connection()
        cur = connection.cursor()
        
        # Verificar si el usuario existe
        cur.execute("SELECT * FROM usuarios WHERE username = %s AND rol = %s", (username, role))
        user = cur.fetchone()
        
        # Si no existe, crearlo automáticamente
        if not user:
            cur.execute("INSERT INTO usuarios (username, rol) VALUES (%s, %s)", (username, role))
            connection.commit()
            user_id = cur.lastrowid
        else:
            user_id = user['id']
        
        cur.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'username': username,
            'role': role
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RESERVAS (CLIENTE) ====================
@app.route('/api/reservas/<int:user_id>', methods=['GET'])
def get_reservas(user_id):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            SELECT r.*, e.nombre as nombre_entrenador 
            FROM reservas r
            LEFT JOIN entrenadores e ON r.entrenador_id = e.id
            WHERE r.usuario_id = %s AND r.estado = 'activa'
            ORDER BY r.fecha, r.hora
        """, (user_id,))
        reservas = cur.fetchall()
        cur.close()
        connection.close()
        
        # Convertir timedelta a string
        for reserva in reservas:
            if 'hora' in reserva and reserva['hora']:
                reserva['hora'] = str(reserva['hora'])
            if 'fecha' in reserva and reserva['fecha']:
                reserva['fecha'] = str(reserva['fecha'])
            if 'fecha_creacion' in reserva and reserva['fecha_creacion']:
                reserva['fecha_creacion'] = str(reserva['fecha_creacion'])
            if 'fecha_modificacion' in reserva and reserva['fecha_modificacion']:
                reserva['fecha_modificacion'] = str(reserva['fecha_modificacion'])
        
        return jsonify(reservas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservas', methods=['POST'])
def crear_reserva():
    try:
        data = request.json
        user_id = data.get('user_id')
        actividad = data.get('actividad')
        fecha = data.get('fecha')
        hora = data.get('hora')
        entrenador_nombre = data.get('entrenador')
        
        connection = get_db_connection()
        cur = connection.cursor()
        
        # Obtener ID del entrenador
        cur.execute("SELECT id FROM entrenadores WHERE nombre = %s", (entrenador_nombre,))
        entrenador = cur.fetchone()
        
        if not entrenador:
            cur.close()
            connection.close()
            return jsonify({'error': 'Entrenador no encontrado'}), 404
        
        entrenador_id = entrenador['id']
        
        # Crear la reserva
        cur.execute("""
            INSERT INTO reservas (usuario_id, actividad, fecha, hora, entrenador_id, estado, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, 'activa', NOW())
        """, (user_id, actividad, fecha, hora, entrenador_id))
        
        connection.commit()
        reserva_id = cur.lastrowid
        cur.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'reserva_id': reserva_id,
            'message': 'Reserva creada exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservas/<int:reserva_id>', methods=['DELETE'])
def cancelar_reserva(reserva_id):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        
        # Verificar que la reserva existe
        cur.execute("SELECT * FROM reservas WHERE id = %s", (reserva_id,))
        reserva = cur.fetchone()
        
        if not reserva:
            cur.close()
            connection.close()
            return jsonify({'error': 'Reserva no encontrada'}), 404
        
        # Actualizar estado a cancelada
        cur.execute("""
            UPDATE reservas 
            SET estado = 'cancelada', fecha_modificacion = NOW()
            WHERE id = %s
        """, (reserva_id,))
        
        connection.commit()
        cur.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Reserva cancelada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HISTORIAL (CLIENTE) ====================
@app.route('/api/historial/<int:user_id>', methods=['GET'])
def get_historial(user_id):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            SELECT r.*, e.nombre as nombre_entrenador 
            FROM reservas r
            LEFT JOIN entrenadores e ON r.entrenador_id = e.id
            WHERE r.usuario_id = %s
            ORDER BY r.fecha_creacion DESC
        """, (user_id,))
        historial = cur.fetchall()
        cur.close()
        connection.close()
        
        # Convertir timedelta a string
        for reserva in historial:
            if 'hora' in reserva and reserva['hora']:
                reserva['hora'] = str(reserva['hora'])
            if 'fecha' in reserva and reserva['fecha']:
                reserva['fecha'] = str(reserva['fecha'])
            if 'fecha_creacion' in reserva and reserva['fecha_creacion']:
                reserva['fecha_creacion'] = str(reserva['fecha_creacion'])
            if 'fecha_modificacion' in reserva and reserva['fecha_modificacion']:
                reserva['fecha_modificacion'] = str(reserva['fecha_modificacion'])
        
        return jsonify(historial), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== BLOQUES (ADMIN) ====================
@app.route('/api/bloques', methods=['GET'])
def get_bloques():
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            SELECT b.*, e.nombre as nombre_entrenador 
            FROM bloques b
            LEFT JOIN entrenadores e ON b.entrenador_id = e.id
            ORDER BY b.fecha, b.hora
        """)
        bloques = cur.fetchall()
        cur.close()
        connection.close()
        
        # Convertir timedelta a string
        for bloque in bloques:
            if 'hora' in bloque and bloque['hora']:
                bloque['hora'] = str(bloque['hora'])
            if 'fecha' in bloque and bloque['fecha']:
                bloque['fecha'] = str(bloque['fecha'])
            if 'fecha_creacion' in bloque and bloque['fecha_creacion']:
                bloque['fecha_creacion'] = str(bloque['fecha_creacion'])
        
        return jsonify(bloques), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bloques', methods=['POST'])
def crear_bloque():
    try:
        data = request.json
        actividad = data.get('actividad')
        fecha = data.get('fecha')
        hora = data.get('hora')
        entrenador_nombre = data.get('entrenador')
        cupos = data.get('cupos')
        
        connection = get_db_connection()
        cur = connection.cursor()
        
        # Obtener ID del entrenador
        cur.execute("SELECT id FROM entrenadores WHERE nombre = %s", (entrenador_nombre,))
        entrenador = cur.fetchone()
        
        if not entrenador:
            cur.close()
            connection.close()
            return jsonify({'error': 'Entrenador no encontrado'}), 404
        
        entrenador_id = entrenador['id']
        
        # Crear el bloque
        cur.execute("""
            INSERT INTO bloques (actividad, fecha, hora, entrenador_id, cupos_totales, cupos_disponibles)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (actividad, fecha, hora, entrenador_id, cupos, cupos))
        
        connection.commit()
        bloque_id = cur.lastrowid
        cur.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'bloque_id': bloque_id,
            'message': 'Bloque creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ENTRENADORES ====================
@app.route('/api/entrenadores', methods=['GET'])
def get_entrenadores():
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM entrenadores")
        entrenadores = cur.fetchall()
        cur.close()
        connection.close()
        
        return jsonify(entrenadores), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ALUMNOS POR ENTRENADOR ====================
@app.route('/api/entrenador/<string:nombre>/alumnos', methods=['GET'])
def get_alumnos_entrenador(nombre):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            SELECT DISTINCT u.username, u.id
            FROM usuarios u
            INNER JOIN reservas r ON u.id = r.usuario_id
            INNER JOIN entrenadores e ON r.entrenador_id = e.id
            WHERE e.nombre = %s AND r.estado = 'activa'
        """, (nombre,))
        alumnos = cur.fetchall()
        cur.close()
        connection.close()
        
        return jsonify(alumnos), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PROGRESO (CLIENTE) ====================
@app.route('/api/progreso/<int:user_id>', methods=['GET'])
def get_progreso(user_id):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        
        # Contar reservas completadas vs totales
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN fecha < CURDATE() THEN 1 ELSE 0 END) as completadas
            FROM reservas
            WHERE usuario_id = %s AND estado = 'activa'
        """, (user_id,))
        
        resultado = cur.fetchone()
        cur.close()
        connection.close()
        
        total = resultado['total'] if resultado['total'] else 0
        completadas = resultado['completadas'] if resultado['completadas'] else 0
        
        porcentaje = (completadas / total * 100) if total > 0 else 0
        
        return jsonify({
            'total': total,
            'completadas': completadas,
            'porcentaje': round(porcentaje, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTA PRINCIPAL ====================
@app.route('/')
def index():
    return jsonify({
        'message': 'API Gimnasio Pro Funcional',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            'login': '/api/login [POST]',
            'reservas': '/api/reservas/:user_id [GET], /api/reservas [POST]',
            'cancelar': '/api/reservas/:reserva_id [DELETE]',
            'historial': '/api/historial/:user_id [GET]',
            'bloques': '/api/bloques [GET, POST]',
            'entrenadores': '/api/entrenadores [GET]',
            'alumnos': '/api/entrenador/:nombre/alumnos [GET]',
            'progreso': '/api/progreso/:user_id [GET]'
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)

