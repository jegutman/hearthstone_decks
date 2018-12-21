import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from shared_utils import *
import itertools
from pprint import pprint
from json_win_rates import *

l1 = ['Druid', 'Hunter', 'Mage', 'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=40)
class_arch = {}
for card_class in l1:
    class_arch[card_class] = []
    for ca in archetypes:
        if card_class == ca.split(' ')[-1]:
            class_arch[card_class].append(ca)

weights = {}
class_fract = {
    'Hunter' : .12857142857142856,
    'Shaman' : .11904761904761904,
    'Druid' : .09047619047619047,
    'Warrior' : .12380952380952381,
    'Rogue' : .1,
    'Paladin' : .1,
    'Priest' : .11904761904761904,
    'Warlock' : .1,
    'Mage' : .11904761904761904,
}

for card_class in l1:
    total = sum([game_count[i] for i in class_arch[card_class]])
    for ca in class_arch[card_class]:
        #weights[ca] = game_count[ca] / 9. / total
        weights[ca] = game_count[ca] * class_fract[card_class] / total

new_win_pcts = {}
for i in weights:
    for j in weights:
        new_win_pcts[i] = new_win_pcts.get(i, 0) + weights[j] * win_pcts.get((i,j), 0.49999)

for i,j in sorted(new_win_pcts.items(), key=lambda x:(x[0].split(' ')[-1], x[1]), reverse=True):
    j = round(j,4)
    print("%-20s %s" % (i,j))
