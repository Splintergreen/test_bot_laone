import os

import requests
from dotenv import load_dotenv

load_dotenv()

CURRENCY_KEY = os.getenv('CURRENCY_KEY')


def convert_currency(from_currency, to_currency, amount):
    '''Конвертация валюты, и обработка ошибок при конвертации.'''
    url = (
        f'https://api.apilayer.com/exchangerates_data/convert?to='
        f'{to_currency}&from={from_currency}&amount={amount}'
        )
    payload = {}
    headers = {
      'apikey': CURRENCY_KEY
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.ConnectionError:
        return '<сетевая ошибка>'
    if response.status_code == 200:
        return response.json().get('result')
    else:
        return '<ошибка на сервере конвертации>'


def get_pet_image():
    '''Получить изображение котика, если нет котика, получить собачку.'''
    url = 'https://api.thecatapi.com/v1/images/search'
    try:
        response = requests.get(url)
    except Exception:
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    if response.status_code == 200:
        response = response.json()
        return response[0].get('url')
    else:
        return '<ошибка на сервере>'


def what_weather(city):
    '''Получение погоды и обработка ошибок при получении.'''
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return '<сетевая ошибка>'
    if response.status_code == 200:
        return response.text
    else:
        return '<ошибка на сервере погоды>'
