import json
import requests


class BetsulApi:
    def __init__(self):
        self.body = json.loads('''{
            "filters": {
                "pais": null,
                "tipoEsporte": 1,
                "torneio": null
            },
            "limit": 500,
            "offset": 0,
            "sort": [
                "date-asc"
            ],
            "type": "aovivo"
            }''')
        self.baseUrl = 'https://www.betsul.com/web/v2/eventos'
        self.gameUrl = 'https://widgets.fn.sportradar.com/betwaywidget/pt/Etc:UTC/gismo/match_detailsextended/'

    def run(self):
        events = requests.post(url=self.baseUrl, json=self.body).json()['eventos']
        for count, event in enumerate(events):
            # Access one's game info
            _indexID = int(str(event).index('matchID'))
            _matchID = str(event)[_indexID + 10:_indexID + 18]
            gameInfo = requests.get(url=self.gameUrl + _matchID).json()['doc'][0]['data']

            # Stop when games didn't started
            if event['periodo'] == 'Não Iniciado':
                break

            home = gameInfo['teams']['home']
            away = gameInfo['teams']['away']
            league = event['nomeCampeonato']
            country = event['nomePais']

            corners = gameInfo['values']['124']['value'] if gameInfo['values'].get('124') else {'home': 0, 'away': 0}
            dangerousAttacks = gameInfo['values']['1029']['value'] if gameInfo['values'].get('1029') else {'home': 0, 'away': 0}
            goalAttempts = gameInfo['values']['goalattempts']['value'] if gameInfo['values'].get('goalattempts') else {'home': 0, 'away': 0}
            score = event['placar']
            matchTime = event['tempoDecorridoMin']

            collection = {'id': _matchID, 'home': home, 'away': away, 'score': score, 'time': matchTime,
                          'goalAttempts': goalAttempts, 'dangerousAttacks': dangerousAttacks, 'corners': corners,
                          'league': league, 'country': country}
            print(collection)


'''{
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
}'''