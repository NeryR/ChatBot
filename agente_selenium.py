import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import ChromeDriveManager

from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from utils.sanitizar import sanitizar

# --- Configuración de Selenium ---
# Se utilizan opciones para ejecutar el navegador de forma silenciosa (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Simulación de un User-Agent real para evitar bloqueos por parte de algunos sitios
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

driver_path = ChromeDriveManager().install()

if os.path.basename(driver_path) != "chromedriver":
    dir_path = os.path.dirname(driver_path)
    binary_path = os.path.join(dir_path, "chromedriver")
    if os.path.exists(binary_path):
        driver_path = binary_path

os.chmod(driver_path, 0o755)

driver = webdriver.Chrome(service=Service(driver_path, options=options))

def procesar_input(user_input):
    user_input = user_input.lower()

    if "clima" in user_input or "temperatura" in user_input:
        return obtener_clima
    elif "precio" in user_input or "accion" in user_input:
        return obtener_precio_accion
    else:
        return None
    
print("Hola, soy tu asistente virtual Selenium, ¿En que te puedo ayudar hoy?")

while True:
    try:
        user_input = input("--->").strip()
        if not user_input:
            continue

        # Salida del ciclo
        if user_input.lower() in ["salir", "exit", "quit", "adios", "adiós", "hasta luego"]:
            print(">>> Hasta luego!")
            break
        # Interpretación negativa
        funcion_agente = procesar_input(user_input)
        if funcion_agente is None:
            print(">>> No estoy seguro de como procesar tu solicitud. Prueba con: 'clima ciudad' o 'precio acción'")
        else:
            input_sanitizado = sanitizar(user_input)

            respuesta = funcion_agente(driver, input_sanitizado)
            print(f">>> {respuesta}")

    except KeyboardInterrupt as e:
        print("\n >>> Hasta pronto!!")
    except Exception as e:
        print(f">>> Ocurrió un error: {e}")

driver.quit()
