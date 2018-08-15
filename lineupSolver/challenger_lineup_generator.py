import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

import datetime

def print_time():
    print(datetime.datetime.now())

if __name__ == '__main__':

    level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12, level13, level14, level15, level16 = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    lineups_to_test = [
        "Odd Warrior,Shudderwock Shaman,Malygos Druid",
        "Odd Rogue,Token Druid,Deathrattle Hunter",
        "Shudderwock Shaman,Mech Rogue,Even Warlock",
        "Control Priest,Control Warlock,Token Druid",
        "Malygos Druid,Even Warlock,Big Spell Mage",
        "Big Spell Mage,Control Warlock,Shudderwock Shaman",
        "Deathrattle Hunter,Malygos Druid,Control Warlock",
        "Deathrattle Hunter,Control Warlock,Malygos Druid",
        "Malygos Druid,Mecha'thun Priest,Even Warlock",
        "Taunt Druid,Deathrattle Hunter,Even Shaman",
        "Token Shaman,Big Druid,Deathrattle Hunter",
        "Even Warlock,Malygos Druid,Odd Paladin",
        "Deathrattle Rogue,Deathrattle Hunter,Zoo Warlock",
        "Shudderwock Shaman,Combo Priest,Odd Warrior",
        "Odd Paladin,Odd Rogue,Zoo Warlock",
        "Even Warlock,Even Shaman,Big Druid",
        "Even Warlock,Shudderwock Shaman,Big Spell Mage",
        "Odd Rogue,Malygos Druid,Zoo Warlock",
        "Odd Paladin,Even Warlock,Big Spell Mage",
        "Odd Warrior,Big Spell Mage,Malygos Druid",
        "Big Spell Mage,Malygos Druid,Control Warlock",
        "Even Shaman,Odd Warrior,Even Warlock",
        "Tempo Mage,Deathrattle Hunter,Mech Rogue",
        "Miracle Rogue,Mill Druid,Zoo Warlock",
        "Malygos Druid,Quest Warrior,Deathrattle Hunter",
        "Even Warlock,Recruit Warrior,Spell Hunter",
        "Big Spell Mage,Mill Druid,Control Warlock",
        "Zoo Warlock,Spell Hunter,Big Spell Mage",
        "Malygos Druid,Miracle Rogue,Control Priest",
        "Zoo Warlock,Odd Rogue,Spell Hunter",
        "Shudderwock Shaman,Odd Paladin,Even Warlock",
        "Tempo Mage,Zoo Warlock,Mecha'thun Druid",
        "Even Warlock,Shudderwock Shaman,Deathrattle Hunter",
        "Big Spell Mage,Even Mecha'thun Warlock,Mecha'thun Druid",
        "Odd Warrior,Token Druid,Spell Hunter",
        "Tempo Mage,Odd Rogue,Even Warlock",
        "Odd Rogue,Zoo Warlock,Tempo Mage",
        "Big Spell Mage,Zoo Warlock,Mech Rogue",
        "Murloc Paladin,Malygos Druid,Zoo Warlock",
        "Tempo Mage,Token Druid,Zoo Warlock",
        "Taunt Druid,Control Warlock,Shudderwock Shaman",
        "Even Warlock,Odd Rogue,Malygos Druid",
        "Big Druid,Big Spell Mage,Zoo Warlock",
        "Mill Druid,Miracle Rogue,Even Warlock",
        "Even Warlock,Control Priest,Shudderwock Shaman",
        "Odd Rogue,Odd Warrior,Zoo Warlock",
        "Mill Druid,Control Warlock,Mecha'thun Priest",
        "Big Spell Mage,Spell Hunter,Even Warlock",
        "Shudderwock Shaman,Malygos Druid,Odd Rogue",
        "Quest Warrior,Spell Hunter,Big Spell Mage",
        "Token Shaman,Malygos Druid,Zoo Warlock",
        "Zoo Warlock,Big Druid,Deathrattle Hunter",
        "Odd Rogue,Tempo Mage,Zoo Warlock",
        "Control Warlock,Combo Priest,Mill Druid",
        "Odd Rogue,Malygos Druid,Even Warlock",
        "Control Priest,Even Shaman,Odd Rogue",
        "Even Warlock,Malygos Druid,Mech Hunter",
        "Odd Rogue,Control Priest,Odd Paladin",
        "Kingsbane Rogue,Big Druid,Even Warlock",
        "Shudderwock Shaman,Cube Warlock,Deathrattle Hunter",
        "Shudderwock Shaman,Zoo Warlock,Malygos Druid",
        "Odd Paladin,Deathrattle Rogue,Zoo Warlock",
        "Malygos Druid,Big Spell Mage,Even Warlock",
        "Shudderwock Shaman,Big Druid,Control Warlock",
        "Zoo Warlock,Midrange Hunter,Odd Rogue",
        "Big Druid,Odd Paladin,Odd Rogue",
        "Mill Druid,Deathrattle Hunter,Even Warlock",
        "Kingsbane Rogue,Quest Warrior,Zoo Warlock",
        "Even Warlock,Odd Rogue,Malygos Druid",
        "Big Spell Mage,Odd Warrior,Control Warlock",
        "Zoo Warlock,Spell Hunter,Big Spell Mage",
        "Malygos Druid,Even Warlock,Quest Warrior",
        "Odd Rogue,Tempo Mage,Odd Paladin",
        "Zoo Warlock,Recruit Warrior,Malygos Druid",
        "Odd Paladin,Odd Rogue,Zoo Warlock",
        "Big Druid,Zoo Warlock,Murloc Paladin",
        "Malygos Druid,Even Warlock,Even Shaman",
        "Malygos Druid,Control Warlock,Shudderwock Shaman",
        "Big Spell Mage,Control Warlock,Shudderwock Shaman",
        "Zoo Warlock,Deathrattle Hunter,Mech Rogue",
        "Quest Warrior,Even Warlock,Miracle Rogue",
        "Zoo Warlock,Malygos Druid,Odd Rogue",
        "Malygos Druid,Even Warlock,Spell Hunter",
        "Combo Priest,Malygos Druid,Zoo Warlock",
        "Malygos Druid,Even Warlock,Tempo Mage",
        "Even Warlock,Spell Hunter,Malygos Druid",
        "Control Warlock,Recruit Warrior,Mill Druid",
        "Odd Warrior,Control Warlock,Combo Priest",
        "Miracle Rogue,Odd Paladin,Zoo Warlock",
        "Miracle Rogue,Malygos Druid,Even Warlock",
        "Zoo Warlock,Odd Paladin,Token Druid",
        "Malygos Druid,Cube Warlock,Tempo Mage",
        "Odd Warrior,Odd Rogue,Zoo Warlock",
        "Zoo Warlock,Odd Rogue,Token Druid",
        "Zoo Warlock,Odd Paladin,Odd Rogue",
        "Mecha'thun Priest,Zoo Warlock,Tempo Mage",
        "Even Warlock,Quest Warrior,Shudderwock Shaman",
        "Zoo Warlock,Mill Druid,Spell Hunter",
        "Mech Hunter,Malygos Druid,Even Mecha'thun Warlock",
        "Tempo Mage,Odd Rogue,Even Warlock",
        "Mecha'thun Priest,Quest Warrior,Mill Druid",
        "Cube Warlock,Deathrattle Hunter,Big Spell Mage",
        "Malygos Druid,Zoo Warlock,Odd Paladin",
        "Zoo Warlock,Odd Paladin,Token Druid",
        "Zoo Warlock,Odd Rogue,Shudderwock Shaman",
        "Big Spell Mage,Token Shaman,Big Druid",
        "Even Warlock,Even Shaman,Big Druid",
        "Tempo Mage,Even Warlock,Mill Druid",
        "Big Spell Mage,Malygos Druid,Control Warlock",
        "Mill Druid,Tempo Mage,Zoo Warlock",
    ]
    lineups_to_test = [l.split(',') for l in lineups_to_test]
    weights = [1 for l in lineups_to_test]


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
                    ]
        win_pcts = override_wr(overrides,win_pcts)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        count, total = 0, 0.0
        values = []
        bans = {}
        line = ['deck1', 'deck2', 'deck3', 'deck4', 'win_pct', 'ban', 'opp_win_pct', 'opp_ban', 'ban_details->']
        print(",".join([str(i) for i in line]))
        for opp_lineup, weight in zip(lineups_to_test, weights):
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            bans[ban] = bans.get(ban, 0) + 1
            #second_ban = sorted(win_rate(my_lineup, opp_lineup, win_pcts).items())[-2][0]
            if win_pct > 0:
                count += weight
                total += win_pct * weight
                values.append(win_pct)
            
            opp_ban, opp_win_pct = win_rate(opp_lineup, my_lineup, win_pcts)
            #print ",".join([str(i) for i in [win_pct, opp_lineup, ban, win_pct, "weight", weight]])
            printCsv = True
            if not printCsv:
                print "%-80s %-7s %-20s %-7s %-s" % (opp_lineup, win_pct, ban, opp_win_pct, opp_ban)
                print "    ", win_rate(my_lineup, opp_lineup, win_pcts)
                print "    ",pre_ban(my_lineup, opp_lineup, win_pcts), "\n"
            else:
                line = []
                line.append(ban)
                line.append('     ')
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
        print("average: %s" % (total / count))
        print("min: %s" % min(values))
        print("bans: %s" % sorted(bans.items(), key=lambda x:x[1], reverse=True))
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
                        ('Miracle Rogue', 'Combo Priest', 0.6),
                        ('Deathrattle Hunter', 'Combo Priest', 0.4),
                        ('Deathrattle Hunter', 'Combo Priest', 0.4),
                        ('Miracle Rogue', 'Quest Rogue', 0.6),
                        ('Miracle Rogue', 'Big Druid', 0.6),
                        ('Miracle Rogue', 'Even Warlock', 0.6),
                        ('Even Warlock', 'Combo Priest', 0.6),
                        ('Even Warlock', 'Quest Rogue', 0.35),
                        ('Malygos Druid', 'Combo Priest', 0.6),
                        ('Miracle Rogue', 'Tempo Mage', 0.4),
                        ('Miracle Rogue', 'Spell Hunter', 0.3),
                        ('Miracle Rogue', 'Odd Rogue', 0.35),
                        ('Miracle Rogue', 'Malygos Druid', 0.5),
                        ('Miracle Rogue', 'Odd Paladin', 0.42),
                        ('Miracle Rogue', 'Zoo Warlock', 0.35),
                        ('Miracle Rogue', 'Shudderwock Shaman', 0.62),
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
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=20, min_win_pct=0.44,limitTop=50)
        print sorted(archetypes, key=lambda x:x.split()[-1])
        excluded = []
        if False:
            excluded += []
            #excluded += ['Tempo Mage', 'Tempo Rogue', 'Murloc Mage', 'Recruit Hunter']
            #excluded += ['Spiteful Druid', 'Kingsbane Rogue', 'Quest Mage']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]
        win_rates_against_good = {}

        print_time()
        additional_archetypes = []
        for lu_test in lineups_to_test:
            for a in lu_test:
                if a not in archetypes:
                    print("Rare Archetypes: %s" % a)
                    additional_archetypes.append(a)
        lineups, archetype_map = generate_lineups(archetypes, additional_archetypes=additional_archetypes, num_classes=3)
        inverse_map = {}
        for i,j in archetype_map.items():
            inverse_map[j] = i
        win_pcts_int = {}
        for i,a in archetype_map.items():
            for j,b in archetype_map.items():
                if (a,b) in win_pcts:
                    win_pcts_int[(i,j)] = win_pcts[(a,b)]
        print_time()
        
        print "testing %s lineups" % len(lineups)
    
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
            for lu_test in lineups_to_test:
                lu_test = list(get_lineup(lu_test, inverse_map))
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts_int)]

        for lineup_txt, winrates in sorted(win_rates_against_good.items(), key=lambda x: x[1][0][1], reverse=True)[:3]:
            print lineup_txt, winrates

        lu_strings = []
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:geometric_mean([i[1] for i in x[1]],weights))[-10:]:
        print_time()
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 2 + min([i[1] for i in x[1]]))[-10:]:
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-40:]:
            i = get_lineup(i, archetype_map)
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            x = []
            for _i in j:
                x.append((str(archetype_map[_i[0]]), _i[1]))
            j = x
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(geometric_mean([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            print "".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()
        classes = ['Druid', 'Mage', 'Shaman', 'Priest', 'Hunter', 'Paladin', 'Rogue', 'Warrior', 'Warlock']
        file = open('tmp_output.csv', 'w')
        res = ['win pct'] + classes
        file.write(",".join(res) + '\n')
        for i,j,k,l in lu_strings:
            res = [str(j)]
            for c in classes:
                res.append(" ".join([d for d in i.split(',') if d.split(' ')[-1] == c]))
            #print(",".join(res))
            file.write(",".join(res) + '\n')
