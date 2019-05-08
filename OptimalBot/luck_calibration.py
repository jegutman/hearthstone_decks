import math

def win_odds(series):
    #series = x ** 3 + 3 * x **2 * (1-x)
    # 7-1 or better
    top8 = series ** 8 + 8 * series ** 7 * (1-series)
    win = series ** 3 * top8
    return win

def percent_90(x, res=0.1):
    return math.log(res) / math.log(1-win_odds(x))

#for x in range(500, 900, 25):
#    x = x / 1000
#    pct = round(x * 100, 1)
#    tournament = round(100 * win_odds(x), 1)
#    #events50 = int(round(percent_90(x, 0.5) + 0.5, 0))
#    #events = int(round(percent_90(x) + 0.5, 0))
#    print("%s,%s,%s,%s" % (pct, tournament, events50, events))

res = []
file = open('all_player_stats.csv')
for line in file:
    player, cups, wins, losses, games, winner = line.strip().split(',')
    cups = int(cups)
    wins = int(wins)
    losses = int(losses)
    games = int(games)
    pct = wins / games
    winner = int(winner)
    twin_pct = win_odds(pct)
    win_0 = (1-twin_pct) ** cups
    unluck = 1-win_0
    res.append((unluck, player, cups, pct, winner))

keys = [0,20,40,60,80]
buckets = {x : [] for x in keys}

for unluck, player, cups, pct, winner in sorted(res, reverse=True):
    for x in buckets.keys():
        if unluck * 100 > x and unluck * 100 < x+20:
            buckets[x].append((player, cups, pct, unluck, winner))
        
    #if unluck > 0.4:
    #    print("%s,%s,%s,%s" % (player, cups, pct, unluck))

for x in buckets.keys():
    print("%s-%s" % (x, x+20),len(buckets[x]), sum([y[-2] for y in buckets[x]])/ len(buckets[x]),sum([y[-1] for y in buckets[x]]), sum([y[-1] for y in buckets[x]]) / len(buckets[x]))
