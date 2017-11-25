from parseWinRates import *

print archetypes
from lhs_utils import *

lineups = []

for a in archetypes:
    for b in archetypes:
        for c in archetypes:
            for d in archetypes:
                decks = tuple(sorted([a,b,c,d]))
                classes = [i.split(' ')[-1] for i in decks]
                if len(set(classes)) == 4:
                    #print decks
                    if decks not in lineups:
                        lineups.append(decks)

win_rates_against_good = {}
level_1 = ['Tempo Rogue', 'Jade Druid', 'Razakus Priest', 'Zoo Warlock']
#level_1_b = ['Tempo Rogue', 'Jade Druid', 'Razakus Priest', 'Murloc Paladin']
#level_1_b = ['Tempo Rogue', 'Big Druid', 'Big Priest', 'Zoo Warlock']
level_2 = ['Big Druid', 'Dragon Priest', 'Murloc Paladin', 'Tempo Rogue']
#level_2 = ['Tempo Rogue', 'Razakus Priest', 'Control Warlock', 'Token Shaman']
#level_3 = ['Aggro-Token Druid', 'Murloc Paladin', 'Tempo Rogue', 'Zoo Warlock']

#new_god = ['Aggro-Token Druid', 'Big Priest', 'Murloc Paladin', 'Tempo Rogue']

#josh_test_1 = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
#
#lineups_to_test = [level_1, level_1_b, level_2]#, level_3]
#lineups_to_test = [level_1, level_1_b, level_2, new_god]#, level_3]
lineups_to_test = [level_1, level_2]#, level_3]

for lineup in lineups:
    for lu_test in lineups_to_test:
        win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts)]

for i,j in sorted(win_rates_against_good.items())[:3]:
    print i,j 

for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
    print "%-90s %s %s" % (i,j, round(sum([x[1] for x in j])/len(j),3))
