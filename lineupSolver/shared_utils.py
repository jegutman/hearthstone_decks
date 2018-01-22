import itertools
import math

def win_rates_grid(decks_a, decks_b, win_pcts,num_games=None):
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
            ng = num_games.get((deck, deck_b), "") if num_games else ""
            line += "%6s (%5s)      " % (wr, ng)
        avg = round(sum(wrs) / len(wrs), 1)    
        line += "%6s              " % avg
        print line
    
def similarity(deck_a, deck_b, win_pcts, archetypes, debug=False):
    tmp = [d for d in archetypes if d not in (deck_a,deck_b)]
    sigma2 = 0
    for i in tmp:
        diff = win_pcts[(deck_a,i)] - win_pcts[(deck_b,i)]
        if debug:
            print "%-25s %s" % (i, diff)
        sigma2 += diff ** 2
    return math.sqrt(sigma2 / len(tmp))
    
    

def check_lineup(decks, archetype_map, num_classes=4):
    classes = [archetype_map.get(x, '').split(' ')[-1] for x in decks]
    if len(set(classes)) == num_classes:
        return True
    else:
        return False

def class_sort(a):
    tmp = a.split(' ' )
    return (tmp[-1], tmp)

def get_lineup(decks, archetype_map):
    return tuple([archetype_map[i] for i in decks])

def generate_lineups(archetypes, unbeatable=False, num_classes=4):
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
        tmp_res = list(itertools.combinations(keys,num_classes))
        lineups = []
        for decks in tmp_res:
            #classes = [x.split(' ')[-1] for x in decks]
            if check_lineup(decks, archetype_map, num_classes):
                #if decks not in lineups:
                lineups.append(decks)
            #if len(set(classes)) == num_classes:
            #    #print decks
            #    if decks not in lineups:
            #        lineups.append(decks)
    return lineups, archetype_map

def get_win_pct(a,b, win_pcts):
    if a == 'Unbeatable' and b != 'Unbeatable': return 1
    if b == 'Unbeatable' and a != 'Unbeatable': return 0
    #if a == b: return 0.5
    res = win_pcts.get((a,b))
    if res == None:
        res = 0.49999
        #print "missing win rate for %s : %s" % (a,b)
    return win_pcts.get((a,b), 0)

def sumproduct_normalize(a, b):
    res = 0
    for i,j in zip(a,b):
        res += i * j
    res = res / sum(b)
    return res
    
