# some assumptions on formating
# whatever deck a player is forced to play should be listed first (for 3v2 and 2v2 scenarios, irrelevant otherwise)

# branching calcs
# 16 x ban phase
# assume order doesn't matter
# branch on both possible results

#win_pct = {}

from parseWinRates import win_pcts
from conquest_utils import *

archetypes = [
    'Tempo Rogue',
    'Razakus Priest',
    'Zoo Warlock',
    'Aggro-Token Druid',
    'Jade Druid',
    'Big Druid',
    'Big Priest',
    'Control Mage',
    'Midrange Hunter',
    'Token Shaman',
    'Control Warlock',
    'Murloc Paladin',
    'Secret Mage',
    'Exodia Mage',
    'Dragon Priest',
    'Miracle Rogue',
]

#lineup_1 = ['Tempo Rogue', 'Jade Druid', 'Razakus Priest', 'Murloc Paladin']
#lineup_2 = ['Aggro-Token Druid', 'Dragon Priest', 'Murloc Paladin', 'Tempo Rogue']
lineup_1 = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
lineup_2 = ['Tempo Rogue', 'Jade Druid', 'Razakus Priest', 'Zoo Warlock']
res = pre_ban_old(lineup_1,
                  lineup_2,
                  win_pcts)
print res.items()
print ""
print lineup_1, "vs", lineup_2
print "bans"
print "%-18s %-18s" % ("p1_ban", "p2_ban")
#for i, j in sorted(res.items(), key=lambda x:-x[1]):
for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
    d1, d2 = i
    print '%-18s %-18s %s' % (d1, d2, round(j,4))

print lineup_1, "vs", lineup_2
res = win_rate(lineup_1,
               lineup_2,
               win_pcts)
print res
print lineup_2, "vs", lineup_1
res = win_rate(lineup_2,
               lineup_1,
               win_pcts)
print res
