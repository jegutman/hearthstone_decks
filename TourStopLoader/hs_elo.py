import math

MU = 1500
defaultK = 36

class Rating(object):

    def __init__(self, mu=MU, K=defaultK, games=0):
        self.mu = mu
        self.minK = K
        #self.factor = 0.25
        self.factor = 0
        self.K = (1+self.factor) * K
        self.games = games
        self.history = []

    def __repr__(self):
        return '%s' % int(self.mu)

    def update(self, delta):
        self.mu += delta
        self.games += 1
        self.K = max(20 - self.games, 0) * self.factor * self.minK + self.minK
        if self.games > 10:
            self.history.append(int(self.mu))

    def __lt__(self, other):
        return self.mu < other.mu


class HS_Elo(object):

    def __init__(self, mu=MU, defaultK=defaultK):
        self.mu = mu
        self.defaultK = defaultK

    def create_rating(self, mu=None, K=None):
        if mu is None:
            mu = self.mu
        if K is None:
            K = self.defaultK
        return Rating(mu, K)

    def expect_score(self, r1, r2):
        rating_diff = r2.mu - r1.mu
        #rating_diff = min(max(rating_diff, -600), 600)
        return 1 / (1 + 10 ** (rating_diff / 1135.77))

    def calc_diff(self, pct):
        C = 1135.77
        return -round(math.log(1/pct - 1, 10) * C, 1)

    def rate(self, rating, series):
        pass

    def rate_1vs1(self, r1, r2, drawn=False):
        win_pct = self.expect_score(r1, r2)
        change1 = round((1 - win_pct) * r1.K, 1)
        change2 = round(-win_pct * r2.K, 1)
        r1.update(change1)
        r2.update(change2)
        
        #return (self.rate(rating1, [(DRAW if drawn else WIN, rating2)]),
        #        self.rate(rating2, [(DRAW if drawn else LOSS, rating1)]))

if __name__ == '__main__':
    env = None
