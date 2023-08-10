import requests
import schedule
import os
from dotenv import load_dotenv
_ = load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']



defaultUrl = "https://scanner.tradingview.com/crypto/scan"


def filterPairs(url=defaultUrl):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': '1997',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }

    params = '''
    {"filter":[{"left":"exchange","operation":"in_range","right":["BINANCE","BYBIT","COINBASE","OKX"]},{"left":"centralization","operation":"equal","right":"cex"},{"left":"change|1","operation":"egreater","right":0.5},{"left":"change|15","operation":"in_range","right":[0.2,1]},{"left":"active_symbol","operation":"equal","right":true},{"left":"ROC","operation":"egreater","right":0},{"left":"24h_vol_change|5","operation":"egreater","right":50},{"left":"currency","operation":"in_range","right":["USD","USDC","USDT"]}],"options":{"lang":"en"},"filter2":{"operator":"and","operands":[{"operation":{"operator":"or","operands":[{"expression":{"left":"type","operation":"in_range","right":["spot"]}}]}},{"operation":{"operator":"or","operands":[{"expression":{"left":"Recommend.All","operation":"in_range","right":[0.1,0.5]}},{"expression":{"left":"Recommend.All","operation":"in_range","right":[-0.1,0.1]}},{"expression":{"left":"Recommend.All","operation":"in_range","right":[0.5,1]}}]}},{"operation":{"operator":"or","operands":[{"expression":{"left":"Recommend.MA","operation":"in_range","right":[0.1,0.5]}},{"expression":{"left":"Recommend.MA","operation":"in_range","right":[-0.1,0.1]}},{"expression":{"left":"Recommend.MA","operation":"in_range","right":[0.5,1]}}]}},{"operation":{"operator":"or","operands":[{"expression":{"left":"Recommend.Other","operation":"in_range","right":[0.1,0.5]}},{"expression":{"left":"Recommend.Other","operation":"in_range","right":[-0.1,0.1]}},{"expression":{"left":"Recommend.Other","operation":"in_range","right":[0.5,1]}}]}}]},"markets":["crypto"],"symbols":{"query":{"types":[]},"tickers":[]},"columns":["base_currency_logoid","currency_logoid","name","exchange","close","ROC","24h_vol_change|5","change|5","change|15","change|60","Recommend.Other","Recommend.All","description","type","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"24h_vol|5","sortOrder":"desc"},"price_conversion":{"to_symbol":false},"range":[0,150]}
    '''
    response = requests.request("POST", url, headers=headers, data=params)
    print(response.text)
    sendToTelegram(response.text)

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




def main():
    schedule.every(1).seconds.do(filterPairs)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()