import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome import ChromeDriverManager  

driver_path = ChromeDriverManager().install()

if os.path.basename(driver_path) != "chromedriver":
    dir_path = os.path.dirname(driver_path)
    binary_path = os.path.join(dir_path, "chromedriver")
    if os.path.exists(binary_path):
        driver_path = binary_path

os.chmod(driver_path, 0o755)

driver = webdriver.Chrome(service=Service(driver_path))

driver.get("https://www.google.com")

sleep(20)

driver.get("https://hybridge.education")

sleep(3)

driver.get("https://openai.com")

sleep(5)