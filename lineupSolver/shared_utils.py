def win_rates_grid(decks_a, decks_b, win_pcts):
    top_line = "%-20s" % "x"
    for deck in decks_b:
        top_line += "%-20s" % deck
    print top_line
    for deck in decks_a:
        line = "%-20s" % deck
        for deck_b in decks_b:
            line += "%6s              " % round(win_pcts.get((deck, deck_b), 0) * 100, 1)
        print line

def generate_lineups(archetypes):
    #archetypes = sorted(archetypes)
    lineups = []
    for i in range(0, len(archetypes)):
        for j in range(i+1, len(archetypes)):
            for k in range(j+1, len(archetypes)):
                for l in range(k+1, len(archetypes)):
                    a, b, c, d = [archetypes[x] for x in [i,j,k,l]]
                    decks = tuple(sorted([a,b,c,d]))
                    classes = [x.split(' ')[-1] for x in decks]
                    if len(set(classes)) == 4:
                        #print decks
                        if decks not in lineups:
                            lineups.append(decks)
    return lineups

def get_win_pct(a,b, win_pcts):
    if a == 'Unbeatable': return 1
    if b == 'Unbeatable': return 0
    return win_pcts.get((a,b), 0)

def sumproduct_normalize(a, b):
    res = 0
    for i,j in zip(a,b):
        res += i * j
    res = res / sum(b)
    return res
    
