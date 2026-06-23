import requests

def obtener_clima(user_input):

    city = user_input.lower().replace("clima", "").replace("temperatura", "").replace("en", "").replace("de", "").strip

    try:
        response = requests.get(f"https://wttr.in/{city}?format=%t", timeout=10)

        if response.status_code == 200:
            return response.text.strip()
        
        else: 
            return "ChatBot: No se pudo encontrar la ciudad que buscas"
        
    except Exception as e:
        return f"ChatBot: Error de red, porfavor revisa tu conexión {e}"