import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

if __name__ == '__main__':

    level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12, level13, level14, level15, level16 = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    #level1 = "Secret Mage,Big Priest,Cube Warlock,Murloc Paladin".split(',')
    level2 = "Cube Warlock,Spell Hunter,Jade Druid,Silver Hand Paladin".split(',')
    level3 = "Silver Hand Paladin,Spell Hunter,Cube Warlock,Combo Priest".split(',')
    level4 = "Secret Hunter,Big Spell Mage,Combo Priest,Cube Warlock".split(',')

    lineups_to_test = [
        'Taunt Druid,Control Priest,Miracle Rogue,Cube Warlock',
        'Taunt Druid,Recruit Hunter,Shudderwock Shaman,Even Warlock',
        'Big Spell Mage,Miracle Rogue,Shudderwock Shaman,Even Warlock',
        'Taunt Druid,Combo Priest,Shudderwock Shaman,Even Warlock',
        'Taunt Druid,Miracle Rogue,Shudderwock Shaman,Cube Warlock',
        'Big Spell Mage,Control Priest,Miracle Rogue,Even Warlock',
        'Token Druid,Odd Paladin,Even Shaman,Even Warlock',
        'Token Druid,Odd Paladin,Shudderwock Shaman,Cube Warlock',
        'Taunt Druid,Recruit Hunter,Miracle Rogue,Shudderwock Shaman',
        'Taunt Druid,Big Spell Mage,Shudderwock Shaman,Quest Warrior',
        'Taunt Druid,Big Spell Mage,Control Priest,Even Warlock',
        'Taunt Druid,Recruit Hunter,Miracle Rogue,Even Warlock',
        'Token Druid,Odd Paladin,Even Shaman,Even Warlock',
        'Big Spell Mage,Miracle Rogue,Shudderwock Shaman,Even Warlock',
        'Spiteful Druid,Recruit Hunter,Miracle Rogue,Even Warlock',
        'Taunt Druid,Miracle Rogue,Even Shaman,Even Warlock',
    ]
    lineups_to_test = [l.split(',') for l in lineups_to_test]
    weights = [1 for l in lineups_to_test]
    #lineups_to_test.append("Token Druid,Odd Paladin,Shudderwock Shaman,Cube Warlock".split(','))
    #weights.append(5)
    
    #weights = [5, 5, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #weights = [11, 6, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #weights = [18, 6, 6, 5, 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
    #weights = []
    #for i in range(0,16):
    #    weights.append(1)
    #weights.append(10)
    #weights.append(10)
    #assert len(weights) == len(lineups_to_test) == 17, "size not 17 %s %s" % (len(weights), len(lineups_to_test))

    #weights = [3,1,1,1]


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
        overrides = [
            #('Zoo Warlock', 'Even Paladin', .48),
            #('Zoo Warlock', 'Tempo Mage', .60),
            #('Zoo Warlock', 'Odd Rogue', .55),
            #('Zoo Warlock', 'Spiteful Druid', .60),
            ('Zoo Warlock', 'Even Paladin', .47),
            ('Zoo Warlock', 'Tempo Mage', .55),
            ('Zoo Warlock', 'Odd Rogue', .42),
            ('Zoo Warlock', 'Spiteful Druid', .50),
            ('Zoo Warlock', 'Cube Warlock', .30),
            ('Zoo Warlock', 'Control Warlock', .30),
            #('Zoo Warlock', 'Quest Rogue', .65),
            ('Zoo Warlock', 'Quest Rogue', .65),
            ('Zoo Warlock', 'Control Priest', .43),
            ('Zoo Warlock', 'Murloc Paladin', .50),
            ('Zoo Warlock', 'Taunt Druid', .55),
            ('Zoo Warlock', 'Odd Warrior', .50),
            ('Zoo Warlock', 'Miracle Rogue', .55),
            ('Zoo Warlock', 'Spell Hunter', .43),
            ('Zoo Warlock', 'Even Shaman', .47),
            ('Zoo Warlock', 'Quest Warrior', .45),
            ('Zoo Warlock', 'Quest Druid', .65),
            ('Zoo Warlock', 'Zoo Warlock', .50),
            ('Even Shaman', 'Tempo Mage', .70),
            ('Even Shaman', 'Quest Rogue', .60),
            ('Even Shaman', 'Murloc Paladin', .62),

            ('Control Priest', 'Quest Rogue', .42),
            ('Control Priest', 'Spiteful Druid', .40),
            ('Tempo Mage', 'Quest Rogue', 0.63),
            ('Even Paladin', 'Quest Rogue', 0.63),
                    ]
        win_pcts = override_wr(overrides,win_pcts)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        count, total = 0, 1.0
        line = ['deck1', 'deck2', 'deck3', 'deck4', 'win_pct', 'ban', 'opp_win_pct', 'opp_ban', 'ban_details->']
        print(",".join([str(i) for i in line]))
        for opp_lineup, weight in zip(lineups_to_test, weights):
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            #second_ban = sorted(win_rate(my_lineup, opp_lineup, win_pcts).items())[-2][0]
            if win_pct > 0:
                count += weight
                total *= win_pct ** weight
            
            opp_ban, opp_win_pct = win_rate(opp_lineup, my_lineup, win_pcts)
            #print ",".join([str(i) for i in [win_pct, opp_lineup, ban, win_pct, "weight", weight]])
            printCsv = True
            if not printCsv:
                print "%-80s %-7s %-20s %-7s %-s" % (opp_lineup, win_pct, ban, opp_win_pct, opp_ban)
                print "    ", win_rate(my_lineup, opp_lineup, win_pcts)
                print "    ",pre_ban(my_lineup, opp_lineup, win_pcts), "\n"
            else:
                line = []
                for l in opp_lineup:
                    line.append(l)
                line.append(win_pct)
                line.append(ban)
                line.append(opp_win_pct)
                line.append(opp_ban)
                for i, j in sorted(pre_ban(my_lineup, opp_lineup, win_pcts).items(), key=lambda x:x[1], reverse=True):
                    line.append(i)
                    line.append(j)
                print(",".join([str(i) for i in line]))
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
                print "%-20s %-20s" % ("p1_ban", "p2_ban", "p1_win_%")
                #for i, j in sorted(res.items(), key=lambda x:-x[1]):
                for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                    d1, d2 = i
                    print '%-20s %-20s %s' % (d1, d2, round(j,4))
                print "\n\n"
        print("average: %s" % (total ** (1./count)))
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
    elif len(args) > 0 and args[0] == 'simfile':
        
        #win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        win_pcts, archetypes = wr_from_csv('input_wr.csv', scaling=100)
        print sorted(archetypes, key=lambda x:x.split()[-1])
        archetypes.append('Unbeatable')
        #archetypes.append('Fatigue Warrior')
        overrides = [
                    ]
        win_pcts = override_wr(overrides,win_pcts)
        if args[1] in custom.keys():
            args[1] = custom.get(args[1])
        if args[2] in custom.keys():
            args[2] = custom.get(args[2])
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        #assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        print my_lineup, "vs", opp_lineup
        win_rates_grid(my_lineup, opp_lineup, win_pcts)
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
        win_rates_grid(my_lineup, opp_lineup, win_pcts)
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

    elif len(args) > 0 and args[0] == 'sim':
        
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print sorted(archetypes, key=lambda x:x.split()[-1])
        archetypes.append('Unbeatable')
        #archetypes.append('Fatigue Warrior')
        overrides = [
            #('Zoo Warlock', 'Even Paladin', .48),
            #('Zoo Warlock', 'Tempo Mage', .60),
            #('Zoo Warlock', 'Odd Rogue', .55),
            #('Zoo Warlock', 'Spiteful Druid', .60),
            ('Zoo Warlock', 'Even Paladin', .47),
            ('Zoo Warlock', 'Tempo Mage', .55),
            ('Zoo Warlock', 'Odd Rogue', .42),
            ('Zoo Warlock', 'Spiteful Druid', .50),
            ('Zoo Warlock', 'Cube Warlock', .30),
            ('Zoo Warlock', 'Control Warlock', .30),
            #('Zoo Warlock', 'Quest Rogue', .65),
            ('Zoo Warlock', 'Quest Rogue', .65),
            ('Zoo Warlock', 'Control Priest', .43),
            ('Zoo Warlock', 'Murloc Paladin', .50),
            ('Zoo Warlock', 'Taunt Druid', .55),
            ('Zoo Warlock', 'Odd Warrior', .50),
            ('Zoo Warlock', 'Miracle Rogue', .55),
            ('Zoo Warlock', 'Spell Hunter', .43),
            ('Zoo Warlock', 'Even Shaman', .47),
            ('Zoo Warlock', 'Quest Warrior', .45),
            ('Zoo Warlock', 'Quest Druid', .65),
            ('Zoo Warlock', 'Zoo Warlock', .50),
            ('Even Shaman', 'Tempo Mage', .70),
            ('Even Shaman', 'Quest Rogue', .60),
            ('Even Shaman', 'Murloc Paladin', .62),

            ('Control Priest', 'Quest Rogue', .42),
            ('Control Priest', 'Spiteful Druid', .40),
            ('Tempo Mage', 'Quest Rogue', 0.63),
            ('Even Paladin', 'Quest Rogue', 0.63),
                    ]
        win_pcts = override_wr(overrides,win_pcts)
        if args[1] in custom.keys():
            args[1] = custom.get(args[1])
        if args[2] in custom.keys():
            args[2] = custom.get(args[2])
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

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
            print "%-20s %-20s %s" % ("p1_ban", "p2_ban", "p1_win_%")
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
        print "%-20s %-20s %s" % ("p1_ban", "p2_ban", "p1_win_%")
        #for i, j in sorted(res.items(), key=lambda x:-x[1]):
        for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
            d1, d2 = i
            print '%-20s %-20s %s' % (d1, d2, round(j,4))

    else:
        #### ESPORTS ARENA
        #usingEsportsArena = True
        usingEsportsArena = False
        if usingEsportsArena:
            win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=50, min_win_pct=0.44,limitTop=100)
        else:
            win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=50, min_win_pct=0.44,limitTop=30)
        print sorted(archetypes, key=lambda x:x.split()[-1])
        excluded = []
        if True:
            excluded += []
            #excluded += ['Cube Warlock']
            #excluded += ['Spiteful Druid', 'Kingsbane Rogue', 'Quest Mage']
            #excluded += ['Odd Paladin', 'Big Spell Mage', 'Quest Rogue']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        win_rates_against_good = {}

        lineups, archetype_map = generate_lineups(archetypes)
        # FILTER LINEUPS
        filterLineups = False
        if filterLineups:
            tmp = []
            for lineup in lineups:
                lineup_tmp = get_lineup(lineup, archetype_map)
                if 'Cube Warlock' in lineup_tmp or 'Control Warlock' in lineup_tmp:
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
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:geometric_mean([i[1] for i in x[1]],weights))[-10:]:
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 2 + min([i[1] for i in x[1]]))[-10:]:
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(geometric_mean([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            if usingEsportsArena:
                print "%-20s: " % inverse[i]
            print "".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()
