import requests
from bs4 import BeautifulSoup


def consulta_dolar():
    url = 'https://dolarhoje.com/'
    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        dollar_value = soup.find('input', {'id': 'nacional'})['value']
        return {"Dolar agora": dollar_value}

    except requests.exceptions.HTTPError as err:
        return False