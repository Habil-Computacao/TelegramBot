from typing import List, Dict, Union, Set, Tuple


class OddCalculator:
    def __init__(self):
        self.matchTime1 = 35
        self.matchTime2 = 82
        self.matchTimeOffset = 5

        self.constAPPM1 = 1.2
        self.constAPPM2 = 1.0
        self.constAPPMOffset = 0.1

        self.constCorners1 = 3
        self.constCorners2 = 7

        self.matchs = {}
        ''' {
            '12345678': False,
            '22345678': False,
            '32345678': True
        } '''

    def run(self, data: List[Dict[str, int or str or dict or list]]) -> List[Dict[int, dict]]:
        response = []
        _dataIds = set()
        print('\n')
        for match in data:
            _matchTime = int(match['time'])
            _matchId = match['id']
            _matchStats = match['stats']
            _verification = 0
            _dataIds.add(_matchId)

            if self.matchTime1 - self.matchTimeOffset < _matchTime < self.matchTime1 + self.matchTimeOffset \
                    or self.matchTime2 - self.matchTimeOffset < _matchTime < self.matchTime2 + self.matchTimeOffset:
                if self.matchs.get(_matchId) is not None:
                    if self.matchs[_matchId] or _matchTime < 45:
                        continue
                _verification = self.oddVerification(_matchStats['dangerousAttacks'], _matchTime,
                                                     _matchStats['corners'], match['score'])
                if type(_verification) is not int:
                    self.matchs.update({_matchId: False}) if _matchTime <= 45 else self.matchs.update({_matchId: True})
                    _verification.update({'teams': match['teams'], 'ballPossession': _matchStats['ballPossession'],
                                          'matchLink': match['matchLink']})
                    response.append({_matchId: _verification})

        self.clearMemory(set(_dataIds))
        print(response)
        return response

    @staticmethod
    def calcAPPM(dangerousAttacks: int, matchTime: int) -> int or float:
        return dangerousAttacks / matchTime if matchTime > 0 else 0

    @staticmethod
    def calcCG(goalAttempts: int, shotsOff: int, corners: int) -> int:
        return goalAttempts + shotsOff + corners

    @staticmethod
    def getLoserStat(stat: Dict[str, int], teamSide: str) -> int:
        return stat[teamSide]

    @staticmethod
    def getLoser(score: str) -> Tuple[str, List[int]]:
        [home, away] = score.split(':')
        home = int(home)
        away = int(away)
        team = 'away' if away < home else 'home' if away > home else 'draw'
        return team, [home, away]

    def oddVerification(self, dangerousAttacks: Dict[str, int], matchTime: int, corners: Dict[str, int],
                        score: str) -> Union[Dict[str, int or float or str], int]:
        [_teamSide, _scoreInt] = self.getLoser(score)

        if _teamSide == 'draw':
            _teamSide = 'away' if self.calcAPPM(self.getLoserStat(dangerousAttacks, 'away'), matchTime) \
                                  > self.calcAPPM(self.getLoserStat(dangerousAttacks, 'home'), matchTime) else 'home'

        dangerousAttacks = self.getLoserStat(dangerousAttacks, _teamSide)
        corners = self.getLoserStat(corners, _teamSide)

        matchTime = int(matchTime)

        _passed = False
        _constAPPM = 0
        _constCorners = 0

        if matchTime <= 45:
            _constAPPM = self.constAPPM1
            _constCorners = self.constCorners1
        elif matchTime > 45:
            _constAPPM = self.constAPPM2
            _constCorners = self.constCorners2

        currentAPPM = self.calcAPPM(dangerousAttacks, matchTime)
        if _constAPPM - self.constAPPMOffset <= currentAPPM\
                and corners > _constCorners\
                and -2 <= _scoreInt[0] - _scoreInt[1] <= 2:
            _passed = True

        return {'score': score, 'appm': currentAPPM, 'corners': corners} if _passed else 0

    def clearMemory(self, events: Set[str]):
        matchs = set()
        for item in self.matchs:
            matchs.add(item)

        toDelete = events.symmetric_difference(matchs)

        for item in toDelete:
            if self.matchs.get(item) is not None:
                self.matchs.pop(item)
