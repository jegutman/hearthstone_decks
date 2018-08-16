import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
sys.path.append(basedir + '/TourStopLoader')
import random

from rate_hs_elo import *

from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

decks = {
    'amnesiac'  :  'Malygos Druid,Zoo Warlock,Odd Rogue,Odd Paladin'.split(','),
    'che0nsu'  :  'Malygos Druid,Spell Hunter,Odd Rogue,Even Paladin'.split(','),
    'cosmo'  :  'Malygos Druid,Spell Hunter,Even Warlock,Odd Rogue'.split(','),
    'dacmalza'  :  'Spell Hunter,Even Warlock,Odd Rogue,Control Priest'.split(','),
    'fungggg'  :  'Malygos Druid,Spell Hunter,Odd Rogue,Tempo Mage'.split(','),
    'kuonet'  :  'Taunt Druid,Deathrattle Hunter,Even Warlock,Shudderwock Shaman'.split(','),
    'lii'  :  'Malygos Druid,Deathrattle Hunter,Control Warlock,Odd Warrior'.split(','),
    #'lucas'  :  'Token Druid,Spell Hunter,Odd Rogue,Token Shaman'.split(','),
    'lucas'  :  'Token Druid,Spell Hunter,Odd Rogue,Shudderwock Shaman'.split(','),
    'monsanto'  :  'Malygos Druid,Even Warlock,Tempo Rogue,Control Warrior'.split(','),
    #'monsanto'  :  'Malygos Druid,Even Warlock,Tempo Rogue,Odd Warrior'.split(','),
    'muzzy'  :  'Big Druid,Deathrattle Hunter,Tempo Rogue,Mech Paladin'.split(','),
    'perna'  :  'Big Druid,Deathrattle Hunter,Even Warlock,Deathrattle Rogue'.split(','),
    'pnc'  :  'Malygos Druid,Deathrattle Hunter,Control Warlock,Odd Warrior'.split(','),
    'rase'  :  'Big Druid,Deathrattle Hunter,Even Warlock,Deathrattle Rogue'.split(','),
    'swidz'  :  'Malygos Druid,Even Warlock,Control Warrior,Control Priest'.split(','),
    #'swidz'  :  'Malygos Druid,Even Warlock,Odd Warrior,Control Priest'.split(','),
    'teamamerica'  :  'Malygos Druid,Deathrattle Hunter,Zoo Warlock,Odd Rogue'.split(','),
    'topopablo11'  :  'Big Druid,Deathrattle Hunter,Zoo Warlock,Deathrattle Rogue'.split(','),
}

groups = [
    ['monsanto', 'lucas', 'che0nsu', 'muzzy'],
    ['rase', 'teamamerica', 'topopablo11', 'pnc'],
    ['kuonet', 'lii', 'fungggg', 'amnesiac'],
    ['swidz', 'perna', 'cosmo', 'dacmalza'],
]

for player in decks.keys():
    print "%-13s" % player,rating[player]

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)



def sim_group(decks, win_pcts, simulate_matchup):
    results = simulate_tournament(decks, rounds=2, win_pcts=win_pcts, simulate_matchup=simulate_matchup)
    results = [i[0] for i in sorted(results.items(), key=lambda x:x[1])]
    first = results[3]
    if simulate_matchup(results[1], results[2], decks[results[1]], decks[results[2]], win_pcts):
        second = results[1]
    else:
        second = results[2]
    return first, second
    

total_points = {}

overrides = [
            ]
win_pcts = override_wr(overrides,win_pcts)
#sim_matchup, mu_pcts = get_sim_matchup(decks,win_pcts)
sim_matchup, mu_pcts = get_sim_matchup_rating(decks,win_pcts, rating)
#def sim_matchup(p1, p2, l1, l2, win_pcts):
#    pct = expect_score_local(rating[p1.lower()].mu, rating[p2.lower()].mu)
#    if random.random() < pct:
#        return 1
#    return 0

num_sims = 100000
firsts = {}
seconds = {}
for x in range(0, num_sims):
    #bracket = []
    bracket = [0, 0, 0, 0, 0, 0, 0, 0]
    for y in range(0, 4):
        #print(y)
        tmp_decks = {}
        tmp_group = groups[y]
        for player in (tmp_group[0], tmp_group[2], tmp_group[1], tmp_group[3]):
            tmp_decks[player] = decks[player]
        first, second = sim_group(tmp_decks, win_pcts=win_pcts, simulate_matchup=sim_matchup)
        if y == 0:
            bracket[0] = first
            bracket[7] = second
        elif y == 1:
            bracket[1] = first
            bracket[6] = second
        elif y == 2:
            bracket[2] = first
            bracket[5] = second
        elif y == 3:
            bracket[3] = first
            bracket[4] = second
        #print(y)
        #bracket.append(first)
        #bracket.append(second)
    #print(bracket)
    tmp_decks = {}
    for player in bracket:
        tmp_decks[player] = decks[player]
    bracket_res = simulate_tournament(tmp_decks, rounds=3, win_pcts=win_pcts, simulate_matchup=sim_matchup)
    bracket_res = [i[0] for i in sorted(bracket_res.items(), key=lambda x:x[1])]
    first = bracket_res[-1]
    firsts[first] = firsts.get(first, 0) + 1
    #bracket_res = simulate_tournament(tmp_decks, rounds=1, win_pcts=win_pcts, simulate_matchup=sim_matchup)
    #bracket_res = [i[0] for i in sorted(bracket_res.items(), key=lambda x:x[1])]
    #worlds = bracket_res[-4:]
    #for p in worlds:
    #    firsts[p] = firsts.get(p, 0) + 1
    #if x % 500 == 0:
    #    print(x)

tops = {}
for i in firsts:
    tops[i] = firsts[i]

for i,j in sorted(tops.items(), key=lambda x:x[1], reverse=True):
    #avg_points = round(float(total_points[i]) / num_sims, 1)
    #print("%-20s %6s %5s %5s %s" % (i,j, avg_points, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))
    #print("%-20s %6s %5s %s" % (i,j, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))
    print("%-20s %5s" % (i, (str(round(float(j) / num_sims * 100., 1)) + '%'), ))
    #print("%s,%s" % (i, (str(round(float(j) / num_sims * 100., 1)) + '%'), ))

num_sims = 100000
letters = ['A', 'B', 'C', 'D']
for y in range(0, 4):
    print('\n', 'Group:', letters[y])
    firsts = {}
    seconds = {}
    for x in range(0, num_sims):
        tmp_decks = {}
        group = groups[y]
        for player in (group[0], group[2], group[1], group[3]):
            tmp_decks[player] = decks[player]
        first, second = sim_group(tmp_decks, win_pcts=win_pcts, simulate_matchup=sim_matchup)
        firsts[first] = firsts.get(first, 0) + 1
        seconds[second] = seconds.get(second, 0) + 1

    tops = {}
    for i in firsts:
        tops[i] = firsts[i] + seconds[i]

    for i,j in sorted(tops.items(), key=lambda x:x[1], reverse=True):
        #avg_points = round(float(total_points[i]) / num_sims, 1)
        #print("%-20s %6s %5s %5s %s" % (i,j, avg_points, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))
        #print("%-20s %6s %5s %s" % (i,j, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))
        print("%-20s %5s" % (i, (str(round(float(j) / num_sims * 100., 1)) + '%')))
        #print("%s,%5s" % (i, (str(round(float(j) / num_sims * 100., 1)) + '%')))
