from hgg_matches import *
from hgg_utils import *
from json_win_rates import *
win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)


#Team,Week,Druid,Hunter,Mage,Paladin,Priest,Rogue,Shaman,Warlock,Warrior,Banned 1,Pick 1,Pick 1,Banned 2,Banned 2,Pick 2,Pick 2,Banned 3,Pick 3
#filename = 'week3_lineups.csv'
#week_file = open(filename)
#lines = [line.strip() for line in week_file]
#team_lineups = {}
#team_played = {}
#team_pick_ban = {}
#archetypes = []
#for line in lines:
#    tmp = line.split(',')
#    team, week = tmp[:2]
#    lineup = tmp[2:11]
#    for l in lineup:
#        if l not in archetypes:
#            archetypes.append(l)
#    ban1, pick1, pick2, ban2, ban3, pick3, pick4, ban4, pick5 = tmp[11:]
#    team_lineups[team] = lineup
#    played = [l for l in lineup if l not in [ban1, ban2, ban3, ban4]]
#    team_played[team] = played
#    team_pick_ban[team] = [ban1, pick1, pick2, ban2, ban3, pick3, pick4, ban4, pick5]

# NEW FORMAT
filename = 'top16_lineups.csv'
week_file = open(filename)
lines = [line.strip() for line in week_file]
team_lineups = {}
archetypes = []
for line in lines:
    tmp = line.split(',')
    team = tmp[0]
    lineup = tmp[1:10]
    for l in lineup:
        if l not in archetypes:
            archetypes.append(l)
    team_lineups[team] = lineup

#for i,j in round9:
#    l1 = team_lineups[i]
#    l2 = team_lineups[j]
#    mu = HGG_Matchup(l1, l2, win_pcts=win_pcts, clear_initialize=True)
#    calc = mu.calculate()
#    res = [i,j, calc]
#    print(",".join([str(x) for x in res]))
#
#for i,j in round9:
#    l1 = team_lineups[j]
#    l2 = team_lineups[i]
#    mu = HGG_Matchup(l1, l2, win_pcts=win_pcts, clear_initialize=True)
#    calc = mu.calculate()
#    res = [j,i, calc]
#    print(",".join([str(x) for x in res]))


# CODE FOR PRE vs POST-QUEUE
for i,j in round9:
    try:
        order = round9_final_order[(i,j)]
    except:
        continue
    l1_order, l2_order = list(zip(*order))
    if l1_order[0] == 'FillInHere': continue
    l1_order = list(l1_order)
    l2_order = list(l2_order)
    #l1 = sorted(l1_played, key=lambda x:l1_order.index(x.split(' ')[-1]))
    #l2 = sorted(team_played[j], key=lambda x:l2_order.index(x.split(' ')[-1]))
    l1 = [d for d in team_lineups[i] if d.split(' ')[-1] in l1_order]
    l2 = [d for d in team_lineups[j] if d.split(' ')[-1] in l2_order]
    l1 = sorted(l1, key=lambda x:l1_order.index(x.split(' ')[-1]))
    l2 = sorted(l2, key=lambda x:l2_order.index(x.split(' ')[-1]))
    final = round(eval_one(l1, l2, win_pcts) * 100, 1)
    #for i,j in zip(l1, l2):
    #    print("%s,%s,%s" % (i, j, win_pcts[(i, j)]))
    pre_order = round(eval_final_calc(l1, l2, win_pcts) * 100, 1)
    diff = round(final - pre_order, 1)
    res = [i,j, pre_order, final]
    print(",".join([str(x) for x in res]))

