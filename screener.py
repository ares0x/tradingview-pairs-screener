import requests
import schedule
import json

from notify import sendToTelegram

# screener 接口
defaultUrl = "https://scanner.tradingview.com/crypto/scan"
defaultLanguage = "en"

def filterPairs(url=defaultUrl):
    language = 'zh'
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
    load_data = json.loads(response.text)
    data = load_data.get("data")
    # print(data)
    parsed_data = []
    for entry in data:
        tmp = entry['d'][11]
        if language == 'en':
            parsed_entry = {
                'detail':{
                    'pair': entry['d'][2],
                    'exchanges': entry['d'][3],  
                    'price': entry['d'][4],
                    'volume': entry['d'][5],
                    'hight': entry['d'][4],
                    'vol 24h change %': str(entry['d'][6])+'%',
                }
            }
            if tmp > 0.0 and tmp < 0.5:
                parsed_entry['technical rating'] = 'buy'
            elif tmp > 0.5:
                parsed_entry['technical rating'] = 'strong buy'

        else:
            parsed_entry = {
                'detail':{
                    '币对': entry['d'][2],
                    '交易所': entry['d'][3], 
                    '价格': entry['d'][4],
                    '成交量': str(entry['d'][5])+'k',
                    '最高价格': entry['d'][4],
                    '24小时成交量变化 %': str(entry['d'][6])+'%',
                }
            }
            if tmp > 0.0 and tmp < 0.5:
                parsed_entry['技术指标'] = 'buy'
            elif tmp > 0.5:
                parsed_entry['技术指标'] = 'strong buy'

        parsed_data.append(parsed_entry)
        
    sendToTelegram(parsed_data)

def main():
    # 每秒执行一次
    schedule.every(5).seconds.do(filterPairs)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()