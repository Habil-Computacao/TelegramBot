import requests
import time
import json
import os
import requests
from requests_html import HTMLSession

body = json.loads('''{
    "filters": {
        "pais": null,
        "tipoEsporte": 1,
        "torneio": null
    },
    "include": [
        "weekdays",
        "sportfilters",
        "cabecalho"
    ],
    "limit": 500,
    "offset": 0,
    "sort": [
        "date-asc"
    ],
    "type": "aovivo"
    }''')
token = '1401583441:AAEPwUV3RzQMAtGBsu_0gkju09Nl04YxKkk'
baseUrl = 'https://www.betsul.com/web/v2/eventos'
bot_url = f'https://api.telegram.org/bot{token}/getUpdates'

allEvents = requests.post(url=baseUrl, json=body)

for item in allEvents:
    print(item)
