import os
import requests
from dotenv import load_dotenv
_ = load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def sendToTelegram(message):
    telegram_message = f"{message}"
    params = (
        ('chat_id',TELEGRAM_CHAT_ID),
        ('text',telegram_message),
        ('parse_mode',"Markdown"),
        ('disable_web_page_preview',"yes")
    )
    telegram_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    telegram_req = requests.post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    if telegram_status == 200:
        print(f"INFO: Telegram Message sent")
    else:
        print("Telegram Error")

# def sendToWechat(message):
#     # do