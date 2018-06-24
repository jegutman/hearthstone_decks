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
            ]
win_pcts = override_wr(overrides,win_pcts)
sim_matchup, mu_pcts = get_sim_matchup(decks,win_pcts)
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
        print("%-20s %6s %5s %s" % (i,j, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))