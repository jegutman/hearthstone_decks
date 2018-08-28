import itertools
import math
import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)


def win_rates_grid(decks_a, decks_b, win_pcts,num_games=None):
    print(win_rates_lines(decks_a, decks_b, win_pcts,num_games))
    
def win_rates_lines(decks_a, decks_b, win_pcts,num_games=None):
    res = ""
    top_line = "%-20s" % "x"
    for deck in decks_b:
        top_line += "%-20s" % deck
    top_line += "%-20s" % 'average'
    res += top_line + '\n'
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
        res += line + '\n'
    return res
    
def similarity(deck_a, deck_b, win_pcts, archetypes, debug=False):
    tmp = [d for d in archetypes if d not in (deck_a,deck_b)]
    sigma2 = 0
    for i in tmp:
        diff = win_pcts[(deck_a,i)] - win_pcts[(deck_b,i)]
        if debug:
            print("%-25s %s" % (i, diff))
        sigma2 += diff ** 2
    return math.sqrt(sigma2 / len(tmp))
    
    

def check_lineup(decks, archetype_map, num_classes=4):
    classes = [archetype_map.get(x, '').split()[-1] for x in decks]
    if len(set(classes)) == num_classes:
        return True
    else:
        return False

def class_sort(a):
    tmp = a.split()
    return (tmp[-1], tmp)

def get_lineup(decks, archetype_map):
    return tuple([archetype_map[i] for i in decks])

def get_class_decks(archetypes, deck_class):
    return [i for i in archetypes if i.split(' ')[-1] == deck_class]


def generate_lineups(archetypes, unbeatable=False, num_classes=4, additional_archetypes=[]):
    archetype_map = {}
    a_count = 0
    for a in sorted(archetypes, key=lambda x:x.split(' ')[-1]):
        archetype_map[a_count] = a
        a_count += 1
    classes = ['Druid', 'Hunter', 'Mage', 'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
    if unbeatable:
        archetypes.append('Unbeatable')
        classes.append('Unbeatable')
    class_arch = {}
    for index, a in archetype_map.items():
        tmp = a.split(' ')[-1]
        class_arch[classes.index(tmp)] = class_arch.get(classes.index(tmp), []) + [index]
    class_sets = list(itertools.combinations(range(0, len(classes)), num_classes))
    lineups = []
    for class_set in class_sets:
        count = 0
        tmp = []
        for i in class_set:
            tmp.append(class_arch.get(i, []))
        lineups += itertools.product(*tmp)
    for a in additional_archetypes:
        archetype_map[a_count] = a
        a_count += 1
    return lineups, archetype_map


missing_wr = []
def get_win_pct(a,b, win_pcts):
    global missing_wr
    if a == 'Unbeatable' and b != 'Unbeatable': return 1
    if b == 'Unbeatable' and a != 'Unbeatable': return 0
    #if a == b: return 0.5
    res = win_pcts.get((a,b))
    if (a,b) not in missing_wr:
        missing_wr.append((a,b))
    if res == None:
        res = 0.49999
    #if a == 'Spiteful Druid':
    #    return win_pcts.get((a,b), 0) - 0.03
    return win_pcts.get((a,b), 0)

def missing_wrs():
    global missing_wr
    return missing_wr

def sumproduct_normalize(a, b):
    res = 0
    for i,j in zip(a,b):
        res += i * j
    res = res / sum(b)
    return res

def geometric_mean(a, b):
    res = 1.0
    for i,j in zip(a,b):
        res *= (i ** j)
    res = res ** (1.0 / sum(b))
    return res
