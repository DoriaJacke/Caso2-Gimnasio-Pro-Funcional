"""
Configuración de Webpay Plus para el Gimnasio
Ambiente de INTEGRACIÓN (pruebas)
"""

# Credenciales de integración de Transbank (ambiente de pruebas)
WEBPAY_COMMERCE_CODE = "597055555532"  # Código de comercio de pruebas
WEBPAY_API_KEY = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"  # API Key de pruebas

# URLs de retorno (ajusta según tu dominio)
# Para desarrollo local:
WEBPAY_RETURN_URL = "http://localhost:5000/api/webpay/confirmar"

# Configuración
WEBPAY_ENVIRONMENT = "INTEGRATION"  # Cambia a "PRODUCTION" en producción

# Monto de la reserva (en pesos chilenos)
PRECIO_RESERVA = 1  # $1 CLP por clase (para pruebas)

print(f"[WEBPAY] Configurado en modo: {WEBPAY_ENVIRONMENT}")
print(f"[WEBPAY] Precio por reserva: ${PRECIO_RESERVA:,} CLP")

