import time
import requests
from src.betsulApi import BetsulApi


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

    def start(self):
        update_id = None
        betApi = BetsulApi()
        gameList = betApi.run()

        while True:
            message = self.createMessage()
            self.sendMessage(message, self.groupId)
            time.sleep(10)

    def createMessage(self):
        message = f"""{self.soccerEmoji} Tipster Bot {self.soccerEmoji}\n\n{self.pinEmoji} \
                    \n\n{self.hand}\n{self.hand}\n{self.hand}\n\n{self.alert}\n\n{self.earth} """
        return message

    def sendMessage(self, resposta, chat_id):
        chatLink = f'{self.botUrl}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(chatLink)


bot = TipsterBot()
bot.start()
