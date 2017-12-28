from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *


if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=100, min_game_count=100)
        #print archetypes 
        archetypes += ['Unbeatable']
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
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=200, min_win_pct=0.4)
        for key in win_pcts.keys():
            i,j = key
            bias = 0.00
            if i == 'Highlander Priest':
                win_pcts[key] += bias
            if j == 'Highlander Priest':
                win_pcts[key] -= bias
        #win_pcts[('Demon Warlock', 'Highlander Priest')] = 0.45
        #win_pcts[('Highlander Priest', 'Demon Warlock')] = 0.55
        #win_pcts[('Demon Warlock', 'Secret Mage')] = 0.50
        #win_pcts[('Secret Mage', 'Demon Warlock')] = 0.5
        print archetypes 
        excluded = []
        #excluded = ['Jade Druid']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        lineups = generate_lineups(archetypes, unbeatable=True)
        archetypes += ['Unbeatable']
        win_rates_against_good = {}
        level1, level2, level3, level4, level5 = None, None, None, None, None
        #level1 = "Recruit Warrior,Demon Warlock,Highlander Priest,Unbeatable".split(',')
        level1 = "Demon Warlock,Highlander Priest,Tempo Rogue,Unbeatable".split(',')
        level2 = "Tempo Rogue,Highlander Priest,Secret Mage,Unbeatable".split(',')
        #level1 = "Tempo Rogue,Highlander Priest,Aggro Druid,Unbeatable".split(',')
        #level2 = "Aggro Paladin,Highlander Priest,Aggro Druid,Unbeatable".split(',')
        lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
        weights = [1 for l in [level1, level2, level3, level4, level5] if l is not None]
        #weights = [1 for l in lineups_to_test if l is not None]
        #weights = [4, 4, 2]
        #from canada_wesg import lineups_to_test, weights
        assert all([len(x) == 4 for x in lineups_to_test])
        print "testing %s lineups" % len(lineups_to_test)

        for i in lineups:
            #print i
            assert all([d in archetypes for d in i]), ([d in archetypes for d in i], i)
            

        print "\n"
        print "TESTING vs LINEUPS"
        for l in lineups_to_test:
            print "   ".join(l), "     ", '"' + ",".join(l) + '"'
        print "\n"

        for lineup in lineups:
            for lu_test in lineups_to_test:
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts)]

        for i,j in sorted(win_rates_against_good.items())[:3]:
            print i,j 

        lu_strings = []
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-10:]:
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3),round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            print "".join(["%20s" % x for x in i.split(',')]), j, k, l, i
