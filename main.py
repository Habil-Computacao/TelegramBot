import time
import requests
from src.betsulApi import BetsulApi
from src.oddCalculator import OddCalculator


class TipsterBot:
    def __init__(self):
        token = '1401583441:AAEPwUV3RzQMAtGBsu_0gkju09Nl04YxKkk'
        self.groupId = '-407721573'
        self.botUrl = f'https://api.telegram.org/bot{token}/'
        self.soccerEmoji = u'\U000026BD'
        self.pinEmoji = u'\U0001F4CC'
        self.arrows = {"home": "u'\U0001F519", "draw": "u'\U0001F51B", "away": "u'\U0001F51C"}
        self.hand = u'\U0001F449'
        self.alert = u'\U000026A0'
        self.earth = u'\U0001F30F'
        self.betApi = BetsulApi()
        self.oddCalculator = OddCalculator()

    def start(self):
        fakedata = [{'score': '1:0', 'time': '35', 'league-country': ['Primeira A - Abertura', 'Colômbia'],
                     'odds': [170, 305, 540], 'teams': {'home': 'Millonarios', 'away': 'Once Caldas'},
                     'stats': {'goalAttempts': {'home': 0, 'away': 5}, 'shotsOff': {'home': 0, 'away': 5},
                               'dangerousAttacks': {'home': 1, 'away': 70}, 'corners': {'home': 1, 'away': 15}},
                     'id': '24847098'}]

        while True:
            gameList = self.oddCalculator.run(fakedata)
            print(gameList)

            for gameDict in gameList:
                for game in gameDict:
                    message = self.createMessage(gameDict[game])
                    self.sendMessage(message, self.groupId)

            time.sleep(30)

    def createMessage(self, game):
        home = game['teams']['home']
        away = game['teams']['away']
        odd = game['odd']
        score = game['score']
        appm = game['appm']

        message = f"""{self.soccerEmoji} Tipster Bot {self.soccerEmoji}\n\n{self.pinEmoji} {home} VS {away}\
                    \n\n{self.hand} Odd atual: {odd}\n{self.hand} Pontuação: {score}\n{self.hand} APPM: {appm}\
                    \n\n{self.alert}\n\n{self.earth}: """
        return message

    def sendMessage(self, resposta, chat_id):
        chatLink = f'{self.botUrl}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(chatLink)


tipsterBot = TipsterBot()
tipsterBot.start()
