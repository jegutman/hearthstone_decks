from archetypes import aggro, meta
archetypes = []
data = {}
line_data = []


with open('CoinData.csv') as f:
    for line in f:
        if line[0] == "#":
            continue
        tmp = line.strip().split(',')
        deck_a, deck_b, first, pct, games = tmp
        if deck_b not in meta: continue
        for d in (deck_a, deck_b):
            if d not in archetypes:
                assert d != '10', line
                archetypes.append(d)
            if d not in data:
                data[d] = {}
        if deck_b not in data[deck_a]:
            data[deck_a][deck_b] = [(), ()]
        first = int(first)
        has_coin = 1 - first
        pct = float(pct)
        games = int(games)
        data[deck_a][deck_b][first] = (pct, games)
        line_data.append((deck_a, deck_b, first, pct, games))

diffs = {}
deck_stats = {}
games_count = {}
for deck_a, deck_b, first, pct, games in line_data:
    key = (deck_a, first)
    deck_stats[key] = deck_stats.get(key, 0) + int(round(pct * games / 100))
    games_count[key] = games_count.get(key, 0) + games

overall = []
for i in archetypes:
    pct_1 = round(float(deck_stats[(i, 1)] / games_count[(i,1)]) * 100, 1)
    pct_0 = round(float(deck_stats[(i, 0)] / games_count[(i,0)]) * 100, 1)
    #min_g = min(games_count[(i,1)], games_count[(i,0)])
    g_1 = games_count[(i,1)]
    g_0 = games_count[(i,0)]
    diff = round(pct_1 - pct_0, 1)
    #print("%-25s" % i, pct_1, pct_0, "%5.1f" % diff, "%6s" % min_g)
    #overall.append((i, pct_1, pct_0, diff, min_g))
    overall.append((i, pct_1, pct_0, diff, g_1, g_0))

#for i, pct_1, pct_0, diff, min_g in sorted(overall, key=lambda x:x[-2], reverse=True):
#    print("%-25s" % i, pct_1, pct_0, "%5.1f" % diff, "%6s" % min_g)

i, pct_1, pct_0, diff, g_1, g_0 = "deck,1st ,2nd ,diff,g_1,g_2".split(',')
print("%-25s" % i, pct_1, pct_0, "%5s" % diff, "%6s" % g_1, "%6s" % g_0)
for i, pct_1, pct_0, diff, g_1, g_0 in sorted(overall, key=lambda x:x[3], reverse=True):
    overall_win = (pct_1 * g_1 + pct_0 * g_0) / (g_1 + g_0)
    print("%-25s" % i.replace(' ', '_'), pct_1, pct_0, "%5.1f" % diff, "%6s" % g_1, "%6s" % g_0, round(overall_win, 1))
