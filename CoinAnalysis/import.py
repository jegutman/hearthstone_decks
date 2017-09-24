archetypes = []
data = {}

with open('CoinData.csv') as f:
    for line in f:
        if line[0] == "#":
            continue
        tmp = line.strip().split(',')
        deck_a, deck_b, first, pct, games = tmp
        for d in (deck_a, deck_b):
            if d not in archetypes:
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
