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
INTERVALO = int(os.getenv("INTERVALO_SEGUNDOS", 60))
TIMEOUT = int(os.getenv("TIMEOUT", 5))
MAX_DURATION = int(os.getenv("MAX_DURATION_MINUTES", 0))  # 0 = indefinido

# Configuração de log
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/handshake.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Tempo de término (se definido)
end_time = None
if MAX_DURATION > 0:
    end_time = datetime.now() + timedelta(minutes=MAX_DURATION)

def check_handshake():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(URL, timeout=TIMEOUT)
        if response.status_code == 200:
            logging.info(f"{timestamp} - OK - Status {response.status_code}")
        else:
            logging.error(f"{timestamp} - FALHA - Status {response.status_code}")
    except Exception as e:
        logging.error(f"{timestamp} - ERRO - {str(e)}")


# Agenda execução
schedule.every(INTERVALO).seconds.do(check_handshake)

print(f"✅ Serviço iniciado. Consultando {URL} a cada {INTERVALO}s...")
if end_time:
    print(f"⏳ Tempo de execução: {MAX_DURATION} minutos")

# Loop principal
while True:
    schedule.run_pending()
    time.sleep(1)
    if end_time and datetime.now() >= end_time:
        print("⏹️ Tempo máximo atingido. Serviço encerrado.")
        break

