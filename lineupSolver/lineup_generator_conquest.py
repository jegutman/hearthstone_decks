from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *


if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print sorted(archetypes)
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
        print "%-27s %-27s" % ("p1_ban", "p2_ban")
        #for i, j in sorted(res.items(), key=lambda x:-x[1]):
        for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
            d1, d2 = i
            print '%-27s %-27s %s' % (d1, d2, round(j,4))

    else:
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=200, min_win_pct=0.4)
        for key in win_pcts.keys():
            i,j = key
            bias = 0.00
            if i == 'Highlander Priest':
                win_pcts[key] += bias
            if j == 'Highlander Priest':
                win_pcts[key] -= bias
            bias = 0.00
            if i == 'Aggro Paladin':
                win_pcts[key] += bias
            if j == 'Aggro Paladin':
                win_pcts[key] -= bias
        print sorted(archetypes)
        excluded = []
        #excluded = ['Exodia Mage', 'Quest Druid', 'Quest Rogue', 'Silver Hand Paladin', 'Secret Mage']
        excluded = ['Murloc Paladin']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        lineups, archetype_map = generate_lineups(archetypes)
        print "testing %s lineups" % len(lineups)
        win_rates_against_good = {}
        level1, level2, level3, level4, level5 = None, None, None, None, None

        target_ban = 'No_ban'
        #target_ban = 'Cube Warlock'

        level1 = 'Highlander Priest,Demon Warlock,Secret Mage,Tempo Rogue'.split(',')
        #level2 = "Jade Druid,Aggro Hunter,Dragon Priest,Cube Warlock".split(',')
        lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
        weights = [1 for l in [level1, level2, level3, level4, level5] if l is not None]
        #weights = [2,2,1]
        if len(args) > 0 and args[0] == 'target':
            level1 = [i.strip() for i in args[1].split(',')]
            weights = [1]
            lineups_to_test = [level1]
        print "\n"
        print "TESTING vs LINEUPS"
        for l in lineups_to_test:
            print "   ".join(l), '"' + ",".join(l) + '"'
        print "\n"

        for lineup in lineups:
            lineup = get_lineup(lineup, archetype_map)
            for lu_test in lineups_to_test:
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts)]

        for i,j in sorted(win_rates_against_good.items())[:3]:
            print i,j 

        lu_strings = []
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-10:]:
            i_print = "    " + "".join(["%-27s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            print "".join(["%-27s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()
