from glicko import Glicko2
import math

env = Glicko2(tau=0.5)

def Rating(mu=None):
    return env.create_rating(1500, 200, 0.06)

#HCT German TakeTV (S1),Global Qualifier,1,Sintolol,Radogask,3,1
#event,sub_event,
filename = 'hct_results.csv'
file = open(filename)
rating = {}
games = {}
wins = {}
expected = []
errors = []
baseline = []
for line in file:
    event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line.strip().split(',')
    if score1 == 'None' or score2 == 'None': 
        continue
    score1 = int(score1)
    score2 = int(score2)
    round_num = int(round_num)
    p1 = p1.lower()
    p2 = p2.lower()
    if max(score1, score2) != 3: continue
    if score1 == score2: continue
    result = score1 > score2
    games[p1] = games.get(p1, 0) + 1
    games[p2] = games.get(p2, 0) + 1
    if p1 not in rating:
        rating[p1] = Rating()
    if p2 not in rating:
        rating[p2] = Rating()
    #print(env.quality_1vs1(rating[p1], rating[p2]))
    est = env.expect(rating[p1], rating[p2])
    est = min(est, 0.75)
    est = max(est, 0.25)
    expected.append( est)
    #baseline.append((0.5-result)**2)
    if result:
        rating[p1], rating[p2] = env.rate_1vs1(rating[p1], rating[p2])
        wins[p1] = wins.get(p1, 0) + 1
        error = (est - 1) ** 2
    else:
        rating[p2], rating[p1] = env.rate_1vs1(rating[p2], rating[p1])
        wins[p2] = wins.get(p2, 0) + 1
        error = (est - 0) ** 2
    errors.append(error)

min_games = 40

def expose(r):
    return r.mu

top_players = [i for i in sorted(rating.items(), key = lambda x:expose(x[1]), reverse=True) if games[i[0]] >= min_games]
print("   %-15s %-5s %-5s" % ('Player', 'rEst', 'games'))
index = 0
for p, r in top_players[:50]:
    index += 1
    win = wins.get(p, 0)
    losses = games[p] - win
    print("%2s %-15s %-5.2f %4s    %s - %s" % (index, p, expose(r), games[p], win, losses))
