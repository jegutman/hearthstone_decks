from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *


if __name__ == '__main__':

    import sys
    args = sys.argv[1:]
    worlds = {
        "Sintolol"           : "Big Spell Mage,Demon Warlock,Dragon Priest,Jade Druid",
        "Muzzy"              : "Aggro Druid,Cube Warlock,Highlander Priest,Tempo Rogue",
        "Purple"             : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "tom60229"           : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "JasonZhou"          : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "Ant"                : "Aggro Druid,Spiteful Priest,Murloc Paladin,Tempo Rogue",
        "SamuelTsao"         : "Aggro Druid,Highlander Priest,Tempo Rogue,Zoo Warlock",
        "ShtanUdachi"        : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Hoej"               : "Aggro Druid,Demon Warlock,Highlander Priest,Murloc Paladin",
        "OmegaZero"          : "Aggro Druid,Demon Warlock,Highlander Priest,Murloc Paladin",
        "Kolento"            : "Demon Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Orange"             : "Aggro Hunter,Demon Warlock,Highlander Priest,Tempo Rogue",
        "Fr0zen"             : "Big Spell Mage,Cube Warlock,Highlander Priest,Jade Druid",
        "Neirea"             : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "Surrender"          : "Aggro Druid,Cube Warlock,Highlander Priest,Tempo Rogue",
        "Docpwn"             : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
    }
    inverse = {}
    for i,j in worlds.items():
        inverse[j] = i
    if len(args) > 0 and args[0] == 'worlds':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        players = sorted(worlds.keys())
        for p1 in players:
            for p2 in players:
                if p1 == p2: continue
                deck_1 = worlds.get(p1)
                deck_2 = worlds.get(p2)
                my_lineup = [d.strip() for d in deck_1.split(',')]
                opp_lineup = [d.strip() for d in deck_2.split(',')]
                assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
                assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

                #a, b = my_lineup, opp_lineup
                #print my_lineup, "vs", opp_lineup
                #win_rates_grid(my_lineup, opp_lineup, win_pcts)
                ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
                print ",".join([str(i) for i in [p1, p2, ban, win_pct]])
                #print pre_ban(my_lineup, opp_lineup, win_pcts)
    elif len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print sorted(archetypes)
        if args[1] in worlds.keys():
            args[1] = worlds.get(args[1])
        if args[2] in worlds.keys():
            args[2] = worlds.get(args[2])
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        #a, b = my_lineup, opp_lineup
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

        my_lineup, opp_lineup = opp_lineup, my_lineup
        print my_lineup, "vs", opp_lineup
        win_rates_grid(my_lineup, opp_lineup, win_pcts)
        print win_rate(my_lineup, opp_lineup, win_pcts)
        print pre_ban(my_lineup, opp_lineup, win_pcts)

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
        #excluded = ['Murloc Paladin']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        lineups, archetype_map = generate_lineups(archetypes)
        print "testing %s lineups" % len(lineups)
        win_rates_against_good = {}
        level1, level2, level3, level4, level5 = None, None, None, None, None

        target_ban = 'No_ban'
        #target_ban = 'Cube Warlock'

        #level1 = "Highlander Priest,Murloc Paladin,Tempo Rogue,Demon Warlock".split(',')
        #level1 = "Highlander Priest,Murloc Paladin,Tempo Rogue,Unbeatable".split(',')
        #level1 = "Highlander Priest,Murloc Paladin,Unbeatable,Demon Warlock".split(',')
        #level1 = "Unbeatable,Murloc Paladin,Tempo Rogue,Demon Warlock".split(',')
        lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
        weights = [1 for l in [level1, level2, level3, level4, level5] if l is not None]
        
        #### ESPORTS ARENA
        #usingEsportsArena = True
        usingEsportsArena = False
        if usingEsportsArena:
            lineups_to_test = [i.split(',') for i in worlds.values()]
            weights = [1 for i in worlds.values()]
            lineups = lineups_to_test


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
            if not usingEsportsArena:
                lineup = get_lineup(lineup, archetype_map)
            else:
                lineup = tuple(lineup)
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
            if usingEsportsArena:
                print "%-20s: " % inverse[i]
            print "".join(["%-27s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()
