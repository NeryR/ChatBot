import os
import re
import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

options = Options()
#options.add_argument("--headless=new")
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

# Use Chromium installed by the system rather than relying only on ChromeDriver's default browser discovery.
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

print("Abrir Google")
driver.get("https://www.google.com")

sleep(5)

print("Abrir Hybridge")
driver.get("https://hybridge.education")

sleep(3)

print("Abrir OpenAI")
driver.get("https://openai.com")

sleep(5)