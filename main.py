import time
import requests
from src.betsulApi import BetsulApi
from src.oddCalculator import OddCalculator


class TipsterBot:
    def __init__(self):
        token = '1401583441:AAEPwUV3RzQMAtGBsu_0gkju09Nl04YxKkk'
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
                          'matchLink': 'https://www.bet365.com/#/AX/K%5EMillonarios%20v%20Once%20Caldas', 'id': '24847098'}]

    def start(self):
        while True:
            allGames = self.betApi.run()
            gameList = self.oddCalculator.run(allGames)

            for gameDict in gameList:
                for game in gameDict:
                    message = self.createMessage(gameDict[game])
                    self.sendMessage(message)

            time.sleep(10)

    def createMessage(self, game):
        home = game['teams']['home']
        away = game['teams']['away']
        finalLink = game['matchLink']
        scoreHome = game['score'][0]
        scoreAway = game['score'][2]
        appm = game['appm']
        corners = game['corners']
        possessionHome = game['ballPossession']['home']
        possessionAway = game['ballPossession']['away']
        print(finalLink)

        message = f"""{self.soccerEmoji} Tipster Bot {self.soccerEmoji}\n\n{self.pinEmoji} {home} {scoreHome} VS {scoreAway} {away}\
                    \n\n{self.hand}Posse de Bola: {possessionHome}% vs {possessionAway}%\
                    \n{self.hand}APPM Variando Entre {appm - 0.1} e {appm + 0.1} \n\n{self.alert} Atenção, linha do canto aberta para: {corners + 1} escanteios.\n\
                    \n{self.earth} -> {finalLink}"""

        return message

    def sendMessage(self, message):
        chatLink = f'{self.botUrl}sendMessage?chat_id={self.groupId}&text={message}'
        requests.get(chatLink)


tipsterBot = TipsterBot()
tipsterBot.start()
