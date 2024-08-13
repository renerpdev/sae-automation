import os
import time
import logging
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("script.log"),
        logging.StreamHandler()
    ]
)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def extract_version(metadata_file):
    with open(metadata_file, 'r') as file:
        data = json.load(file)
        return data.get('aliases', {}).get('canary', None)

# Extraer la versión canary usando json
chromedriver_version = extract_version('./chromedriver/.metadata')
chrome_binary_version = extract_version('./chrome/.metadata')

if not chromedriver_version or not chrome_binary_version:
    raise ValueError("No se pudo extraer la versión canary de uno o ambos archivos de metadata")

# Obtener las rutas desde el archivo metadata
chrome_driver_path=f'./chromedriver/mac_arm-{chromedriver_version}/chromedriver-mac-arm64/chromedriver'
chrome_binary_path=f'./chrome/mac_arm-{chrome_binary_version}/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'

# Configuración de Selenium para usar Chrome Canary
options = Options()
options.headless = True
options.binary_location = chrome_binary_path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Configuración de Slack
slack_token = os.getenv('SLACK_TOKEN')
client = WebClient(token=slack_token)
channel_id = os.getenv('CHANNEL_ID')

def send_slack_message(message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {slack_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'channel': channel_id,
        'text': message,
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        logging.info('Message sent successfully!')
        logging.info(response.json())
    else:
        logging.info('Failed to send message')
        logging.info(response.status_code, response.text)

# Función principal
def check_page():
    url_prefix = "https://sae.corteelectoral.gub.uy/sae/agendarReserva/Paso1.xhtml"
    page_url = f"{url_prefix}?e=1&a=1&r=1"
    driver.get(page_url)

    try:
        # Esperar hasta que el botón esté presente y hacer clic en él
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.element_to_be_clickable((By.ID, "form:botonElegirHora")))
        button.click()
        logging.info("Botón 'Elegir día y hora' clickeado")

        # Verificar si se ha cargado una nueva página
        time.sleep(3)  # Esperar unos segundos para que la página cargue
        if not driver.current_url.startswith(url_prefix):
            send_slack_message(f"New page loaded: {driver.current_url}")
            return True
    except Exception as e:
        logging.error("Error: %s", e)

    return False

while True:
    first_page_loaded = check_page()
    if first_page_loaded == True:
        break
    time.sleep(0)

while True:
    logging.info('Waiting for user input...')

