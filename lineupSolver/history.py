from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 


import sys
import os

deck_a = sys.argv[1]
deck_b = sys.argv[2]

if len(sys.argv) > 3:
    time_range = sys.argv[3]
else:
    time_range = '7DAYS'

print(deck_a, deck_b)
first_date = '2018_04_15'

file_type = 'LONLY_' + time_range

print("\n%s\n" % file_type)

all_samples = []
for i in sorted(os.listdir('win_rates/')):
    if '2018' in i and file_type in i:
        try:
            win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=100, filename='win_rates/%s' % i)
            results = []
            #hsreplay20180509_LONLY_7DAYS.json
            date = i.replace('hsreplay', '').replace('_%s.json' % file_type, '')
            date = date[:4] + '_' + date[4:6] + '_' + date[6:]
            all_samples.append((date, 100 * get_win_pct(deck_a,deck_b,win_pcts), num_games[(deck_a,deck_b)]))
            print("%10s   %4.1f   %s" % (date, 100 * get_win_pct(deck_a,deck_b,win_pcts), num_games[(deck_a,deck_b)]))
        except:
            pass

total = 0
total_pct = 0
for i in range(0, 12, 3):
    date, pct, games = all_samples[-i]
    total_pct += pct * games
    total += games
    #print pct, games

print("%2.2f %s" % (total_pct / total, total))
