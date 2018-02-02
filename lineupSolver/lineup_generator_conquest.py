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
    # FIRST PASS
    level1 = "Highlander Priest,Demon Warlock,Big Spell Mage,Jade Druid".split(',')
    level2 = "Highlander Priest,Demon Warlock,Big Spell Mage,N'Zoth Paladin".split(',')
    level3 = "Highlander Priest,Cube Warlock,Jade Druid,Tempo Rogue".split(',')
    level4 = "Zoo Warlock,Aggro Druid,Murloc Paladin,Tempo Rogue".split(',')
    #level6 = "Jade Druid,Exodia Mage,Highlander Priest,Cube Warlock".split(',')
    # SECOND PASS
    #level1 = "Highlander Priest,Demon Warlock,Tempo Rogue,Big Spell Mage".split(',')
    #level2 = "Highlander Priest,Cube Warlock,Jade Druid,Tempo Rogue".split(',')
    #level3 = "Highlander Priest,Cube Warlock,Jade Druid,Tempo Rogue".split(',')
    #level1 = "Dragon Priest,Secret Mage,Tempo Rogue,Cube Warlock".split(',')
    lineups_to_test = [l for l in [level1, level2, level3, level4, level5, level6, level7] if l is not None]
    weights = [1 for l in [level1, level2, level3, level4, level5, level6, level7] if l is not None]


    import sys
    args = sys.argv[1:]
    worlds = {
        "AnguiStar"         : "Aggro Druid,Big Spell Mage,Demon Warlock,Highlander Priest",
        "Arreador"          : "Tempo Rogue,Big Spell Mage,Demon Warlock,Spiteful Priest",
        "Astrogation"       : "Recruit Warrior,Spiteful Priest,Cube Warlock,Secret Mage",
        "DacLue"            : "Jade Druid,Big Spell Mage,Cube Warlock,Highlander Priest",
        "DiegoDias"         : "Fatigue Warrior,Big Spell Mage,Demon Warlock,Highlander Priest",
        "DonAndres"         : "Big Priest,Demon Warlock,Jade Druid,Secret Mage",
        "Fenom"             : "Cube Warlock,Highlander Priest,Exodia Mage,Quest Rogue",
        "Gallon"            : "Spiteful Priest,Cube Warlock,Pirate Warrior,Tempo Rogue",
        "Garifar"           : "Dragon Priest,Jade Druid,Tempo Rogue,Zoo Warlock",
        "Gladen99"          : "Demon Warlock,Big Spell Mage,Highlander Priest,Jade Druid",
        "Gutxi"             : "Aggro Druid,Highlander Priest,Murloc Paladin,Tempo Rogue",
        "iamChapsgg"        : "Aggro Paladin,Big Spell Mage,Jade Druid,Tempo Rogue",
        "Joaquin"           : "Cube Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Juristis"          : "Demon Warlock,Highlander Priest,Jade Druid,Quest Rogue",
        "Kuonet"            : "Big Spell Mage,Cube Warlock,Highlander Priest,Jade Druid",
        "LegolaS"           : "Big Spell Mage,Demon Warlock,Highlander Priest,Jade Druid",
        "MixKokinho"        : "Big Spell Mage,Demon Warlock,Highlander Priest,Tempo Rogue",
        "Mokranichile"      : "Demon Warlock,Highlander Priest,Jade Druid,Tempo Rogue",
        "Monsanto"          : "Dragon Priest,Quest Druid,Exodia Mage,Quest Rogue",
        "Neves"             : "Cube Warlock,Highlander Priest,Jade Druid,Miracle Rogue",
        "Nourish"           : "Aggro Druid,Murloc Paladin,Secret Mage,Tempo Rogue",
        "Perna"             : "Big Spell Mage,N'Zoth Paladin,Demon Warlock,Highlander Priest",
        "Pinche"            : "Big Spell Mage,Cube Warlock,Highlander Priest,Jade Druid",
        "Rase"              : "Big Spell Mage,N'Zoth Paladin,Demon Warlock,Highlander Priest",
        "seohyun628"        : "Big Spell Mage,Fatigue Warrior,Highlander Priest,Demon Warlock",
        "sid"               : "Cube Warlock,Highlander Priest,Jade Druid,Exodia Mage",
        "thetrueasian"      : "Highlander Priest,Cube Warlock,Aggro Hunter,Aggro Paladin",
        "tyler"             : "Highlander Priest,Cube Warlock,Quest Druid,Quest Rogue",
        "Valash"            : "Highlander Priest,Demon Warlock,Jade Druid,Big Spell Mage",
        "vny"               : "Highlander Priest,Demon Warlock,N'Zoth Paladin,Big Spell Mage",
        "yinus"             : "Big Spell Mage,Cube Warlock,Jade Druid,Highlander Priest",
        "zlsjs"             : "Big Spell Mage,Fatigue Warrior,Highlander Priest,Demon Warlock",
    }
    inverse = {}
    for i,j in worlds.items():
        inverse[j] = i
    if len(args) > 0 and args[0] == 'practice':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        for opp_lineup in lineups_to_test:
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            print ",".join([str(i) for i in [opp_lineup, ban, win_pct]])
            print win_rate(my_lineup, opp_lineup, win_pcts)
            print pre_ban(my_lineup, opp_lineup, win_pcts)
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
    elif len(args) > 0 and args[0] == 'worlds':
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
                ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
                print ",".join([str(i) for i in [p1, p2, ban, win_pct]])
    elif len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print sorted(archetypes)
        archetypes.append('Unbeatable')
        overrides = [
                     ('Highlander Priest', 'Jade Druid', 0.45),
                     #('Big Spell Mage', 'Highlander Priest', 0.6),
                     #('Fatigue Warrior', 'Big Spell Mage',  0.8),
                     #('Fatigue Warrior', 'Highlander Priest',  0.35),
                     #('Fatigue Warrior', 'Tempo Rogue',  0.55),
                     #('Fatigue Warrior', 'Demon Warlock', 0.25),
                     #('Cube Warlock', 'Demon Warlock', 0.55),
                    ]
        #for a in archetypes:
        #    if a != 'Fatigue Warrior':
        #        win_pcts[('Fatigue Warrior',a)] = 0.4
        #        win_pcts[(a,'Fatigue Warrior')] = 0.6
        win_pcts = override_wr(overrides,win_pcts)
        #win_pcts[('Big Spell Mage', 'Big Spell Mage')] = 0.4
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
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=20, min_game_count=20, min_win_pct=0.42,limitTop=40)
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
        win_pcts[('Highlander Priest', 'Jade Druid')] = 0.45
        win_pcts[('Jade Druid', 'Highlander Priest')] = 0.55
        print sorted(archetypes)
        excluded = ['Elemental Priest']
        excluded += ['Big Priest', 'Mill Rogue', 'Spiteful Priest', 'Jade Druid', 'OTK DK Paladin', 'Token Shaman', 'Spiteful Warrior']
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
