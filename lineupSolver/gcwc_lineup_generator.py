from json_win_rates import * 
from lhs_utils import * 
from shared_utils import *

win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=200, min_game_count=1000)
print archetypes 

excluded = []
excluded = ['Big Priest']
excluded_classes = []
excluded_classes = ['Druid', 'Priest']
#excluded = ['Murloc Paladin', 'Secret Mage', 'Exodia Mage', 'Aggro-Token Druid', 'Dragon Priest']
print "\n\nEXCLUDING:", excluded
print "\n\nEXCLUDING CLASSES:", excluded_classes
archetypes = [a for a in archetypes if a not in excluded and a.split(' ')[-1] not in excluded_classes] + ['Unbeatable']

lineups = generate_lineups(archetypes)

print "testing %s lineups" % len(lineups)

win_rates_against_good = {}
level_1 = ['Unbeatable', 'Tempo Rogue', 'Quest Warrior', 'Zoo Warlock']
#level_1_b = ['Tempo Rogue', 'Jade Druid', 'Razakus Priest', 'Murloc Paladin']
#level_1_b = ['Tempo Rogue', 'Big Druid', 'Big Priest', 'Zoo Warlock']
#level_2 = ['Big Druid', 'Dragon Priest', 'Murloc Paladin', 'Tempo Rogue']
#level_2 = ['Tempo Rogue', 'Razakus Priest', 'Control Warlock', 'Token Shaman']
#level_3 = ['Aggro-Token Druid', 'Murloc Paladin', 'Tempo Rogue', 'Zoo Warlock']

#new_god = ['Aggro-Token Druid', 'Big Priest', 'Murloc Paladin', 'Tempo Rogue']

#josh_test_1 = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
#
#lineups_to_test = [level_1, level_1_b, level_2]#, level_3]
#lineups_to_test = [level_1, level_1_b, level_2, new_god]#, level_3]
lineups_to_test = [level_1]#, level_2]#, level_3]

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

for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
    print "%-90s %s %s" % (i,j, round(sum([x[1] for x in j])/len(j),3))
