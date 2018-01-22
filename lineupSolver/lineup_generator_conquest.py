from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *

possible_playoff_decks = [
    'Aggro Druid',
    'Jade Druid',
    'Quest Druid', # Combo Druid
    'Aggro Hunter',
    'Secret Mage',
    'Big Spell Mage',
    'Exodia Mage',
    'Tempo Rogue',
    'Quest Rogue',
    'Aggro Paladin',
    'Control Paladin',
    'Murloc Paladin',
    'Highlander Priest',
    'Dragon Priest',
    #'Spiteful Priest',
    'Cube Warlock',
    'Demon Warlock',
    'Zoo Warlock',
    #'Pirate Warrior',
]


if __name__ == '__main__':

    level1, level2, level3, level4, level5, level6, level7 = None, None, None, None, None, None, None

    #level1 = "Highlander Priest,Murloc Paladin,Tempo Rogue,Demon Warlock".split(',')
    #level1 = "Highlander Priest,Demon Warlock,Tempo Rogue,Aggro Druid".split(',')
    level1 = "Highlander Priest,Demon Warlock,Big Spell Mage,Tempo Rogue".split(',')
    level2 = "Highlander Priest,Demon Warlock,Jade Druid,Big Spell Mage".split(',')
    level3 = "Highlander Priest,Cube Warlock,Jade Druid,Tempo Rogue".split(',')
    level4 = "Highlander Priest,Demon Warlock,Jade Druid,Tempo Rogue".split(',')
    level5 = "Highlander Priest,Cube Warlock,Aggro Druid,Tempo Rogue".split(',')
    level6 = "Jade Druid,Exodia Mage,Highlander Priest,Cube Warlock".split(',')
    lineups_to_test = [l for l in [level1, level2, level3, level4, level5, level6, level7] if l is not None]
    weights = [1 for l in [level1, level2, level3, level4, level5, level6, level7] if l is not None]


    import sys
    args = sys.argv[1:]
    worlds = {
        "Ant"                : "Aggro Druid,Spiteful Priest,Murloc Paladin,Tempo Rogue",
        "Docpwn"             : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Fr0zen"             : "Big Spell Mage,Cube Warlock,Highlander Priest,Jade Druid",
        "Hoej"               : "Aggro Druid,Demon Warlock,Highlander Priest,Murloc Paladin",
        "JasonZhou"          : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "Kolento"            : "Demon Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Muzzy"              : "Aggro Druid,Cube Warlock,Highlander Priest,Tempo Rogue",
        "Neirea"             : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "OmegaZero"          : "Aggro Druid,Demon Warlock,Highlander Priest,Murloc Paladin",
        "Orange"             : "Aggro Hunter,Demon Warlock,Highlander Priest,Tempo Rogue",
        "Purple"             : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "SamuelTsao"         : "Aggro Druid,Highlander Priest,Tempo Rogue,Zoo Warlock",
        "ShtanUdachi"        : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Sintolol"           : "Big Spell Mage,Demon Warlock,Dragon Priest,Jade Druid",
        "Surrender"          : "Aggro Druid,Cube Warlock,Highlander Priest,Tempo Rogue",
        "tom60229"           : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
    }
    group_c = {
        "Ant"                : "Aggro Druid,Spiteful Priest,Murloc Paladin,Tempo Rogue",
        "Purple"             : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "ShtanUdachi"        : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Sintolol"           : "Big Spell Mage,Demon Warlock,Dragon Priest,Jade Druid",
    }
    group_d = {
        "Fr0zen"             : "Big Spell Mage,Cube Warlock,Highlander Priest,Jade Druid",
        "Neirea"             : "Aggro Druid,Demon Warlock,Highlander Priest,Tempo Rogue",
        "OmegaZero"          : "Aggro Druid,Demon Warlock,Highlander Priest,Murloc Paladin",
        "Surrender"          : "Aggro Druid,Cube Warlock,Highlander Priest,Tempo Rogue",
    }
    inverse = {}
    for i,j in worlds.items():
        inverse[j] = i
    if len(args) > 0 and args[0] == 'practice':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=25)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        for opp_lineup in lineups_to_test:
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            print ",".join([str(i) for i in [opp_lineup, ban, win_pct]])
            # BAN STUFF
            showBans = False
            if showBans:
                print my_lineup, "vs", opp_lineup
                win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
                res = pre_ban_old(my_lineup,
                                  opp_lineup,
                                  win_pcts)
                print ""
                print my_lineup, "vs", opp_lineup
                print "bans"
                print "%-20s %-20s" % ("p1_ban", "p2_ban")
                #for i, j in sorted(res.items(), key=lambda x:-x[1]):
                for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                    d1, d2 = i
                    print '%-20s %-20s %s' % (d1, d2, round(j,4))
            print "\n\n"
    elif len(args) > 0 and args[0] == 'Fr0zen':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=25)
        players = sorted(worlds.keys())
        p1 = 'Fr0zen'
        
        win_pcts[("Big Spell Mage","Murloc Paladin")] = 0.60
        win_pcts[("Big Spell Mage","Aggro Druid")] = 0.60
        win_pcts[("Big Spell Mage","Tempo Rogue")] = 0.67
        win_pcts[("Big Spell Mage","Spiteful Priest")] = 0.31
        win_pcts[("Big Spell Mage","Aggro Hunter")] = 0.50
        win_pcts[("Big Spell Mage","Demon Warlock")] = 0.35
        win_pcts[("Big Spell Mage","Cube Warlock")] = 0.15
        win_pcts[("Jade Druid","Tempo Rogue")] = 0.55
        win_pcts[("Jade Druid","Murloc Paladin")] = 0.40
        win_pcts[("Jade Druid","Aggro Hunter")] = 0.45
        win_pcts[("Jade Druid","Cube Warlock")] = 0.40
        win_pcts[("Jade Druid","Demon Warlock")] = 0.40
        win_pcts[("Jade Druid","Aggro Druid")] = 0.55
        win_pcts[("Jade Druid","Spiteful Priest")] = 0.35
        win_pcts[("Cube Warlock","Aggro Druid")] = 0.56
        win_pcts[("Cube Warlock","Tempo Rogue")] = 0.60
        win_pcts[("Cube Warlock","Jade Druid")] = 0.55
        win_pcts[("Cube Warlock","Cube Warlock")] = 0.45
        win_pcts[("Cube Warlock","Demon Warlock")] = 0.45
        win_pcts[("Highlander Priest","Jade Druid")] = 0.42
        
        for p2 in players:
            if p1 == p2: continue
            if p2 in ["tom60229", "ShtanUdachi", "OmegaZero", "Neirea"]:
                # Auctioneer
                win_pcts[("Big Spell Mage","Highlander Priest")] = 0.60
                win_pcts[("Cube Warlock","Highlander Priest")] = 0.40
                win_pcts[("Jade Druid","Highlander Priest")] = 0.70
            else:
                # Lyra
                win_pcts[("Big Spell Mage","Highlander Priest")] = 0.50
                win_pcts[("Cube Warlock","Highlander Priest")] = 0.45
                win_pcts[("Jade Druid","Highlander Priest")] = 0.60
            deck_1 = worlds.get(p1)
            deck_2 = worlds.get(p2)
            my_lineup = [d.strip() for d in deck_1.split(',')]
            opp_lineup = [d.strip() for d in deck_2.split(',')]
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            print ",".join([str(i) for i in [p1, p2, ban, win_pct]])
            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
            # BAN STUFF
            res = pre_ban_old(my_lineup,
                              opp_lineup,
                              win_pcts)
            print ""
            print my_lineup, "vs", opp_lineup
            print "bans"
            print "%-20s %-20s" % ("p1_ban", "p2_ban")
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                d1, d2 = i
                print '%-20s %-20s %s' % (d1, d2, round(j,4))
            print "\n\n"
    elif len(args) > 0 and args[0] == 'worlds':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=25)
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
                ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
                print ",".join([str(i) for i in [p1, p2, ban, win_pct]])
    elif len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=25)
        print sorted(archetypes)
        archetypes.append('Unbeatable')
        for a in archetypes:
            if a != 'Fatigue Warrior':
                win_pcts[('Fatigue Warrior',a)] = 0.4
                win_pcts[(a,'Fatigue Warrior')] = 0.6
            win_pcts[('Fatigue Warrior', 'Big Spell Mage')] = 0.6
            win_pcts[('Fatigue Warrior', 'Tempo Rogue')] = 0.65
            win_pcts[('Fatigue Warrior', 'Aggro Paladin')] = 0.50
            win_pcts[('Big Spell Mage', 'Fatigue Warrior')] = 0.4
            win_pcts[('Tempo Rogue', 'Fatigue Warrior')] = 0.35
            win_pcts[('Aggro Paladin', 'Fatigue Warrior')] = 0.50
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
        win_rates_grid(my_lineup, opp_lineup, win_pcts,num_games)
        if len(my_lineup) < 4 or len(opp_lineup) < 4:
            print round(post_ban(my_lineup, opp_lineup, win_pcts) * 100,2)
        else:
            print win_rate(my_lineup, opp_lineup, win_pcts)
            print pre_ban(my_lineup, opp_lineup, win_pcts)

            res = pre_ban_old(my_lineup,
                              opp_lineup,
                              win_pcts)
            print ""
            print my_lineup, "vs", opp_lineup
            print "bans"
            print "%-20s %-20s" % ("p1_ban", "p2_ban")
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                d1, d2 = i
                print '%-20s %-20s %s' % (d1, d2, round(j,4))

        my_lineup, opp_lineup = opp_lineup, my_lineup
        print my_lineup, "vs", opp_lineup
        win_rates_grid(my_lineup, opp_lineup, win_pcts,num_games)
        print win_rate(my_lineup, opp_lineup, win_pcts)
        print pre_ban(my_lineup, opp_lineup, win_pcts)

        res = pre_ban_old(my_lineup,
                          opp_lineup,
                          win_pcts)
        print ""
        print my_lineup, "vs", opp_lineup
        print "bans"
        print "%-20s %-20s" % ("p1_ban", "p2_ban")
        #for i, j in sorted(res.items(), key=lambda x:-x[1]):
        for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
            d1, d2 = i
            print '%-20s %-20s %s' % (d1, d2, round(j,4))

    else:
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=20, min_game_count=20, min_win_pct=0.42,limitTop=25)
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
        excluded = ['Spiteful Priest', 'Secret Mage', 'Big Priest', 'Mill Rogue', 'Pirate Warrior', 'Spiteful Warrior', 'Miracle Rogue', 'Barnes Hunter', 'Jade Druid']
        #excluded = ['Secret Mage', 'Barnes Hunter', 'Secret Hunter']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        win_rates_against_good = {}

        lineups, archetype_map = generate_lineups(archetypes)
        print "testing %s lineups" % len(lineups)

        
    
        #### ESPORTS ARENA
        #usingEsportsArena = True
        usingEsportsArena = False
        if usingEsportsArena:
            lineups_to_test = [i.split(',') for i in worlds.values()]
            weights = [1 for i in worlds.values()]
            lineups = lineups_to_test


        #weights = [2,2,1]
        if len(args) > 0 and args[0] == 'target':
            lineups_to_test = []
            for x in args[1:]:
                tmp = [i.strip() for i in x.split(',')]
                lineups_to_test.append(tmp)
            weights = [1 for i in lineups_to_test]
        elif len(args) > 0 and args[0] == 'playoff':
            archetypes = possible_playoff_decks
            lineups, archetype_map = generate_lineups(archetypes)
            lineups_to_test = []
            for x in args[1:]:
                tmp = [i.strip() for i in x.split(',')]
                lineups_to_test.append(tmp)
            weights = [1 for i in lineups_to_test]
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
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-10:]:
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            if usingEsportsArena:
                print "%-20s: " % inverse[i]
            print "".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()
