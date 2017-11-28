from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *

win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=200, min_game_count=100)
print archetypes 

excluded = []
#excluded = ['Big Priest']
#excluded = ['Murloc Paladin', 'Secret Mage', 'Exodia Mage', 'Aggro-Token Druid', 'Dragon Priest']
print "\n\nEXCLUDING:", excluded
archetypes = [a for a in archetypes if a not in excluded]


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'sim':
        #my_lineup = ['Big Druid', 'Dragon Priest', 'Tempo Rogue', 'Zoo Warlock']
        #opp_lineup = ['Tempo Rogue', 'Big Druid', 'Big Priest', 'Control Mage']
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        print my_lineup, "vs", opp_lineup
        win_rates_grid(my_lineup, opp_lineup, win_pcts)
        print win_rate(my_lineup, opp_lineup, win_pcts)
        print pre_ban(my_lineup, opp_lineup, win_pcts)

        res = pre_ban_old(my_lineup,
                          opp_lineup,
                          win_pcts)
        print ""
        print my_lineup, "vs", opp_lineup
        print "bans"
        print "%-18s %-18s" % ("p1_ban", "p2_ban")
        #for i, j in sorted(res.items(), key=lambda x:-x[1]):
        for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
            d1, d2 = i
            print '%-18s %-18s %s' % (d1, d2, round(j,4))

    else:
        lineups = generate_lineups(archetypes)
        print "testing %s lineups" % len(lineups)
        win_rates_against_good = {}
        level1, level2, level3, level4, level5 = None, None, None, None, None
        #level1 = ['Tempo Rogue', 'Big Druid', 'Highlander Priest', 'Murloc Paladin']
        #level1 = ['Tempo Rogue', 'Big Druid', 'Highlander Priest', 'Zoo Warlock']
        level1 = ['Tempo Rogue', 'Jade Druid', 'Highlander Priest', 'Token Shaman']
        #level2 = ['Unbeatable', 'Dragon Priest', 'Tempo Rogue', 'Murloc Paladin']
        lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]

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
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
            print "%-90s %s %s" % (i,j, round(sum([x[1] for x in j])/len(j),3))

