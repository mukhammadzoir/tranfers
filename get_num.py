import requests
import fake_useragent


def get_binance_avr_rates(type='BUY', fiat='RUB', asset="USDT", pay='TinkoffNew'):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    user = fake_useragent.UserAgent().random
    headers = {
        'accept': "*/*",
        'user-agent': user
    }
    if fiat=='KZT':
            params = {
            "asset": f"{asset}",
            "countries": [],
            "fiat": f"{fiat}",
            "merchantCheck": False,
            "page": 1,
            "payTypes": [f"{pay}"],
            "proMerchantAds": False,
            "publisherType": None, 
            "rows": 10,
            "tradeType": f"{type}",
            "transAmount": 5000,
        }
    else:
        params = {
            "asset": f"{asset}",
            "countries": [],
            "fiat": f"{fiat}",
            "merchantCheck": False,
            "page": 1,
            "payTypes": [f"{pay}"],
            "proMerchantAds": False,
            "publisherType": 'merchant',        
            "rows": 10,
            "tradeType": f"{type}",
            "transAmount": 1000,
        }
    prices = []

    response = requests.post(url=url, headers=headers, json=params).json()
    for i in range(0, 8):
        price = response['data'][i]["adv"]['price']
        prices.append(float(price))
    avgp = round(sum(prices)/len(prices),4)
    return avgp
