from json_win_rates import * 
from lhs_utils import * 
from shared_utils import *

if __name__ == '__main__':
    level1, level2, level3, level4, level5 = None, None, None, None, None
    level1 = "Cube Warlock,Even Paladin,Control Priest,Odd Rogue".split(',')
    #level2 = "Zoo Warlock,Murloc Paladin,Spiteful Priest,Secret Mage".split(',')
    #level3 = "Cube Warlock,Combo Priest,Silver Hand Paladin,Quest Rogue".split(',')

    lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
    tmp_weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    lineups_to_test = [
        'Cube Warlock,Spell Hunter,Big Spell Mage,Recruit Warrior',
        'Cube Warlock,Token Druid,Spell Hunter,Tempo Mage',
        'Malygos Druid,Even Warlock,Miracle Rogue,Spell Hunter',
        'Miracle Rogue,Control Priest,Token Druid,Even Warlock',
        'Miracle Rogue,Cube Warlock,Token Druid,Quest Warrior',
        'Murloc Paladin,Token Druid,Control Priest,Shudderwock Shaman',
        'Odd Paladin,Token Druid,Cube Warlock,Recruit Warrior',
        'Odd Paladin,Token Druid,Miracle Rogue,Even Warlock',
        'Odd Paladin,Token Druid,Spell Hunter,Cube Warlock',
        'Token Druid,Quest Priest,Odd Paladin,Zoo Warlock',
        'Quest Priest,Taunt Druid,Recruit Warrior,Cube Warlock',
        'Quest Warrior,Even Warlock,Even Shaman,Token Druid',
        'Quest Warrior,Malygos Druid,Miracle Rogue,Even Warlock',
        'Quest Warrior,Odd Rogue,Cube Warlock,Tempo Mage',
        'Quest Warrior,Spell Hunter,Token Druid,Cube Warlock',
        'Quest Warrior,Token Druid,Cube Hunter,Cube Warlock',
        'Recruit Warrior,Token Druid,Spell Hunter,Cube Warlock',
        'Shudderwock Shaman,Cube Warlock,Quest Warrior,Token Druid',
        'Shudderwock Shaman,Recruit Warrior,Cube Warlock,Spell Hunter',
        'Shudderwock Shaman,Spell Hunter,Tempo Mage,Quest Warrior',
        'Shudderwock Shaman,Spell Hunter,Token Druid,Quest Rogue',
        'Spell Hunter,Miracle Rogue,Cube Warlock,Taunt Druid',
        'Spell Hunter,Tempo Mage,Cube Warlock,Miracle Rogue',
        'Spell Hunter,Token Druid,Cube Warlock,Quest Warrior',
        'Spell Hunter,Token Druid,Miracle Rogue,Even Warlock',
        'Spiteful Druid,Big Spell Mage,Miracle Rogue,Spell Hunter',
        'Spiteful Druid,Big Spell Mage,Spell Hunter,Miracle Rogue',
        'Taunt Druid,Big Spell Mage,Even Warlock,Quest Warrior',
        'Taunt Druid,Miracle Rogue,Cube Warlock,Recruit Warrior',
        'Taunt Druid,Odd Rogue,Spell Hunter,Cube Warlock',
        'Taunt Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock',
        'Tempo Mage,Odd Rogue,Cube Warlock,Quest Warrior',
        'Token Druid,Combo Priest,Miracle Rogue,Cube Warlock',
        'Token Druid,Even Shaman,Even Warlock,Odd Warrior',
        'Token Druid,Even Shaman,Even Warlock,Quest Warrior',
        'Token Druid,Even Warlock,Quest Warrior,Big Spell Mage',
        'Token Druid,Miracle Rogue,Cube Warlock,Quest Warrior',
        'Token Druid,Miracle Rogue,Cube Warlock,Quest Warrior',
        'Token Druid,Miracle Rogue,Cube Warlock,Quest Warrior',
        'Token Druid,Miracle Rogue,Shudderwock Shaman,Cube Warlock',
        'Token Druid,Miracle Rogue,Shudderwock Shaman,Cube Warlock',
        'Token Druid,Odd Paladin,Quest Warrior,Cube Warlock',
        'Token Druid,Odd Rogue,Even Shaman,Even Warlock',
        'Token Druid,Recruit Hunter,Cube Warlock,Quest Warrior',
        'Token Druid,Shudderwock Shaman,Cube Warlock,Control Warrior',
        'Token Druid,Shudderwock Shaman,Cube Warlock,Rush Warrior',
        'Token Druid,Shudderwock Shaman,Cube Warlock,Tempo Mage',
        'Token Druid,Spell Hunter,Miracle Rogue,Cube Warlock',
        'Token Druid,Spell Hunter,Miracle Rogue,Even Warlock',
        'Token Druid,Spell Hunter,Shudderwock Shaman,Recruit Warrior',
        'Zoo Warlock,Token Druid,Odd Rogue,Tempo Mage',
    ]
    lineups_to_test = [l.split(',') for l in lineups_to_test]
    weights = [1 for l in lineups_to_test if l is not None]
    #weights = [5,5,4,4,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #weights = [11, 6, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'practice':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
        overrides = [
        ]
        win_pcts = override_wr(overrides,win_pcts)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        total, count = 1.0, 0
        for opp_lineup, weight in zip(lineups_to_test, weights):
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            print ",".join([str(i) for i in [opp_lineup, ban, win_pct]])
            wr =  win_rate(my_lineup, opp_lineup, win_pcts)
            if win_pct > 0:
                count += weight
                total *= win_pct ** weight
            print wr
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
        print("average: %s" % (total ** (1./count)))
    elif len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print len(archetypes), sorted(archetypes, key=class_sort)
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        if len(my_lineup) == 4:

            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
            print win_rate(my_lineup, opp_lineup, win_pcts)
            print pre_ban(my_lineup, opp_lineup, win_pcts)

            print '\nOPP BANS'
            print win_rate(opp_lineup, my_lineup, win_pcts)
            print pre_ban(opp_lineup,my_lineup,win_pcts)

            res = pre_matrix(my_lineup,
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
            print "bans"
            print "%-27s %-27s" % ("p1_ban", "p2_ban")
            for i, j in sorted(res.items(), key=lambda x:(x[0][1], x[1])):
                d1, d2 = i
                print '%-27s %-27s %s' % (d1, d2, round(j,4))
        elif len(my_lineup) <= 3:
            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
            #print win_rate(my_lineup, opp_lineup, win_pcts)
            #print pre_ban(my_lineup, opp_lineup, win_pcts)

            res = lead_matrix(my_lineup,
                              opp_lineup,
                              win_pcts)
            print ""
            print my_lineup, "vs", opp_lineup
            print "leads"
            print "%-27s %-27s" % ("p1_lead", "p2_lead")
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][1], -x[1])):
                d1, d2 = i
                print '%-27s %-27s %s' % (d1, d2, round(j,4))
            
    else:
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=40, min_game_count=20, min_win_pct=0.44,limitTop=30)
        for key in win_pcts.keys():
            i,j = key
            bias = 0.00
            if i == 'Highlander Priest':
                win_pcts[key] += bias
            if j == 'Highlander Priest':
                win_pcts[key] -= bias
            #bias = 0.03
            bias = 0.00
            if i == 'Jade Druid':
                win_pcts[key] += bias
            if j == 'Jade Druid':
                win_pcts[key] -= bias
        print len(archetypes), sorted(archetypes, key=class_sort)

        excluded = []
        #excluded = ['Spiteful Druid', 'Spiteful Priest', 'Miracle Rogue', 'Pirate Warrior']
        #excluded = ['Aggro Hunter', 'Combo Priest', 'Rush Warrior', 'Odd Hunter', 'Odd Paladin']
        #excluded = ['Odd Paladin', 'Cube Warlock', 'Control Warlock']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]

        lineups, archetype_map = generate_lineups(archetypes)

        print "testing %s lineups" % len(lineups)

        win_rates_against_good = {}

        if len(args) > 0 and args[0] == 'target':
            lineups_to_test = []
            for x in args[1:]:
                tmp = [i.strip() for i in x.split(',')]
                lineups_to_test.append(tmp)
            weights = [1 for i in lineups_to_test]
        #if len(args) > 0 and args[0] == 'target':
        #    level1 = [i.strip() for i in args[1].split(',')]
        #    weights = [1]
        #    lineups_to_test = [level1]
        print "\n"
        print "TESTING vs LINEUPS"
        for l in lineups_to_test:
            print "   ".join(l), '"' + ",".join(l) + '"'
        print "\n"

        for lineup in lineups:
            lineup = get_lineup(lineup, archetype_map)
            for lu_test in lineups_to_test:
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts, useGlobal=True)]

        lu_strings = []
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:geometric_mean([i[1] for i in x[1]],weights))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 3 + min([i[1] for i in x[1]]))[-10:]:
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 3 + min([i[1] for i in x[1]]))[-10:]:
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            print "".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()

        #    i_print = "    " + "".join(["%-27s" % x for x in i])
        #    #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
        #    print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
        #    lineup_string = ",".join(i)
        #    lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3),round(min([x[1] for x in j]),3)))
        #    print '         "' + lineup_string + '"'
        #for i,j,k,l in lu_strings:
        #    print "".join(["%-27s" % x for x in i.split(',')]), j, k, l
