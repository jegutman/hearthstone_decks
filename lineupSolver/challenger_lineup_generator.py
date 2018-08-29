from __future__ import print_function
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
        "Odd Warrior,Malygos Druid,Deathrattle Hunter",
        "Zoo Warlock,Shudderwock Shaman,Token Druid",
        "Quest Rogue,Shudderwock Shaman,Odd Quest Warrior",
        "Miracle Rogue,Deathrattle Hunter,Even Warlock",
        "Zoo Warlock,Odd Paladin,Odd Rogue",
        "Miracle Rogue,Odd Paladin,Even Warlock",
        "Even Warlock,Deathrattle Hunter,Token Druid",
        "Even Warlock,Malygos Druid,Deathrattle Hunter",
        "Malygos Druid,Odd Warrior,Quest Rogue",
        "Big Druid,Deathrattle Hunter,Control Warlock",
        "Zoo Warlock,Token Druid,Odd Rogue",
        "Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
        "Odd Paladin,Control Warlock,Odd Rogue",
        "Zoo Warlock,Odd Rogue,Deathrattle Hunter",
        "Control Priest,Odd Rogue,Even Warlock",
        "Control Warrior,Control Warlock,Deathrattle Hunter",
        "Tempo Mage,Miracle Rogue,Deathrattle Hunter",
        "Control Warlock,Quest Rogue,Mill Druid",
        "Odd Rogue,Deathrattle Hunter,Odd Warrior",
        "Zoo Warlock,Odd Rogue,Odd Paladin",
        "Malygos Druid,Deathrattle Hunter,Midrange Shaman",
        "Even Warlock,Deathrattle Hunter,Malygos Druid",
        "Odd Paladin,Zoo Warlock,Mill Druid",
        "Even Warlock,Control Priest,Odd Rogue",
        "Even Warlock,Odd Rogue,Midrange Shaman",
        "Control Warlock,Mech Paladin,Recruit Warrior",
        "Big Druid,Recruit Warrior,Odd Rogue",
        "Deathrattle Hunter,Odd Rogue,Control Warlock",
        "Malygos Druid,Control Warlock,Control Priest",
        "Spell Hunter,Control Warlock,Token Druid",
        "Even Warlock,Deathrattle Hunter,Taunt Druid",
        "Deathrattle Hunter,Odd Warrior,Malygos Druid",
        "Big Druid,Deathrattle Hunter,Even Warlock",
        "Tempo Mage,Even Warlock,Quest Rogue",
        "Malygos Druid,Control Warlock,Miracle Rogue",
        "Control Warlock,Malygos Druid,Spell Hunter",
        "Odd Rogue,Spell Hunter,Taunt Druid",
        "Malygos Druid,Deathrattle Hunter,Even Warlock",
        "Even Warlock,Odd Paladin,Control Priest",
        "Even Warlock,Odd Rogue,Taunt Druid",
        "Kingsbane Rogue,Token Druid,Deathrattle Hunter",
        "Odd Rogue,Deathrattle Hunter,Malygos Druid",
        "Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
        "Deathrattle Hunter,Malygos Druid,Odd Rogue",
        "Control Warlock,Odd Rogue,Odd Paladin",
        "Zoo Warlock,Deathrattle Hunter,Odd Rogue",
        "Deathrattle Hunter,Zoo Warlock,Malygos Druid",
        "Big Druid,Control Priest,Even Warlock",
        "Shudderwock Shaman,Token Druid,Zoo Warlock",
        "Malygos Druid,Odd Paladin,Control Warlock",
        "Even Warlock,Malygos Druid,Odd Rogue",
        "Even Warlock,Odd Warrior,Malygos Druid",
        "Big Spell Mage,Deathrattle Hunter,Zoo Warlock",
    ]
    lineups_to_test = [l.split(',') for l in lineups_to_test]
    weights = [1 for l in lineups_to_test]


    import sys
    args = sys.argv[1:]
    custom = {
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
        samples = []
        bans = {}
        line = ['deck1', 'deck2', 'deck3', 'deck4', 'win_pct', 'ban', 'opp_win_pct', 'opp_ban', 'ban_details->']
        print(",".join([str(i) for i in line]))
        for opp_lineup, weight in zip(lineups_to_test, weights):
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            win_pct = round(win_rate_nash_calc(my_lineup, opp_lineup, win_pcts), 4)
            bans[ban] = bans.get(ban, 0) + 1
            #second_ban = sorted(win_rate(my_lineup, opp_lineup, win_pcts).items())[-2][0]
            if win_pct > 0:
                count += weight
                total += win_pct * weight
                samples.append(win_pct)
                values.append(win_pct)
            
            opp_ban, opp_win_pct = win_rate(opp_lineup, my_lineup, win_pcts)
            #print ",".join([str(i) for i in [win_pct, opp_lineup, ban, win_pct, "weight", weight]])
            printCsv = True
            if not printCsv:
                print("%-80s %-7s %-20s %-7s %-s" % (opp_lineup, win_pct, ban, opp_win_pct, opp_ban))
                print("    ", win_rate(my_lineup, opp_lineup, win_pcts))
                print("    ",pre_ban(my_lineup, opp_lineup, win_pcts), "\n")
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
                print(my_lineup, "vs", opp_lineup)
                win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
                res = pre_ban_old(my_lineup,
                                  opp_lineup,
                                  win_pcts)
                print("")
                print(my_lineup, "vs", opp_lineup)
                print("bans")
                print("%-20s %-20s" % ("p1_ban", "p2_ban", "p1_win_%"))
                #for i, j in sorted(res.items(), key=lambda x:-x[1]):
                for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                    d1, d2 = i
                    print('%-20s %-20s %s' % (d1, d2, round(j,4)))
                print("\n\n")
        print("average: %s" % (total / count))
        print("samples: %s" % sorted(samples))
        print("distr: %s %s" % (len([i for i in samples if i<0.5]), len([i for i in samples if i> 0.50])))
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
                print(",".join([str(i) for i in [p1, p2, ban, win_pct]]))
    elif len(args) > 0 and args[0] == 'simfile':
        
        #win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        win_pcts, archetypes = wr_from_csv('input_wr.csv', scaling=100)
        print(sorted(archetypes, key=lambda x:x.split()[-1]))
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

        print(my_lineup, "vs", opp_lineup)
        win_rates_grid(my_lineup, opp_lineup, win_pcts)
        if len(my_lineup) < 4 or len(opp_lineup) < 4:
            print(round(post_ban(my_lineup, opp_lineup, win_pcts) * 100,2))
        else:
            print(win_rate(my_lineup, opp_lineup, win_pcts))
            print(pre_ban(my_lineup, opp_lineup, win_pcts))

            res = pre_ban_old(my_lineup,
                              opp_lineup,
                              win_pcts)
            print("")
            print(my_lineup, "vs", opp_lineup)
            print("bans")
            print("%-20s %-20s" % ("p1_ban", "p2_ban"))
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                d1, d2 = i
                print('%-20s %-20s %s' % (d1, d2, round(j,4)))

        my_lineup, opp_lineup = opp_lineup, my_lineup
        print(my_lineup, "vs", opp_lineup)
        win_rates_grid(my_lineup, opp_lineup, win_pcts)
        print(win_rate(my_lineup, opp_lineup, win_pcts))
        print(pre_ban(my_lineup, opp_lineup, win_pcts))

        res = pre_ban_old(my_lineup,
                          opp_lineup,
                          win_pcts)
        print("")
        print(my_lineup, "vs", opp_lineup)
        print("bans")
        print("%-20s %-20s" % ("p1_ban", "p2_ban"))
        #for i, j in sorted(res.items(), key=lambda x:-x[1]):
        for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
            d1, d2 = i
            print('%-20s %-20s %s' % (d1, d2, round(j,4)))

    elif len(args) > 0 and args[0] == 'sim':
        
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print(sorted(archetypes, key=lambda x:x.split()[-1]))
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
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        print(my_lineup, "vs", opp_lineup)
        win_rates_grid(my_lineup, opp_lineup, win_pcts,num_games)
        if len(my_lineup) < 3 or len(opp_lineup) < 3:
            print(round(post_ban(my_lineup, opp_lineup, win_pcts) * 100,2))
        else:
            #print(win_rate(my_lineup, opp_lineup, win_pcts))
            print(win_rate_nash_calc(my_lineup, opp_lineup, win_pcts))
            print(pre_ban(my_lineup, opp_lineup, win_pcts))

            res = pre_ban_old(my_lineup,
                              opp_lineup,
                              win_pcts)
            print("")
            print(my_lineup, "vs", opp_lineup)
            print("bans")
            print("%-20s %-20s %s" % ("p1_ban", "p2_ban", "p1_win_%"))
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                d1, d2 = i
                print('%-20s %-20s %s' % (d1, d2, round(j,4)))

        my_lineup, opp_lineup = opp_lineup, my_lineup
        print(my_lineup, "vs", opp_lineup)
        win_rates_grid(my_lineup, opp_lineup, win_pcts,num_games)
        print(win_rate(my_lineup, opp_lineup, win_pcts))
        print(pre_ban(my_lineup, opp_lineup, win_pcts))

        res = pre_ban_old(my_lineup,
                          opp_lineup,
                          win_pcts)
        print("")
        print(my_lineup, "vs", opp_lineup)
        print("bans")
        print("%-20s %-20s %s" % ("p1_ban", "p2_ban", "p1_win_%"))
        #for i, j in sorted(res.items(), key=lambda x:-x[1]):
        for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
            d1, d2 = i
            print('%-20s %-20s %s' % (d1, d2, round(j,4)))

    else:
        #### ESPORTS ARENA
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=20, min_win_pct=0.44,limitTop=30)
        print(sorted(archetypes, key=lambda x:x.split()[-1]))
        excluded = []
        if True:
            excluded += []
            #excluded += ['Tempo Mage', 'Tempo Rogue', 'Murloc Mage', 'Recruit Hunter']
            excluded += ['Spiteful Druid', 'Taunt Druid']
        print("\n\nEXCLUDING:", excluded)
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
        #lineups, archetype_map = generate_lineups(archetypes, additional_archetypes=additional_archetypes, num_classes=4)
        inverse_map = {}
        for i,j in archetype_map.items():
            inverse_map[j] = i
        win_pcts_int = {}
        for i,a in archetype_map.items():
            for j,b in archetype_map.items():
                if (a,b) in win_pcts:
                    win_pcts_int[(i,j)] = win_pcts[(a,b)]
        print_time()
        
        print("testing %s lineups" % len(lineups))
    
        if len(args) > 0 and args[0] == 'target':
            lineups_to_test = []
            for x in args[1:]:
                tmp = [i.strip() for i in x.split(',')]
                lineups_to_test.append(tmp)
            weights = [1 for i in lineups_to_test]
        print("\n")
        print("TESTING vs LINEUPS")
        for l in lineups_to_test:
            print("%-80s" % ("   ".join(l)), '"' + ",".join(l) + '"')
        print("\n")

        count_index = 0
        for lineup in lineups:
            for lu_test in lineups_to_test:
                count_index += 1
                print(count_index, [archetype_map[i] for i in lineup], lu_test)
                lu_test = list(get_lineup(lu_test, inverse_map))
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts_int)]
                #win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate_nash(list(lineup), lu_test, win_pcts_int)]

        for lineup_txt, winrates in sorted(win_rates_against_good.items(), key=lambda x: x[1][0][1], reverse=True)[:3]:
            print(lineup_txt, winrates)

        lu_strings = []
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:geometric_mean([i[1] for i in x[1]],weights))[-10:]:
        print_time()
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 2 + min([i[1] for i in x[1]]))[-10:]:
        max_output = 40
        max_file_output = 100
        for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))[-max_file_output:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([1 if i[1] > 0.5 else 0 for i in x[1]]))[-max_file_output:]:
            i = get_lineup(i, archetype_map)
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print("%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"')
            x = []
            for _i in j:
                x.append((str(archetype_map[_i[0]]), _i[1]))
            j = x
            max_file_output -= 1
            if max_file_output <= max_output:
                print("%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(geometric_mean([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print('         "' + lineup_string + '"')
        for i,j,k,l in lu_strings:
            print("".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals())
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
