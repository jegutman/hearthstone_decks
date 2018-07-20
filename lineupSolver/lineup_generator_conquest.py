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
        "Malygos Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
        "Malygos Druid,Control Priest,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Taunt Druid,Shudderwock Shaman,Cube Warlock,Quest Warrior",
        "Token Druid,Odd Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Big Spell Mage,Even Warlock,Quest Warrior",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Big Druid,Deathrattle Hunter,Miracle Rogue,Even Warlock",
        "Token Druid,Murloc Paladin,Zoo Warlock,Quest Warrior",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Malygos Druid,Odd Paladin,Control Priest,Odd Rogue",
        "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Odd Paladin,Odd Rogue,Quest Warrior",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Control Priest,Shudderwock Shaman,Control Warlock,Quest Warrior",
        "Malygos Druid,Deathrattle Hunter,Big Spell Mage,Even Warlock",
        "Big Druid,Deathrattle Hunter,Murloc Mage,Zoo Warlock",
        "Token Druid,Shudderwock Shaman,Cube Warlock,Quest Warrior",
        "Midrange Hunter,Odd Rogue,Even Shaman,Even Warlock",
        "Big Druid,Miracle Rogue,Shudderwock Shaman,Even Warlock",
        "Spell Hunter,Murloc Mage,Miracle Rogue,Cube Warlock",
        "Taunt Druid,Control Priest,Shudderwock Shaman,Cube Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Big Druid,Control Priest,Even Warlock,Quest Warrior",
        "Big Druid,Control Priest,Even Warlock,Quest Warrior",
        "Deathrattle Hunter,Tempo Mage,Odd Rogue,Even Warlock",
        "Big Druid,Control Priest,Even Warlock,Quest Warrior",
        "Malygos Druid,Control Priest,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Control Priest,Shudderwock Shaman,Control Warlock,Recruit Warrior",
        "Malygos Druid,Elemental Mage,Tempo Rogue,Overload Shaman",
        "Combo Priest,Miracle Rogue,Big Spell Mage,Zoo Warlock",
        "Malygos Druid,Control Priest,Shudderwock Shaman,Even Warlock",
        "Token Druid,Miracle Rogue,Shudderwock Shaman,Even Warlock",
        "Spell Hunter,Odd Paladin,Even Shaman,Quest Warrior",
        "Token Druid,Shudderwock Shaman,Cube Warlock,Quest Warrior",
        "Malygos Druid,Control Priest,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Miracle Rogue,Big Spell Mage,Even Warlock",
        "Token Druid,Even Shaman,Cube Warlock,Quest Warrior",
        "Deathrattle Hunter,Odd Paladin,Big Spell Mage,Even Warlock",
        "Token Druid,Shudderwock Shaman,Even Warlock,Quest Warrior",
        "Malygos Druid,Shudderwock Shaman,Even Warlock,Quest Warrior",
        "Big Druid,Control Priest,Even Warlock,Quest Warrior",
        "Malygos Druid,Odd Rogue,Even Warlock,Quest Warrior",
        "Malygos Druid,Resurrect Priest,Miracle Rogue,Cube Warlock",
        "Malygos Druid,Combo Priest,Miracle Rogue,Even Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Malygos Druid,Odd Paladin,Control Priest,Odd Rogue",
        "Big Druid,Miracle Rogue,Shudderwock Shaman,Cube Warlock",
        "Token Druid,Odd Rogue,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Token Druid,Control Priest,Even Warlock,Quest Warrior",
        "Token Druid,Odd Paladin,Even Shaman,Even Warlock",
        "Control Priest,Tempo Rogue,Big Spell Mage,Control Warlock",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Taunt Druid,Control Priest,Shudderwock Shaman,Cube Warlock",
        "Big Druid,Spell Hunter,Miracle Rogue,Cube Warlock",
        "Token Druid,Odd Rogue,Even Shaman,Cube Warlock",
        "Malygos Druid,Control Priest,Cube Warlock,Quest Warrior",
        "Malygos Druid,Deathrattle Hunter,Big Spell Mage,Even Warlock",
        "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Malygos Druid,Control Priest,Shudderwock Shaman,Cube Warlock",
        "Token Druid,Control Priest,Even Warlock,Quest Warrior",
        "Taunt Druid,Control Priest,Cube Warlock,Quest Warrior",
        "Malygos Druid,Elemental Mage,Control Priest,Quest Warrior",
        "Malygos Druid,Odd Paladin,Control Priest,Odd Rogue",
        "Token Druid,Odd Rogue,Even Warlock,Quest Warrior",
        "Malygos Druid,Odd Paladin,Odd Rogue,Big Spell Mage",
        "Taunt Druid,Shudderwock Shaman,Big Spell Mage,Even Warlock",
        "Taunt Druid,Shudderwock Shaman,Cube Warlock,Quest Warrior",
        "Malygos Druid,Odd Paladin,Odd Rogue,Shudderwock Shaman",
        "Malygos Druid,Big Spell Mage,Even Warlock,Quest Warrior",
        "Token Druid,Odd Paladin,Big Spell Mage,Even Warlock",
        "Malygos Druid,Control Priest,Shudderwock Shaman,Quest Warrior",
        "Malygos Druid,Odd Rogue,Big Spell Mage,Even Warlock",
        "Malygos Druid,Big Spell Mage,Even Warlock,Quest Warrior",
        "Token Druid,Odd Paladin,Even Shaman,Zoo Warlock",
        "Token Druid,Tempo Mage,Control Warlock,Quest Warrior",
        "Malygos Druid,Miracle Rogue,Shudderwock Shaman,Cube Warlock",
        "Big Druid,Even Shaman,Big Spell Mage,Cube Warlock",
        "Taunt Druid,Odd Rogue,Big Spell Mage,Zoo Warlock",
        "Malygos Druid,Control Priest,Even Shaman,Even Warlock",
        "Spiteful Druid,Recruit Hunter,Miracle Rogue,Even Warlock",
        "Control Priest,Big Spell Mage,Even Warlock,Quest Warrior",
        "Token Druid,Big Spell Mage,Zoo Warlock,Quest Warrior",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
        "Token Druid,Miracle Rogue,Big Spell Mage,Even Warlock",
        "Mill Druid,Shudderwock Shaman,Big Spell Mage,Quest Warrior",
        "Malygos Druid,Control Priest,Even Warlock,Odd Warrior",
        "Malygos Druid,Recruit Hunter,Odd Paladin,Quest Warrior",
        "Token Druid,Big Spell Mage,Even Warlock,Quest Warrior",
        "Big Druid,Control Priest,Shudderwock Shaman,Cube Warlock",
        "Big Druid,Deathrattle Hunter,Murloc Mage,Miracle Rogue",
        "Malygos Druid,Odd Paladin,Control Priest,Zoo Warlock",
        "Midrange Hunter,Miracle Rogue,Even Shaman,Zoo Warlock",
        "Taunt Druid,Control Priest,Big Spell Mage,Cube Warlock",
        "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Taunt Druid,Odd Paladin,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Control Priest,Big Spell Mage,Quest Warrior",
        "Big Druid,Control Priest,Even Warlock,Quest Warrior",
        "Recruit Hunter,Tempo Mage,Murloc Paladin,Miracle Rogue",
        "Big Druid,Control Priest,Miracle Rogue,Zoo Warlock",
        "Mill Druid,Control Priest,Shudderwock Shaman,Quest Warrior",
        "Control Priest,Big Spell Mage,Even Warlock,Quest Warrior",
        "Malygos Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Malygos Druid,Big Spell Mage,Cube Warlock,Quest Warrior",
        "Token Druid,Control Priest,Even Warlock,Quest Warrior",
        "Token Druid,Odd Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Control Priest,Big Spell Mage,Even Warlock",
        "Malygos Druid,Odd Paladin,Control Priest,Odd Rogue",
        "Control Priest,Shudderwock Shaman,Big Spell Mage,Cube Warlock",
        "Malygos Druid,Odd Rogue,Even Warlock,Quest Warrior",
        "Malygos Druid,Shudderwock Shaman,Big Spell Mage,Even Warlock",
        "Odd Paladin,Control Priest,Miracle Rogue,Even Warlock",
        "Malygos Druid,Odd Rogue,Shudderwock Shaman,Even Warlock",
        "Spiteful Druid,Tempo Mage,Odd Rogue,Even Shaman",
        "Malygos Druid,Big Spell Mage,Even Warlock,Recruit Warrior",
        "Token Druid,Even Shaman,Even Warlock",
        "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Big Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Odd Paladin,Odd Rogue,Big Spell Mage,Even Warlock",
        "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Big Druid,Combo Priest,Miracle Rogue,Big Spell Mage",
        "Token Druid,Tempo Mage,Odd Rogue,Zoo Warlock",
        "Taunt Druid,Spell Hunter,Even Shaman,Big Spell Mage",
        "Odd Paladin,Even Shaman,Big Spell Mage,Even Warlock",
        "Token Druid,Control Priest,Even Shaman,Even Warlock",
        "Taunt Druid,Miracle Rogue,Big Spell Mage,Even Warlock",
        "Recruit Hunter,Odd Rogue,Even Shaman,Zoo Warlock",
        "Malygos Druid,Miracle Rogue,Big Spell Mage,Even Warlock",
        "Big Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
        "Taunt Druid,Shudderwock Shaman,Even Warlock",
        "Spiteful Druid,Spell Hunter,Zoo Warlock",
        "Odd Paladin,Shudderwock Shaman,Zoo Warlock,Quest Warrior",
        "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Token Druid,Odd Paladin,Even Shaman,Cube Warlock",
        "Token Druid,Odd Paladin,Even Warlock,Quest Warrior",
        "Malygos Druid,Control Priest,Even Warlock,Quest Warrior",
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
                    ]
        win_pcts = override_wr(overrides,win_pcts)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        count, total = 0, 1.0
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
            win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=50, min_game_count=20, min_win_pct=0.44,limitTop=40)
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
        lineups, archetype_map = generate_lineups(archetypes)
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

        #for lineup in lineups:
        #    if not usingEsportsArena:
        #        lineup = get_lineup(lineup, archetype_map)
        #    else:
        #        lineup = tuple(lineup)
        #    for lu_test in lineups_to_test:
        #        win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts)]
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
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(geometric_mean([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
        for i,j,k,l in lu_strings:
            if usingEsportsArena:
                print "%-20s: " % inverse[i]
            print "".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()
