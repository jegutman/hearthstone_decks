import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

decks = {
    'A83650'             : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'BloodTrail'         : ['Taunt Druid', 'Recruit Hunter', 'Shudderwock Shaman', 'Even Warlock'],
    'Bunnyhoppor'        : ['Big Spell Mage', 'Miracle Rogue', 'Shudderwock Shaman', 'Even Warlock'],
    'Dog'                : ['Taunt Druid', 'Combo Priest', 'Shudderwock Shaman', 'Even Warlock'],
    'Glory'              : ['Taunt Druid', 'Miracle Rogue', 'Shudderwock Shaman', 'Cube Warlock'],
    'Jinsoo'             : ['Big Spell Mage', 'Control Priest', 'Miracle Rogue', 'Even Warlock'],
    'killinallday'       : ['Token Druid', 'Odd Paladin', 'Even Shaman', 'Even Warlock'],
    'Leaoh'              : ['Token Druid', 'Odd Paladin', 'Shudderwock Shaman', 'Cube Warlock'],
    'Nalguidan'          : ['Taunt Druid', 'Recruit Hunter', 'Miracle Rogue', 'Shudderwock Shaman'],
    'Rase'               : ['Taunt Druid', 'Big Spell Mage', 'Shudderwock Shaman', 'Quest Warrior'],
    'Rugal'              : ['Taunt Druid', 'Big Spell Mage', 'Control Priest', 'Even Warlock'],
    'Tansoku'            : ['Taunt Druid', 'Recruit Hunter', 'Miracle Rogue', 'Even Warlock'],
    'Turna'              : ['Token Druid', 'Odd Paladin', 'Even Shaman', 'Even Warlock'],
    'Viper'              : ['Big Spell Mage', 'Miracle Rogue', 'Shudderwock Shaman', 'Even Warlock'],
    'XiaoT'              : ['Spiteful Druid', 'Recruit Hunter', 'Miracle Rogue', 'Even Warlock'],
    'YuYi'               : ['Taunt Druid', 'Miracle Rogue', 'Even Shaman', 'Even Warlock'],
}

groups = [
    ['Rase', 'Viper', 'XiaoT', 'Tansoku'],
    ['A83650', 'BloodTrail', 'Nalguidan', 'YuYi'],
    ['Jinsoo', 'Rugal', 'Turna', 'Dog'],
    ['Leaoh', 'killinallday', 'Glory', 'Bunnyhoppor'],
]

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)



def sim_group(decks, win_pcts, simulate_matchup):
    results = simulate_tournament(decks, rounds=2, win_pcts=win_pcts, simulate_matchup=simulate_matchup)
    results = [i[0] for i in sorted(results.items(), key=lambda x:x[1])]
    first = results[3]
    if simulate_matchup(decks[results[1]], decks[results[2]], win_pcts):
        second = results[1]
    else:
        second = results[2]
    return first, second
    

total_points = {}

overrides = [
    ('Big Spell Mage', 'Even Warlock', 0.67),
    ('Big Spell Mage', 'Taunt Druid', 0.7),
    ('Miracle Rogue', 'Even Warlock', 0.62),
    ('Shudderwock Shaman', 'Even Warlock', 0.6),
            ]
win_pcts = override_wr(overrides,win_pcts)
sim_matchup, mu_pcts = get_sim_matchup(decks,win_pcts)
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
            bracket[5] = second
        elif y == 1:
            bracket[1] = first
            bracket[4] = second
        elif y == 2:
            bracket[2] = first
            bracket[7] = second
        elif y == 3:
            bracket[3] = first
            bracket[6] = second
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
    if x % 500 == 0:
        print(x)

tops = {}
for i in firsts:
    tops[i] = firsts[i]

for i,j in sorted(tops.items(), key=lambda x:x[1], reverse=True):
    #avg_points = round(float(total_points[i]) / num_sims, 1)
    #print("%-20s %6s %5s %5s %s" % (i,j, avg_points, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))
    print("%-20s %6s %5s %s" % (i,j, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))
