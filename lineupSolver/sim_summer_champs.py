import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 
from sim_matchup import *

from random import shuffle

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
overrides = [
            ]
win_pcts = override_wr(overrides,win_pcts)

tops = {}

#def simulate_tournament(decks, rounds, scores=None, win_pcts={}):
#    if scores == None:
#        for d in decks:
#            scores[d.name] = 0
#    for i in range(0, rounds):
#        simulate_round(decks, scores, win_pcts)
#    return scores

d1 = decks[sys.argv[1]]
d2 = decks[sys.argv[2]]

print(calculate_win_rate(d1, d2, win_pcts))
print(sim(d1, d2))
print(cq_bans(d1, d2))
