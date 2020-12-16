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
gameUrl = 'https://widgets.fn.sportradar.com/betwaywidget/pt/Etc:UTC/gismo/match_detailsextended/'
bot_url = f'https://api.telegram.org/bot{token}/getUpdates'

events = requests.post(url=baseUrl, json=body).json()['eventos']

for count, event in enumerate(events):
    indexID = int(str(event).index('matchID'))
    matchID = str(event)[indexID + 10:indexID + 18]

    response = requests.get(url=gameUrl+matchID).json()
    data = response['doc'][0]['data']

    home = data['teams']['home']
    away = data['teams']['away']
    league = event['nomeCampeonato']
    country = event['nomePais']

    homeGoals = []
    homeAttacks = []
    homeKicks = []
    homeCorners = []

    awayGoals = []
    time = event['tempoDecorridoMin']

    collection = [home, away, time, league, country]
    print(collection)
