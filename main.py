import os
import time
import logging
import json
import requests
import schedule
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

# Datos del usuario
user_id = os.getenv('ID')
user_name = os.getenv('NAME')
user_last_name = os.getenv('LAST_NAME')

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

first_page_url = "https://sae.corteelectoral.gub.uy/sae/agendarReserva/Paso1.xhtml"
second_page_url = "https://sae.corteelectoral.gub.uy/sae/agendarReserva/Paso2.xhtml"
third_page_url = "https://sae.corteelectoral.gub.uy/sae/agendarReserva/Paso3.xhtml"

def wait_until_browser_is_ready():
    while driver.execute_script("return document.readyState") != "complete":
        logging.info("Esperando a que la página termine de cargar...")
        time.sleep(0.5)  # Espera corta para no sobrecargar el sistema

# Función para seleccionar una ubicación y luego hacer clic en el botón "Elegir día y hora"
def select_location():
    page_url = f"{first_page_url}?e=1&a=1&r=1"
    driver.get(page_url)

    try:
        # Esperar hasta que el botón esté presente y hacer clic en él
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.element_to_be_clickable((By.ID, "form:botonElegirHora")))
        button.click()
        logging.info("Botón 'Elegir día y hora' clickeado")

        # Esperar hasta que el navegador haya terminado de cargar la página
        wait_until_browser_is_ready()


        if driver.current_url.startswith(second_page_url):
            send_slack_message(f"Second page loaded: {driver.current_url}")
            return True
    except Exception as e:
        logging.error("Error: %s", e)

    return False

# Función para hacer clic en una fecha disponible y luego en el botón "Completar Datos"
def select_available_date():
    try:
        # Esperar hasta que el elemento con el selector esté presente y hacer clic
        wait = WebDriverWait(driver, 10)
        available_date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-datepicker td.fechaFutura:not(.ui-datepicker-unselectable):not(.ui-state-disabled)")))
        available_date.click()
        logging.info("Fecha disponible clickeada")

        # Esperar hasta que el botón 'Completar Datos' esté presente y hacer clic
        complete_button = wait.until(EC.element_to_be_clickable((By.ID, "form:botonCompletarDatos")))
        complete_button.click()
        logging.info("Botón 'Completar Datos' clickeado")

        # Esperar hasta que el navegador haya terminado de cargar la página
        wait_until_browser_is_ready()

        if driver.current_url.startswith(third_page_url):
            send_slack_message(f"Third page loaded: {driver.current_url}")
            return True
    except Exception as e:
        logging.error("Error al seleccionar la fecha o hacer clic en el botón: %s", e)

    return False

# Función para ingresar datos del usuario y luego hacer click en el botón "Enviar"
def enter_user_details_and_complete():
    # TODO: NOT IMPLEMENTED YET

    # Esperar hasta que el navegador haya terminado de cargar la página
    wait_until_browser_is_ready()

    return False

# Función que se ejecutará cada lunes a las 9:50 AM
def job():
    logging.info("Iniciando el proceso programado para el lunes a las 9:50 AM.")

    # Página 1: Detalles y ubicación
    while True:
        second_page_loaded = select_location()
        if second_page_loaded == True:
            break
        time.sleep(0)

    # Página 2: Día y hora
    while True:
        logging.info('Seleccionando día y hora para la cita...')
        third_page_loaded = select_available_date()
        if third_page_loaded == True:
            break
        time.sleep(0)

    # Página 3: Datos necesarios
    while True:
        logging.info('Ingresando los datos del usuario...')
        details_submitted = enter_user_details_and_complete()
        if details_submitted == True:
            break
        else
            logging.info('Waiting for user input...')

    logging.info('***CITA CREADA CORRECTAMENTE***')


# Programar la tarea para que se ejecute los lunes a las 9:50 AM
schedule.every().monday.at("09:50").do(job)

while True:
    # Verificar si hay alguna tarea pendiente
    schedule.run_pending()
    time.sleep(1)  # Esperar 1 segundo antes de la siguiente verificación

