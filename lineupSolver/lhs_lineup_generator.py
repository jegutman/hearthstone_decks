from json_win_rates import * 
from lhs_utils import * 
from shared_utils import *

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
    if len(args) > 0 and args[0] == 'sim':
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        if len(my_lineup) == 4:

            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts)
            print win_rate(my_lineup, opp_lineup, win_pcts)
            print pre_ban(my_lineup, opp_lineup, win_pcts)

            res = pre_matrix(my_lineup,
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
        elif len(my_lineup) <= 3:
            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts)
            #print win_rate(my_lineup, opp_lineup, win_pcts)
            #print pre_ban(my_lineup, opp_lineup, win_pcts)

            res = lead_matrix(my_lineup,
                              opp_lineup,
                              win_pcts)
            print ""
            print my_lineup, "vs", opp_lineup
            print "bans"
            print "%-18s %-18s" % ("p1_ban", "p2_ban")
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][1], -x[1])):
                d1, d2 = i
                print '%-18s %-18s %s' % (d1, d2, round(j,4))
            
    else:
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=100, min_game_count=1500)
        for key in win_pcts.keys():
            i,j = key
            bias = 0.00
            if i == 'Highlander Priest':
                win_pcts[key] += bias
            if j == 'Highlander Priest':
                win_pcts[key] -= bias
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
        # force ban druid
        #level1 = ['Tempo Rogue', 'Jade Druid', 'Highlander Priest', 'Murloc Paladin']
        #level1 = ['Big Priest', 'Control Mage', 'Jade Druid', 'Tempo Rogue']
        #level1 = ['Big Druid', 'Dragon Priest', 'Zoo Warlock', 'Tempo Rogue']
        #level2 = ['Tempo Rogue', 'Secret Mage', 'Highlander Priest', 'Demon Warlock']
        level1 = ['Highlander Priest', 'Demon Warlock', 'Secret Mage', 'Tempo Rogue']
        #level3 = 'Tempo Rogue,Zoo Warlock,Murloc Paladin,Secret Mage'.split(',')
        #level4 = ['Tempo Rogue', 'Unbeatable', 'Highlander Priest', 'Zoo Warlock']
        #level3 = ['Tempo Rogue', 'Unbeatable', 'Murloc Paladin', 'Zoo Warlock']

        lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
        #from lineups_from_1129 import lineups
        #print lineups_to_test
        #lineups_to_test = [sorted(x.split(',')) for x in lineups.values()][:2]
        #print lineups_to_test
        tmp_weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        weights = [w for w,l in zip(tmp_weights, lineups_to_test) if l is not None]

        print "\n"
        print "TESTING vs LINEUPS"
        for l in lineups_to_test:
            print "   ".join(l), '"' + ",".join(l) + '"'
        print "\n"

        for lineup in lineups:
            for lu_test in lineups_to_test:
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts, useGlobal=True)]

        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-10:]:
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
            i_print = "    " + "".join(["%-20s" % x for x in i])
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'

