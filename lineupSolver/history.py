from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 


import sys
import os
deck = " ".join(sys.argv[1:])
print "TESTING: %s" % deck
for i in sorted(os.listdir('win_rates/')):
    if '2018' in i and 'LONLY_7DAYS' in i:
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=100, filename='win_rates/%s' % i)
        results = []
        print i, 100 * get_win_pct('Cube Warlock','Quest Rogue',win_pcts)
