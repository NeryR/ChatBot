import os
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from utils.sanitizar import sanitizar

# --- Configuración de Selenium ---
# Se utilizan opciones para ejecutar el navegador de forma silenciosa (headless)
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-client-side-phishing-detection")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-sync")
options.add_argument("--metrics-recording-only")
options.add_argument("--no-first-run")
options.add_argument("--safebrowsing-disable-auto-update")
options.binary_location = "/usr/bin/chromium-browser"

RE_CHROME_VERSION = re.compile(r"(\d+\.\d+\.\d+\.\d+)")

def get_chromium_version(binary_path="/usr/bin/chromium-browser"):
    try:
        proc = subprocess.run([binary_path, "--version"], capture_output=True, text=True, timeout=10)
        output = (proc.stdout or proc.stderr or "").strip()
        match = RE_CHROME_VERSION.search(output)
        return match.group(1) if match else None
    except Exception:
        return None

chromium_version = get_chromium_version()
if chromium_version:
    driver_path = ChromeDriverManager(driver_version=chromium_version, chrome_type=ChromeType.CHROMIUM).install()
else:
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

if os.path.basename(driver_path) != "chromedriver":
    dir_path = os.path.dirname(driver_path)
    binary_path = os.path.join(dir_path, "chromedriver")
    if os.path.exists(binary_path):
        driver_path = binary_path

os.chmod(driver_path, 0o755)

driver = webdriver.Chrome(service=Service(driver_path), options=options)

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
