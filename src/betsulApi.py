import json
import requests
from typing import Tuple, Dict


class BetsulApi:
    def __init__(self):
        self.body = json.loads('''{"filters": {"pais": null,"tipoEsporte": 1,"torneio": null},"limit": 500,"offset": 0,
        "sort": ["date-asc"],"type": "aovivo"}''')
        self.baseUrl = 'https://www.betsul.com/web/v2/eventos'
        self.gameUrl = 'https://lmt.fn.sportradar.com/demolmt/en/Etc:UTC/gismo/match_detailsextended/'

    def requestEvents(self) -> list:
        return requests.post(url=self.baseUrl, json=self.body).json()['eventos']

    def getGameData(self, events) -> Tuple[list, list, list]:
        allEvents = []
        allGames = []
        allMatchIds = []
        for event in events:
            if event['periodo'] == 'Não Iniciado':
                continue

            _indexID = int(str(event).index('matchID'))
            _matchID = str(event)[_indexID + 10:_indexID + 18]
            _gameData = requests.get(url=self.gameUrl + _matchID).json()['doc'][0]['data']

            allGames.append(_gameData)
            allEvents.append(event)
            allMatchIds.append(_matchID)

        return allEvents, allGames, allMatchIds

    @staticmethod
    def verifyGameValue(gameData, valueName) -> Dict[str, int or str]:
        return gameData['values'][valueName]['value'] if gameData['values'].get(valueName) else {'home': 0, 'away': 0}

    def getGameValues(self, gameData) -> dict:
        home = gameData['teams']['home']
        away = gameData['teams']['away']
        corners = self.verifyGameValue(gameData, '124')
        dangerousAttacks = self.verifyGameValue(gameData, '1029')
        goalAttempts = self.verifyGameValue(gameData, 'goalattempts')

        _attempts = self.verifyGameValue(gameData, '126')
        _blocks = self.verifyGameValue(gameData, '171')

        shotsOff = {'home': _attempts['home'] + _blocks['home'], 'away': _attempts['away'] + _blocks['away']}

        return {'teams': {'home': home, 'away': away},
                'stats': {'goalAttempts': goalAttempts, 'shotsOff': shotsOff, 'dangerousAttacks': dangerousAttacks,
                          'corners': corners}}

    @staticmethod
    def getEventValues(eventData) -> dict:
        score = eventData['placar']
        matchTime = eventData['tempoDecorridoMin']
        league = eventData['nomeCampeonato']
        country = eventData['nomePais']

        _odds = eventData['subeventos']
        oddHome = _odds[0]['cotacao']
        oddDraw = _odds[1]['cotacao']
        oddAway = _odds[2]['cotacao']

        return {'score': score, 'time': matchTime, 'league-country': [league, country],
                'odds': [oddHome, oddDraw, oddAway]}

    def run(self) -> list:
        _events = self.requestEvents()
        [_eventsData, _gamesData, _matchIds] = self.getGameData(_events)
        result = []

        for event, game, matchId in zip(_eventsData, _gamesData, _matchIds):
            _temp = self.getEventValues(event)
            _temp.update(self.getGameValues(game))
            team = _temp['teams']['home'].replace(' ', '%2520')
            matchLink = self.matchLink + team

            _temp.update({'id': matchId, 'matchLink': matchLink})

            result.append(_temp)

        return result
