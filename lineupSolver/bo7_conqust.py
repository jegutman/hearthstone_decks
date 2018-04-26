from json_win_rates import * 
from conquest_utils import * 
from shared_utils import *

if __name__ == '__main__':

    level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12, level13, level14, level15, level16 = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    #level1 = "Cube Warlock,Spiteful Priest,Murloc Paladin,Quest Rogue".split(',')
    #level2 = "Zoo Warlock,Spiteful Priest,Murloc Paladin,Secret Mage".split(',')
    #level3 = "Cube Warlock,Control Priest,Silver Hand Paladin,Token Shaman".split(',')
    level1 = "Cube Warlock,Secret Mage,Combo Priest,Murloc Paladin".split(',')
    level2 = "Cube Warlock,Control Priest,Token Shaman,Silver Hand Paladin".split(',')
    level3 = "Cube Warlock,Quest Rogue,Spiteful Priest,Murloc Paladin".split(',')
    level4 = "Spell Hunter,Zoo Warlock,Murloc Paladin,Token Shaman".split(',')

    #level1 = "Unbeatable,Spiteful Priest,Murloc Paladin,Quest Rogue".split(',')
    #level2 = "Zoo Warlock,Spiteful Priest,Murloc Paladin,Secret Mage".split(',')
    #level3 = "Unbeatable,Control Priest,Silver Hand Paladin,Token Shaman".split(',')

    lineups_to_test = [l for l in [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12, level13, level14, level15, level16] if l is not None]
    weights = [1 for l in [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12, level13, level14, level15, level16] if l is not None]
    weights = [2,0,2]


    import sys
    args = sys.argv[1:]
    custom = {
        'Akumaker'      :   "Big Priest,Murloc Paladin,Cube Warlock,Secret Mage",
        'Angrycarp'     :   "Big Priest,Quest Rogue,Secret Mage,Cube Warlock",
        'Disdai'        :   "Cube Warlock,Big Spell Mage,Spiteful Priest,Quest Warrior",
        'Ender'         :   "Spiteful Priest,Murloc Paladin,C'Thun Druid,Secret Mage",
        #'GhostASA'      :   "Quest Rogue,Quest Druid,OTK DK Paladin,Jade Shaman",
        'Glory'         :   "Cube Warlock,Big Priest,Big Spell Mage,OTK DK Paladin",
        'Hearthstoner'  :   "Cube Warlock,Murloc Paladin,Spell Hunter,Combo Priest",
        'Hikage7'       :   "Secret Mage,Zoo Warlock,Combo Priest,Murloc Paladin",
        'Hotmeowth'     :   "Cube Warlock,Big Spell Mage,OTK DK Paladin,Spiteful Priest",
        'Jakattack'     :   "Cube Warlock,Spiteful Priest,Secret Mage,OTK DK Paladin",
        'Khaius'        :   "Murloc Paladin,Secret Mage,Cube Warlock,Combo Priest",
        'Kin0531'       :   "Cube Warlock,Spiteful Priest,Silver Hand Paladin,Secret Mage",
        'Odyssey'       :   "Control Warlock,Spiteful Priest,Secret Mage,Quest Rogue",
        'Okasinnsuke'   :   "Combo Priest,Secret Mage,Cube Warlock,Spell Hunter",
        'ProfessorOak'  :   "Cube Warlock,Silver Hand Paladin,Big Priest,Spell Hunter",
        'WaningMoon'    :   "Cube Warlock,Murloc Paladin,Secret Mage,Combo Priest",
    }
    #useCustom = True
    useCustom = False
    if useCustom:
        lineups_to_test = []
        weights = []
        for i in custom.values():
            lineups_to_test.append(i.split(','))
            weights.append(1)
    inverse = {}
    for i,j in custom.items():
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
    elif len(args) > 0 and args[0] == 'custom':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        win_pcts[('Control Warrior', 'Control Warrior')] = 0.5
        players = sorted(custom.keys())
        for p1 in players:
            for p2 in players:
                if p1 == p2: continue
                deck_1 = custom.get(p1)
                deck_2 = custom.get(p2)
                my_lineup = [d.strip() for d in deck_1.split(',')]
                opp_lineup = [d.strip() for d in deck_2.split(',')]
                assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
                assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
                ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
                print ",".join([str(i) for i in [p1, p2, ban, win_pct]])
    elif len(args) > 0 and args[0] == 'sim':
        
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print sorted(archetypes, key=lambda x:x.split()[-1])
        archetypes.append('Unbeatable')
        #archetypes.append('Fatigue Warrior')
        overrides = [
                     #('Highlander Priest', 'Jade Druid', 0.45),
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
        if args[1] in custom.keys():
            args[1] = custom.get(args[1])
        if args[2] in custom.keys():
            args[2] = custom.get(args[2])
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
        #### ESPORTS ARENA
        #usingEsportsArena = True
        usingEsportsArena = False
        if usingEsportsArena:
            win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=200, min_game_count=100, min_win_pct=0.40,limitTop=100)
        else:
            win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=200, min_game_count=100, min_win_pct=0.40,limitTop=30)
        print sorted(archetypes, key=lambda x:x.split()[-1])
        excluded = []
        if False:
            excluded += ['Spiteful Druid', 'Control Warrior', 'Spell Hunter']
            #excluded += ['Jade Druid', 'Kingsbane Rogue', 'Big Priest']
            #excluded += ['Spell Hunter']
        #excluded = ['Control Hunter', 'Spell Hunter']
        #excluded = ['Tempo Druid', 'Pirate Warrior', 'Spell Hunter', 'Control Hunter', 'Aggro Hunter', 'Midrange Hunter']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        win_rates_against_good = {}

        lineups, archetype_map = generate_lineups(archetypes, num_classes=5)
        # FILTER LINEUPS
        filterLineups = False
        if filterLineups:
            tmp = []
            for lineup in lineups:
                lineup_tmp = get_lineup(lineup, archetype_map)
                if 'Cube Warlock' in lineup_tmp and 'Murloc Paladin' in lineup_tmp and 'Spiteful Priest' in lineup_tmp:
                    tmp.append(lineup)
            lineups = tmp
        
        print "testing %s lineups" % len(lineups)

        
    
        if usingEsportsArena:
            lineups_to_test = [i.split(',') for i in custom.values()]
            #for my_lineup in lineups_to_test:
            #    assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            weights = [1 for i in custom.values()]
            #for i in lineups_to_test:
            #    print i
            #assert False
            lineups = lineups_to_test


        #weights = [2,2,1]
        if len(args) > 0 and args[0] == 'target':
            lineups_to_test = []
            for x in args[1:]:
                tmp = [i.strip() for i in x.split(',')]
                lineups_to_test.append(tmp)
            weights = [1 for i in lineups_to_test]
        print "\n"
        print "TESTING vs LINEUPS"
        for l in lineups_to_test:
            print "%-80s" % ("   ".join(l)), '"' + ",".join(l) + '"'
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
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 2 + min([i[1] for i in x[1]]))[-10:]:
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
