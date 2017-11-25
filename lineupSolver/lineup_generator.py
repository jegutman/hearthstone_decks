from parseWinRates import *

print archetypes
from conquest_utils import *
from shared_utils import *

lineups = []

excluded = []
#excluded = ['Murloc Paladin', 'Secret Mage', 'Exodia Mage', 'Aggro-Token Druid']
print "\n\nEXCLUDING:", excluded
archetypes = [a for a in archetypes if a not in excluded]

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
#level_1_shaman = ['Tempo Rogue', 'Jade Druid', 'Razakus Priest', 'Token Shaman']
#level_2 = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
level_2 = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Murloc Paladin']
level_3 = ['Big Druid', 'Big Priest', 'Control Mage', 'Tempo Rogue']


#new_god = ['Aggro-Token Druid', 'Big Priest', 'Murloc Paladin', 'Tempo Rogue']

#josh_test_1 = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
#
#lineups_to_test = [level_1, level_1_b, level_2]#, level_3]
#lineups_to_test = [level_1, level_1_b, level_2, new_god]#, level_3]
opp_lineup_1 = ['Tempo Rogue', 'Big Druid', 'Big Priest', 'Control Mage']
opp_lineup_2 = ['Tempo Rogue', 'Big Druid', 'Murloc Paladin', 'Razakus Priest']
#lineups_to_test = [level_1,level_2, level_3]
lineups_to_test = [opp_lineup_1, opp_lineup_2]
#lineups_to_test = [level_1_shaman]

print "\n"
print "TESTING vs LINEUPS"
for l in lineups_to_test:
    print "   ".join(l)
print "\n"

for lineup in lineups:
    for lu_test in lineups_to_test:
        win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts)]

for i,j in sorted(win_rates_against_good.items())[:3]:
    print i,j 

#for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
    print "%-90s %s %s" % (i,j, round(sum([x[1] for x in j])/len(j),3))

#my_lineup = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
my_lineup = ['Big Druid', 'Big Priest', 'Tempo Rogue', 'Zoo Warlock']
#opp_lineup = ['Tempo Rogue', 'Big Druid', 'Big Priest', 'Control Mage']
opp_lineup = ['Tempo Rogue', 'Big Druid', 'Murloc Paladin', 'Razakus Priest']

win_rates_grid(my_lineup, opp_lineup, win_pcts)
print win_rate(my_lineup, opp_lineup, win_pcts)
print pre_ban(my_lineup, opp_lineup, win_pcts)

