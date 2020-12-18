from typing import List, Dict, Union


class OddCalculator:
    def __init__(self):
        self.matchTime1 = 35
        self.matchTime2 = 82
        self.matchTimeOffset = 5

        self.constAPPM1 = 1.2
        self.constAPPM2 = 1.0
        self.constCG1 = 9
        self.constCG2 = 15
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
        for match in data:
            _matchTime = int(match['time'])
            _matchId = match['id']
            _matchStats = match['stats']
            _verification = 0
            if self.matchTime1 - self.matchTimeOffset < _matchTime < self.matchTime1 + self.matchTimeOffset or self.matchTime2 - self.matchTimeOffset < _matchTime < self.matchTime2 + self.matchTimeOffset:
                if self.matchs.get(_matchId):
                    if self.matchs[_matchId] or _matchTime < 45:
                        continue
                _verification = self.oddVerification(_matchStats['dangerousAttacks'], _matchTime, _matchStats['goalAttempts'],
                                                     _matchStats['shotsOff'], _matchStats['corners'], match['odds'], match['score'])
                if type(_verification) is not int:
                    self.matchs.update({_matchId: False}) if _matchTime <= 45 else self.matchs.update({_matchId: True})
                    _verification.update({'teams': match['teams']})
                    response.append({_matchId: _verification})

        return response

    @staticmethod
    def calcAPPM(dangerousAttacks: int, matchTime: int) -> int or float:
        return dangerousAttacks / matchTime if matchTime > 0 else 0

    @staticmethod
    def calcCG(goalAttempts: int, shotsOff: int, corners: int) -> int:
        return goalAttempts + shotsOff + corners

    @staticmethod
    def calcOdd(odds: List[int], score: str) -> int:
        [home, away] = score.split(':')
        home = int(home)
        away = int(away)
        return odds[0] if home > away else odds[2] if away > home else odds[1]

    @staticmethod
    def getLoserStat(stat: Dict[str, int], teamSide: str) -> int:
        return stat[teamSide]

    @staticmethod
    def getLoser(score: str) -> str:
        [home, away] = score.split(':')
        home = int(home)
        away = int(away)
        return 'away' if away < home else 'home'

    def oddVerification(self, dangerousAttacks: Dict[str, int], matchTime: int, goalAttempts: Dict[str, int],
                        shotsOff: Dict[str, int], corners: Dict[str, int], odds: List[int],
                        score: str) -> Union[Dict[str, int or float or str], int]:
        _teamSide = self.getLoser(score)

        matchTime = int(matchTime)
        dangerousAttacks = self.getLoserStat(dangerousAttacks, _teamSide)
        goalAttempts = self.getLoserStat(goalAttempts, _teamSide)
        shotsOff = self.getLoserStat(shotsOff, _teamSide)
        corners = self.getLoserStat(corners, _teamSide)

        _passed = False
        _constAPPM = 0
        _constCG = 0
        _constCorners = 0

        if matchTime <= 45:
            _constAPPM = self.constAPPM1
            _constCG = self.constCG1
            _constCorners = self.constCorners1
        elif matchTime > 45:
            _constAPPM = self.constAPPM2
            _constCG = self.constCG2
            _constCorners = self.constCorners2

        currentAPPM = self.calcAPPM(dangerousAttacks, matchTime)
        if self.calcAPPM(dangerousAttacks, matchTime) > _constAPPM and self.calcCG(goalAttempts, shotsOff, corners) > _constCG and corners > _constCorners and corners > shotsOff:
            _passed = True
        return {'odd': self.calcOdd(odds, score), 'score': score, 'appm': currentAPPM} if _passed else 0
