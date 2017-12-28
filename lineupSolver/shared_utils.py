import itertools
def win_rates_grid(decks_a, decks_b, win_pcts):
    top_line = "%-20s" % "x"
    for deck in decks_b:
        top_line += "%-20s" % deck
    top_line += "%-20s" % 'average'
    print top_line
    for deck in decks_a:
        line = "%-20s" % deck
        wrs = []
        for deck_b in decks_b:
            wr = round(win_pcts.get((deck, deck_b), 0) * 100, 1)
            wrs.append(wr)
            line += "%6s              " % wr
        avg = round(sum(wrs) / len(wrs), 1)    
        line += "%6s              " % avg
        print line
    

def check_lineup(decks, archetype_map):
    classes = [archetype_map.get(x, '').split(' ')[-1] for x in decks]
    if len(set(classes)) == 4:
        return True
    else:
        return False

def class_sort(a):
    tmp = a.split(' ' )
    return (tmp[-1], tmp)

def get_lineup(decks, archetype_map):
    return tuple([archetype_map[i] for i in decks])

def generate_lineups(archetypes, unbeatable=False):
    #archetypes = sorted(archetypes)
    #lineups = []
    #if unbeatable:
    #    for i in range(0, len(archetypes)):
    #        for j in range(i+1, len(archetypes)):
    #            for k in range(j+1, len(archetypes)):
    #                a, b, c = [archetypes[x] for x in [i,j,k]]
    #                d = 'Unbeatable'
    #                decks = tuple(sorted([a,b,c,d]))
    #                #decks = tuple(sorted([a,b,c]))
    #                classes = [x.split(' ')[-1] for x in decks]
    #                if len(set(classes)) == 4:
    #                    #print decks
    #                    if decks not in lineups:
    #                        lineups.append(decks)
    #else:
    #    for i in range(0, len(archetypes)):
    #        for j in range(i+1, len(archetypes)):
    #            for k in range(j+1, len(archetypes)):
    #                for l in range(k+1, len(archetypes)):
    #                    a, b, c, d = [archetypes[x] for x in [i,j,k,l]]
    #                    decks = tuple(sorted([a,b,c,d]))
    #                    classes = [x.split(' ')[-1] for x in decks]
    #                    if len(set(classes)) == 4:
    #                        #print decks
    #                        if decks not in lineups:
    #                            lineups.append(decks)
    ############ NEW METHOD ##########
    if unbeatable:
        archetypes_tmp = archetypes[:]
        archetypes = archetypes_tmp
        archetype_map = {}
        for i in range(0, len(archetypes)):
            archetype_map[i] = archetypes[i]
        #keys = sorted(archetype_map.keys())
        #tmp_res = list(itertools.combinations(keys,3))
        tmp_res = list(itertools.combinations(archetypes,3))
        archetypes.append('Unbeatable')
        archetype_map[archetypes.index('Unbeatable')] = 'Unbeatable'
        lineups = []
        for decks in tmp_res:
            classes = [x.split(' ')[-1] for x in decks]
            if len(set(classes)) == 3:
                if decks not in lineups:
                    lineups.append(decks+('Unbeatable', ))
    else:
        archetypes_tmp = archetypes[:]
        archetypes = archetypes_tmp
        archetype_map = {}
        for i in range(0, len(archetypes)):
            archetype_map[i] = archetypes[i]
        keys = sorted(archetype_map.keys())
        tmp_res = list(itertools.combinations(keys,4))
        #tmp_res = list(itertools.combinations(archetypes,4))
        lineups = []
        for decks in tmp_res:
            #classes = [x.split(' ')[-1] for x in decks]
            if check_lineup(decks, archetype_map):
                #if decks not in lineups:
                lineups.append(decks)
            #if len(set(classes)) == 4:
            #    #print decks
            #    if decks not in lineups:
            #        lineups.append(decks)
    return lineups, archetype_map

def get_win_pct(a,b, win_pcts):
    if a == 'Unbeatable' and b != 'Unbeatable': return 1
    if b == 'Unbeatable' and a != 'Unbeatable': return 0
    if a == b: return 0.5
    res = win_pcts.get((a,b))
    if res == None:
        res = 0.5
        #print "missing win rate for %s : %s" % (a,b)
    return win_pcts.get((a,b), 0)

def sumproduct_normalize(a, b):
    res = 0
    for i,j in zip(a,b):
        res += i * j
    res = res / sum(b)
    return res
    
