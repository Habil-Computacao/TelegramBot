import json
import requests
from typing import Tuple, Dict


class BetsulApi:
    def __init__(self):
        self.body = json.loads('''{"filters": {"pais": null,"tipoEsporte": 1,"torneio": null},"limit": 500,"offset": 0,
        "sort": ["date-asc"],"type": "aovivo"}''')
        self.baseUrl = 'https://www.betsul.com/web/v2/eventos'
        self.matchLink = 'https://www.bet365.com/%23/AX/K%5E'
        self.gameUrl = 'https://lmt.fn.sportradar.com/demolmt/en/Etc:UTC/gismo/match_detailsextended/'
        self.gameTimelineUrl = 'https://lmt.fn.sportradar.com/common/br/Etc:UTC/gismo/match_timeline/'

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
        corners = self.verifyGameValue(gameData, '124')
        dangerousAttacks = self.verifyGameValue(gameData, '1029')
        ballPossession = self.verifyGameValue(gameData, '110')

        return {'stats': {'dangerousAttacks': dangerousAttacks, 'corners': corners, 'ballPossession': ballPossession}}

    @staticmethod
    def getEventValues(eventData) -> dict:
        score = eventData['placar']
        matchTime = eventData['tempoDecorridoMin']

        return {'score': score, 'time': matchTime}

    def getGameName(self, matchId):
        teams = requests.get(self.gameTimelineUrl + matchId).json()['doc']['data']['match']['teams']

        return {'teams': {'home': teams['home']['mediumname'], 'away': teams['away']['mediumname']}}

    def run(self) -> list:
        _events = self.requestEvents()
        [_eventsData, _gamesData, _matchIds] = self.getGameData(_events)
        result = []

        for event, game, matchId in zip(_eventsData, _gamesData, _matchIds):
            _temp = self.getEventValues(event)
            _temp.update(self.getGameValues(game))
            _temp.update(self.getGameName(matchId))

            home = _temp['teams']['home'].replace(' ', '%2520')
            away = _temp['teams']['away'].replace(' ', '%2520')
            finalLink = self.matchLink + home + '%2520v%2520' + away
            _temp.update({'id': matchId, 'matchLink': finalLink})

            result.append(_temp)
        return result
