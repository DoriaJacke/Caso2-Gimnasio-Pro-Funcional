from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'gimnasio_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ==================== USUARIOS ====================
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        role = data.get('role')
        
        if not username or not role:
            return jsonify({'error': 'Usuario y rol son requeridos'}), 400
        
        cur = mysql.connection.cursor()
        
        # Verificar si el usuario existe
        cur.execute("SELECT * FROM usuarios WHERE username = %s AND rol = %s", (username, role))
        user = cur.fetchone()
        
        # Si no existe, crearlo automáticamente (para simplificar el demo)
        if not user:
            cur.execute("INSERT INTO usuarios (username, rol) VALUES (%s, %s)", (username, role))
            mysql.connection.commit()
            user_id = cur.lastrowid
        else:
            user_id = user['id']
        
        cur.close()
        
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
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT r.*, e.nombre as nombre_entrenador 
            FROM reservas r
            LEFT JOIN entrenadores e ON r.entrenador_id = e.id
            WHERE r.usuario_id = %s AND r.estado = 'activa'
            ORDER BY r.fecha, r.hora
        """, (user_id,))
        reservas = cur.fetchall()
        cur.close()
        
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
        
        cur = mysql.connection.cursor()
        
        # Obtener ID del entrenador
        cur.execute("SELECT id FROM entrenadores WHERE nombre = %s", (entrenador_nombre,))
        entrenador = cur.fetchone()
        
        if not entrenador:
            cur.close()
            return jsonify({'error': 'Entrenador no encontrado'}), 404
        
        entrenador_id = entrenador['id']
        
        # Crear la reserva
        cur.execute("""
            INSERT INTO reservas (usuario_id, actividad, fecha, hora, entrenador_id, estado, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, 'activa', NOW())
        """, (user_id, actividad, fecha, hora, entrenador_id))
        
        mysql.connection.commit()
        reserva_id = cur.lastrowid
        cur.close()
        
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
        cur = mysql.connection.cursor()
        
        # Verificar que la reserva existe
        cur.execute("SELECT * FROM reservas WHERE id = %s", (reserva_id,))
        reserva = cur.fetchone()
        
        if not reserva:
            cur.close()
            return jsonify({'error': 'Reserva no encontrada'}), 404
        
        # Actualizar estado a cancelada
        cur.execute("""
            UPDATE reservas 
            SET estado = 'cancelada', fecha_modificacion = NOW()
            WHERE id = %s
        """, (reserva_id,))
        
        mysql.connection.commit()
        cur.close()
        
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
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT r.*, e.nombre as nombre_entrenador 
            FROM reservas r
            LEFT JOIN entrenadores e ON r.entrenador_id = e.id
            WHERE r.usuario_id = %s
            ORDER BY r.fecha_creacion DESC
        """, (user_id,))
        historial = cur.fetchall()
        cur.close()
        
        return jsonify(historial), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== BLOQUES (ADMIN) ====================
@app.route('/api/bloques', methods=['GET'])
def get_bloques():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT b.*, e.nombre as nombre_entrenador 
            FROM bloques b
            LEFT JOIN entrenadores e ON b.entrenador_id = e.id
            ORDER BY b.fecha, b.hora
        """)
        bloques = cur.fetchall()
        cur.close()
        
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
        
        cur = mysql.connection.cursor()
        
        # Obtener ID del entrenador
        cur.execute("SELECT id FROM entrenadores WHERE nombre = %s", (entrenador_nombre,))
        entrenador = cur.fetchone()
        
        if not entrenador:
            cur.close()
            return jsonify({'error': 'Entrenador no encontrado'}), 404
        
        entrenador_id = entrenador['id']
        
        # Crear el bloque
        cur.execute("""
            INSERT INTO bloques (actividad, fecha, hora, entrenador_id, cupos_totales, cupos_disponibles)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (actividad, fecha, hora, entrenador_id, cupos, cupos))
        
        mysql.connection.commit()
        bloque_id = cur.lastrowid
        cur.close()
        
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
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM entrenadores")
        entrenadores = cur.fetchall()
        cur.close()
        
        return jsonify(entrenadores), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ALUMNOS POR ENTRENADOR ====================
@app.route('/api/entrenador/<string:nombre>/alumnos', methods=['GET'])
def get_alumnos_entrenador(nombre):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT DISTINCT u.username, u.id
            FROM usuarios u
            INNER JOIN reservas r ON u.id = r.usuario_id
            INNER JOIN entrenadores e ON r.entrenador_id = e.id
            WHERE e.nombre = %s AND r.estado = 'activa'
        """, (nombre,))
        alumnos = cur.fetchall()
        cur.close()
        
        return jsonify(alumnos), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PROGRESO (CLIENTE) ====================
@app.route('/api/progreso/<int:user_id>', methods=['GET'])
def get_progreso(user_id):
    try:
        cur = mysql.connection.cursor()
        
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
    app.run(debug=True, port=5000)

