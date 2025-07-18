#Para usar esse arquivo, o HEBHOOK, API e NGROK devem estar ativos e configurados, este é somente a configurção de envio
#Ele vai servir para enviar quantas mensagens quiser, porém deve ser feito com cuidado


import json
import requests
import random
import logging
import os
import time
from dotenv import load_dotenv

# Configuração do log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#  .env com todas as diretrizes corretas
load_dotenv()
API_KEY = os.getenv("API_KEY")
URL_ENVIO = os.getenv("WTT_API_URL")
MENSAGENS_PATH = os.getenv("MENSAGENS_PATH")
NUMEROS_PATH = os.getenv("NUMEROS_PATH")

# Checagem das variáveis e arquivos do .env
if not API_KEY:
    logging.error("API_KEY não definida no .env!")
    exit(1)
if API_KEY.startswith('"') and API_KEY.endswith('"'):
    API_KEY = API_KEY[1:-1]  # Remove aspas, opis algumas Key tem "#" então previne erros
if not URL_ENVIO:
    logging.error("WTT_API_URL não definida no .env!")
    exit(1)
if not MENSAGENS_PATH or not os.path.exists(MENSAGENS_PATH):
    logging.error(f"MENSAGENS_PATH inválido: {MENSAGENS_PATH}")
    exit(1)
if not NUMEROS_PATH or not os.path.exists(NUMEROS_PATH):
    logging.error(f"NUMEROS_PATH inválido: {NUMEROS_PATH}")
    exit(1)

# leitura de mensagem e destinatários
with open(MENSAGENS_PATH, encoding='utf-8') as fmsg:
    mensagens = json.load(fmsg)
with open(NUMEROS_PATH, encoding='utf-8') as fcont:
    pessoas = json.load(fcont)

logging.info(f"Total de contatos lidos: {len(pessoas)}")

resultado_envios = []  # Guardar envios

# Envio de mensagens em massa, uma a uma.
for i, pessoa in enumerate(pessoas, start=1):
    nome, numero_destinatario = list(pessoa.items())[0]

    # Envio de mensagem aleatória, se seus leads froem limpos, pode comentar essa parte, eu uso pois neste uso em específico não está
    mensagem = random.choice(mensagens)
    mensagem_id = mensagem.get("id")
    texto_mensagem = mensagem.get("texto")

    payload = json.dumps({
        "number": numero_destinatario,
        "textMessage": {"text": texto_mensagem}
    })

    headers = {
        'Content-Type': 'application/json',
        'apikey': API_KEY
    }

    logging.info(f"Enviando para {nome} ({numero_destinatario}): '{texto_mensagem[:30]}...'")

    envio_ok = False
    try:
        response = requests.request("POST", URL_ENVIO, headers=headers, data=payload)
        if response.status_code in (200, 201):
            logging.info(f"Mensagem enviada com sucesso para {nome} ({numero_destinatario})")
            envio_ok = True
        else:
            logging.warning(f"Falha ao enviar para {nome} ({numero_destinatario}). Código HTTP {response.status_code}")
            logging.warning(f"Detalhe do erro: {response.text}")
    except Exception as e:
        logging.error(f"Erro ao enviar para {nome} ({numero_destinatario}): {e}")

    # Registra o envio no resultado final
    resultado_envios.append({
        "nome": nome,
        "numero": numero_destinatario,
        "mensagem_id": mensagem_id,
        #tire o comnetário caso queira que o texto seja incluso, eu prefiro sem
       # "mensagem_texto": texto_mensagem,
        "status": "enviado" if envio_ok else "falha"
    })

    # -------- PAUSAS DE SEGURANÇA --------
    #aqui eu adicionei uma segurança para bloqueio, altere como achar necessário
    
    if i % 50 == 0:
        logging.info("Pausa de segurança: aguardando 2 minutos após 50 envios...")
        time.sleep(120)  # 2 minutos de pausa após cada 50 envios
    else:
        time.sleep(5)    # 5 segundos entre cada envio normal

# Salvar
with open("saida_envios.json", "w", encoding="utf-8") as fout:
    json.dump(resultado_envios, fout, ensure_ascii=False, indent=2)

logging.info("Todos os envios finalizados! Resultado salvo em saida_envios.json.")