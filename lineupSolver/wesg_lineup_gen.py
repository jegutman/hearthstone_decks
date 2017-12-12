from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *


if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=100, min_game_count=100)
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
        win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=100, min_game_count=1000)
        print archetypes 
        excluded = []
        #excluded = ['Murloc Paladin', 'Secret Mage', 'Exodia Mage', 'Aggro-Token Druid', 'Dragon Priest']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded] + ['Unbeatable']
        lineups = generate_lineups(archetypes, unbeatable=True)
        print "testing %s lineups" % len(lineups)
        win_rates_against_good = {}
        level1, level2, level3, level4, level5 = None, None, None, None, None
        level1 = ['Tempo Rogue', 'Big Druid', 'Highlander Priest', 'Murloc Paladin']
        level1 = ['Tempo Rogue', 'Big Druid', 'Highlander Priest', 'Zoo Warlock']
        level1 = ['Princelock Warlock', 'Tempo Rogue', 'Aggro Druid', 'Unbeatable']
        level2 = ['Aggro Druid', 'Tempo Rogue', 'Zoolock Warlock', 'Unbeatable']
        level3 = ['Demonlock Warlock', 'Big Priest', 'Big Druid', 'Unbeatable']
        level4 = ['Murloc Paladin', 'Big Priest', 'Tempo Rogue', 'Unbeatable']
        level5 = ['Murloc Paladin', 'Secret Mage', 'Tempo Rogue', 'Unbeatable']
        lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
        weights = [1 for l in [level1, level2, level3, level4, level5] if l is not None]
        #lineups_to_test = [level1]
        #lineup_01, weight_01 = ['Dragon Priest', 'Secret Mage ', 'Spell Hunter', 'Unbeatable'], 18.0
        #lineup_02, weight_02 = ['Dragon Priest', 'Secret Mage ', 'Tempo Rogue', 'Unbeatable'], 16.0
        #lineup_03, weight_03 = ['Dragon Priest', 'Secret Mage ', 'Unbeatable', 'Zoolock Warlock'], 14.0
        #lineup_04, weight_04 = ['Secret Mage ', 'Spell Hunter', 'Tempo Rogue', 'Unbeatable'], 14.0
        #lineup_05, weight_05 = ['Demonlock Warlock', 'Dragon Priest', 'Secret Mage ', 'Unbeatable'], 14.0
        #lineup_06, weight_06 = ['Secret Mage ', 'Spell Hunter', 'Unbeatable', 'Zoolock Warlock'], 12.0
        #lineup_07, weight_07 = ['Aggro Paladin', 'Dragon Priest', 'Secret Mage ', 'Unbeatable'], 12.0
        #lineup_08, weight_08 = ['Demonlock Warlock', 'Secret Mage ', 'Spell Hunter', 'Unbeatable'], 12.0
        #lineup_09, weight_09 = ['Highlander Priest', 'Secret Mage ', 'Spell Hunter', 'Unbeatable'], 12.0
        #lineup_10, weight_10 = ['Secret Mage ', 'Tempo Rogue', 'Unbeatable', 'Zoolock Warlock'], 11.0
        #lineup_11, weight_11 = ['Dragon Priest', 'Other Hunter', 'Secret Mage ', 'Unbeatable'], 11.0
        #lineup_12, weight_12 = ['Demonlock Warlock', 'Secret Mage ', 'Tempo Rogue', 'Unbeatable'], 11.0
        #lineup_13, weight_13 = ['Highlander Priest', 'Secret Mage ', 'Tempo Rogue', 'Unbeatable'], 11.0
        #lineup_14, weight_14 = ['Big Priest', 'Secret Mage ', 'Spell Hunter', 'Unbeatable'], 11.0
        #lineup_15, weight_15 = ['Aggro Paladin', 'Secret Mage ', 'Spell Hunter', 'Unbeatable'], 10.0
        #lineup_16, weight_16 = ['Dragon Priest', 'Murloc Paladin', 'Secret Mage ', 'Unbeatable'], 10.0
        #lineup_17, weight_17 = ['Dragon Priest', 'Spell Hunter', 'Tempo Rogue', 'Unbeatable'], 10.0
        #lineup_18, weight_18 = ['Big Priest', 'Secret Mage ', 'Tempo Rogue', 'Unbeatable'], 9.0
        #lineup_19, weight_19 = ['Highlander Priest', 'Secret Mage ', 'Unbeatable', 'Zoolock Warlock'], 9.0
        #lineup_20, weight_20 = ['Aggro Paladin', 'Secret Mage ', 'Tempo Rogue', 'Unbeatable'], 9.0
        #lineups_to_test = [lineup_01, lineup_02, lineup_03, lineup_04, lineup_05, lineup_06, lineup_07, lineup_08, lineup_09, lineup_10, lineup_11, lineup_12, lineup_13, lineup_14, lineup_15, lineup_16, lineup_17, lineup_18, lineup_19, lineup_20]
        #weights = [weight_01, weight_02, weight_03, weight_04, weight_05, weight_06, weight_07, weight_08, weight_09, weight_10, weight_11, weight_12, weight_13, weight_14, weight_15, weight_16, weight_17, weight_18, weight_19, weight_20]

        for i in lineups:
            print i
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
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3)))
            print '         "' + lineup_string + '"'
        for i,j in lu_strings:
            print "".join(["%20s" % x for x in i.split(',')]), j
