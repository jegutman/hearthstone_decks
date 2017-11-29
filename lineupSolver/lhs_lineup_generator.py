from json_win_rates import * 
from lhs_utils import * 
from shared_utils import *

win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=200, min_game_count=1000)
print archetypes 

excluded = []
#excluded = ['Big Priest']
#excluded = ['Murloc Paladin', 'Secret Mage', 'Exodia Mage', 'Aggro-Token Druid', 'Dragon Priest']
print "\n\nEXCLUDING:", excluded
archetypes = [a for a in archetypes if a not in excluded]

lineups = generate_lineups(archetypes)

print "testing %s lineups" % len(lineups)

win_rates_against_good = {}
level1, level2, level3, level4, level5 = None, None, None, None, None
#level1 = ['Unbeatable', 'Tempo Rogue', 'Quest Warrior', 'Zoo Warlock']
#level1 = ['Tempo Rogue', 'Jade Druid', 'Highlander Priest', 'Zoo Warlock']
level1 = ['Tempo Rogue', 'Jade Druid', 'Highlander Priest', 'Token Shaman']
#level2 = ['Tempo Rogue', 'Big Druid', 'Big Priest', 'Zoo Warlock']
#level3 = ['Pirate Warrior', 'Aggro Druid', 'Murloc Paladin', 'Zoo Warlock']

lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]

print "\n"
print "TESTING vs LINEUPS"
for l in lineups_to_test:
    print "   ".join(l)
print "\n"

for lineup in lineups:
    for lu_test in lineups_to_test:
        win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts, useGlobal=True)]

for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
    i = " ".join(i)
    print "%-90s %s %s" % (i,j, round(sum([x[1] for x in j])/len(j),3))
