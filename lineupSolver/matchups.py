from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *


if __name__ == '__main__':

    import sys
    deck = " ".join(sys.argv[1:])
    print "TESTING: %s" % deck
    win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=50, min_game_count=500)
    results = []
    for a in archetypes:
        results.append((round( 100 * get_win_pct(deck,a,win_pcts), 1), a))
    #for pct, a in sorted(results, reverse=True):
    for pct, a in sorted(results, key=lambda x:num_games.get((deck, x[1])), reverse=True):
        print "%-25s %6s %5s" % (a, pct, num_games[(deck,a)])
