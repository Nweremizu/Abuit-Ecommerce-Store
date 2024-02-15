import requests


def paypalCurrencyConverter(amount: float):
    url = f'https://v6.exchangerate-api.com/v6/4bccf8b67edab01d68e7701b/pair/NGN/USD/{amount}'
    try:
        response = requests.get(url)
        data = response.json()
        return float(data['conversion_result'])
    except :
        return 100.00


def nairaCurrencyConverter(amount: float):
    url = f'https://v6.exchangerate-api.com/v6/4bccf8b67edab01d68e7701b/pair/USD/NGN/{amount}'
    try:
        response = requests.get(url)
        data = response.json()
        return float(data['conversion_result'])
    except:
        return 100.00
