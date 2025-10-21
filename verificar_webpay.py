"""
Script para verificar transacciones de Webpay en MySQL
"""
import pymysql
import config

def verificar_webpay():
    print("=" * 70)
    print("VERIFICANDO TRANSACCIONES DE WEBPAY")
    print("=" * 70)
    
    try:
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        
        cursor = connection.cursor()
        
        # Verificar si existe la tabla
        cursor.execute("SHOW TABLES LIKE 'transacciones_webpay'")
        if not cursor.fetchone():
            print("\n[INFO] La tabla transacciones_webpay aun no existe.")
            print("       Se creara automaticamente cuando hagas la primera transaccion.")
            cursor.close()
            connection.close()
            return
        
        # Ver transacciones de Webpay
        print("\n[TRANSACCIONES DE WEBPAY]")
        cursor.execute("""
            SELECT 
                t.id,
                t.buy_order,
                t.amount,
                t.estado,
                t.fecha_creacion,
                r.actividad,
                r.fecha as fecha_clase,
                r.hora,
                r.estado as estado_reserva,
                u.username
            FROM transacciones_webpay t
            JOIN reservas r ON t.reserva_id = r.id
            JOIN usuarios u ON r.usuario_id = u.id
            ORDER BY t.fecha_creacion DESC
        """)
        
        transacciones = cursor.fetchall()
        
        if not transacciones:
            print("  No hay transacciones registradas aun.")
            print("  Crea una reserva desde el frontend para generar una transaccion.")
        else:
            for t in transacciones:
                print(f"\n  ID: {t[0]}")
                print(f"  Orden: {t[1]}")
                print(f"  Monto: ${t[2]:,} CLP")
                print(f"  Estado Transaccion: {t[3].upper()}")
                print(f"  Fecha Creacion: {t[4]}")
                print(f"  ----")
                print(f"  Usuario: {t[9]}")
                print(f"  Actividad: {t[5]}")
                print(f"  Clase: {t[6]} a las {t[7]}")
                print(f"  Estado Reserva: {t[8].upper()}")
                print(f"  {'-' * 66}")
        
        # Resumen
        cursor.execute("""
            SELECT 
                estado,
                COUNT(*) as cantidad,
                SUM(amount) as total
            FROM transacciones_webpay
            GROUP BY estado
        """)
        
        resumen = cursor.fetchall()
        
        if resumen:
            print("\n[RESUMEN]")
            for r in resumen:
                print(f"  {r[0].upper()}: {r[1]} transaccion(es) - Total: ${r[2]:,} CLP")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    verificar_webpay()

