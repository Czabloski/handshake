import os
import time
import requests
import schedule
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Carrega variáveis do .env
load_dotenv()

URL = os.getenv("URL_ENDPOINT")
URL_HEALTH = os.getenv("URL_ENDPOINT_HEALTH")
INTERVALO = int(os.getenv("INTERVALO_SEGUNDOS", 60))
TIMEOUT = int(os.getenv("TIMEOUT", 5))
MAX_DURATION = int(os.getenv("MAX_DURATION_MINUTES", 0))  # 0 = indefinido

USER = os.getenv("API_USER")
PASSWORD = os.getenv("API_PASSWORD")

# Configuração de log
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/handshake.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Tempo de término (se definido)
end_time = datetime.now() + timedelta(minutes=MAX_DURATION) if MAX_DURATION > 0 else None

def check_handshake():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        payload = {"user": USER, "password": PASSWORD}
        headers = {"Content-Type": "application/json"}
        response = requests.post(URL, json=payload, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            logging.info(f"{timestamp} - {URL} - OK - Status {response.status_code}")
        else:
            logging.error(f"{timestamp} - {URL} - FALHA - Status {response.status_code}")
    except Exception as e:
        logging.error(f"{timestamp} - {URL} - ERRO - {str(e)}")

def check_healthshake():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        payload = {"user": USER, "password": PASSWORD}
        headers = {"Content-Type": "application/json"}
        response = requests.post(URL_HEALTH, json=payload, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            logging.info(f"{timestamp} - {URL_HEALTH} - OK - Status {response.status_code}")
        else:
            logging.error(f"{timestamp} - {URL_HEALTH} - FALHA - Status {response.status_code}")
    except Exception as e:
        logging.error(f"{timestamp} - {URL_HEALTH} - ERRO - {str(e)}")

# ✅ Agenda as duas funções antes do loop
schedule.every(INTERVALO).seconds.do(check_handshake)
schedule.every(INTERVALO).seconds.do(check_healthshake)

print(f"✅ Serviço iniciado. Consultando {URL} e {URL_HEALTH} a cada {INTERVALO}s...")
if end_time:
    print(f"⏳ Tempo de execução: {MAX_DURATION} minutos")

# ✅ Um único loop principal
while True:
    schedule.run_pending()
    time.sleep(1)
    if end_time and datetime.now() >= end_time:
        print("⏹️ Tempo máximo atingido. Serviço encerrado.")
        break