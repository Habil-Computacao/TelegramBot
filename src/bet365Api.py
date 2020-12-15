import string
import time
from soccerapi.api import ApiBet365


class Bet365Api:
    def __init__(self):
        self.api = ApiBet365()
        self.lists = {
            'BrasileiraoA': [],
            'BrasileiraoB': []
        }
        self.urls = {
            'BrasileiraoA': 'https://www.bet365.com/#/AC/B1/C1/D13/E51310447/F2/',
            'BrasileiraoB': 'https://www.bet365.com/#/AC/B1/C1/D13/E51340799/F2/'
        }

    def updateList(self, key: string):
        self.lists[key] = self.api.odds(self.urls[key])

    def dev(self):
        self.updateList('BrasileiraoA')
        print(self.lists)
        time.sleep(5)
        self.updateList('BrasileiraoB')
        print(self.lists)
        time.sleep(20)
