import time
import requests
from src.betsulApi import BetsulApi
from src.oddCalculator import OddCalculator


class TipsterBot:
    def __init__(self):
        token = '1401583441:AAEPwUV3RzQMAtGBsu_0gkju09Nl04YxKkk'
        self.hello = 'Tipster Bot iniciado!'
        self.bye = 'Tipster Bot sendo desligado!'
        self.groupId = '-407721573'
        self.botUrl = f'https://api.telegram.org/bot{token}/'
        self.url_base = f'https://api.telegram.org/bot{token}/getUpdates'
        self.soccerEmoji = u'\U000026BD'
        self.pinEmoji = u'\U0001F4CC'
        self.arrows = {"home": "u'\U0001F519", "draw": "u'\U0001F51B", "away": "u'\U0001F51C"}
        self.hand = u'\U0001F449'
        self.alert = u'\U000026A0'
        self.earth = u'\U0001F30F'
        self.betApi = BetsulApi()
        self.oddCalculator = OddCalculator()
        self.testData = [{'score': '1:0', 'time': '35',
                          'teams': {'home': 'Millonarios', 'away': 'Once Caldas'},
                          'stats': {'goalAttempts': {'home': 0, 'away': 5}, 'dangerousAttacks': {'home': 1, 'away': 70},
                                    'corners': {'home': 1, 'away': 15}, 'ballPossession': {'home': 18, 'away': 92}},
                          'matchLink': 'https://www.bet365.com/%23/AX/K%5ESarandi%2520v%2520Junior/', 'id': '24847098'}]

    def start(self):
        requests.get(self.botUrl + 'sendMessage?chat_id='+ self.groupId + '&text=' + self.hello)

        while True:
            allGames = self.betApi.run()
            gameList = self.oddCalculator.run(self.testData)

            for gameDict in gameList:
                for game in gameDict:
                    message = self.createMessage(gameDict[game])
                    self.sendMessage(message)

            time.sleep(10)

    def createMessage(self, game):
        messageStruct = []
        home = game['teams']['home']
        away = game['teams']['away']
        matchLink = game['matchLink']
        scoreHome = game['score'][0]
        scoreAway = game['score'][2]
        appmMin = str(game['appm'] - 0.1)
        appmMax = str(game['appm'] + 0.1)
        corners = str(game['corners'] + 1)
        possessionHome = str(game['ballPossession']['home'])
        possessionAway = str(game['ballPossession']['away'])

        messageStruct.append(f'''{self.soccerEmoji}{self.soccerEmoji}{self.soccerEmoji} + Tipster Bot + {self.soccerEmoji}{self.soccerEmoji}{self.soccerEmoji}\n\
                            \n{self.pinEmoji} {home} {scoreHome} + VS + {scoreAway} {away} +\n\
                            \n{self.hand} Posse de Bola: {possessionHome} % vs  {possessionAway}%\
                            \n{self.hand} APPM Variando Entre: {appmMin}  e  {appmMax} +\n\
                            \n{self.alert} Atenção, linha do canto aberta para: {corners} escanteios.\n\
                            \n''')

        messageStruct.append(matchLink)

        return messageStruct

    def sendMessage(self, message):
        chatLinkCorpse = f'{self.botUrl}sendMessage?chat_id={self.groupId}&text={message[0]}'
        chatLinkMatch = f'{self.botUrl}sendMessage?chat_id={self.groupId}&text={message[1]}'

        requests.get(chatLinkCorpse)
        requests.get(chatLinkMatch)


tipsterBot = TipsterBot()
tipsterBot.start()
