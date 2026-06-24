import re

def sanitizar(name):
    # Normaliza texto a minúsculas y elimina espacios sobrantes
    name = name.lower().strip()

    # Reemplaza puntuación y caracteres extraños por espacios
    name = re.sub(r'[^a-z0-9áéíóúüñ\s]', ' ', name)

    # Palabras y frases comunes a eliminar de la intención del usuario
    stop_words = [
        "precio de la acción", "precio de la accion", "precio de la", "precio de las", "precio de",
        "precio acción", "precio accion", "precio", "acción", "accion", "stock", "cotización",
        "cotizacion", "ticker", "valor de", "valor", "cotización de", "cotizacion de",
        "de", "en", "para", "la", "el", "las", "los", "mi", "por favor", "porfavor"
    ]

    for stop in stop_words:
        name = re.sub(r'\b' + re.escape(stop) + r'\b', ' ', name)

    name = re.sub(r'\s+', ' ', name).strip()
    return name
    