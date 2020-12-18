import time

from src.betsulApi import BetsulApi
from src.oddCalculator import OddCalculator

betApi = BetsulApi()
oddCalculator = OddCalculator()

fakedata = [{'score': '1:0', 'time': '35', 'league-country': ['Primeira A - Abertura', 'Colômbia'],
             'odds': [170, 305, 540], 'teams': {'home': 'Millonarios', 'away': 'Once Caldas'},
             'stats': {'goalAttempts': {'home': 0, 'away': 5}, 'shotsOff': {'home': 0, 'away': 5},
                       'dangerousAttacks': {'home': 1, 'away': 70}, 'corners': {'home': 1, 'away': 15}},
             'id': '24847098'}]

while True:
    print(oddCalculator.run(fakedata))
    time.sleep(60)
