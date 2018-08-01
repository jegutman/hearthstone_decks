from trueskill import *
import trueskill
import itertools
import math

def win_probability(p1, p2):
    team1 = [p1]
    team2 = [p2]
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)

#HCT German TakeTV (S1),Global Qualifier,1,Sintolol,Radogask,3,1
#event,sub_event,
filename = 'hct_results.csv'
file = open(filename)
rating = {}
games = {}
wins = {}
for line in file:
    #event, sub_event, round_num, p1, p2, score1, score2 = line.strip().split(',')
    #date, bracket_name, round_number, p1, p2, result, p1_score, p2_score, games = line.strip().split(',')
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
    if result:
        rating[p1], rating[p2] = rate_1vs1(rating[p1], rating[p2])
        wins[p1] = wins.get(p1, 0) + 1
    else:
        rating[p2], rating[p1] = rate_1vs1(rating[p2], rating[p1])
        wins[p2] = wins.get(p2, 0) + 1
file.close()

min_games = 40

top_players = [i for i in sorted(rating.items(), key = lambda x:expose(x[1]), reverse=True) if games[i[0]] >= min_games]
print("    %-15s %-5s %-5s" % ('Player', 'rEst', 'games'))
index = 0
for p, r in top_players[:200]:
    index += 1
    win = wins.get(p, 0)
    losses = games[p] - win
    print("%3s %-15s %-5.2f %4s    %s - %s" % (index, p, expose(r), games[p], win, losses))

top100 = [i for i,j in top_players[:100]]

filename = 'hct_results.csv'
file = open(filename)
rating = {}
games = {}
wins = {}
for line in file:
    tmp = line.strip().split(',')
    if len(tmp) == 8:
        event, sub_event, sub_bracket, round_num, p1, p2, score1, score2 = tmp
    elif len(tmp) == 10:
        event, sub_event, sub_bracket, season, patch, round_num, p1, p2, score1, score2 = tmp
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
    if result:
        rating[p1], rating[p2] = rate_1vs1(rating[p1], rating[p2])
        wins[p1] = wins.get(p1, 0) + 1
    else:
        rating[p2], rating[p1] = rate_1vs1(rating[p2], rating[p1])
        wins[p2] = wins.get(p2, 0) + 1
file.close()

