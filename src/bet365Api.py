import time
from .bet365 import ApiBet365


class Bet365Api:
    def __init__(self):
        self.api = ApiBet365()
        self.lists = {
            'BrasileiraoA': [],
            'BrasileiraoB': [],
            'CariocaB': [],
            'PortugalPrimeiraLiga': [],
            'ChileB': []
        }
        self.urls = {
            'BrasileiraoA': 'https://www.bet365.com/#/AC/B1/C1/D13/E51310447/F2/',
            'BrasileiraoB': 'https://www.bet365.com/#/AC/B1/C1/D13/E51340799/F2/',
            'CariocaB': 'https://www.bet365.com/#/AC/B1/C1/D13/E52619596/F2/',
            'PortugalPrimeiraLiga': 'https://www.bet365.com/#/AC/B1/C1/D13/E51878880/F2/',
            'ChileB': 'https://www.bet365.com/#/AC/B1/C1/D13/E51971243/F2/'
        }

    def updateList(self, key: str):
        self.lists[key] = self.api.odds(self.urls[key])

    def dev(self):
        self.updateList('BrasileiraoA')
        print(self.lists)
        time.sleep(3)
