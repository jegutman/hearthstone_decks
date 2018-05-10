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
    #'TEST_1'                  : "Spiteful Druid,Murloc Paladin,Odd Rogue,Cube Warlock".split(','),
    'Alan870806'         : ['Spiteful Druid','Spell Hunter','Miracle Rogue','Cube Warlock'],
    'amnesiac'          : ['Spiteful Druid','Murloc Paladin','Odd Rogue','Control Warlock'],
    'AnguiStar'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Ant'                : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Apxvoid'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'bloodyface'         : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'chosenone'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'cthulukitty'        : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    #'Deathsie'           : ['Spiteful Druid','Even Paladin','Spiteful Priest','Control Warlock'],
    'Deathsie'           : ['Spiteful Druid','Even Paladin','Spiteful Druid','Control Warlock'],
    'docpwn'             : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Quest Rogue'],
    'dog'                : ['Spiteful Druid','Control Priest','Control Warlock','Odd Warrior'],
    'DrJikininki'        : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'ETC'               : ['Even Paladin','Control Priest','Quest Rogue','Control Warlock'],
    #'fibonacci'          : ['Spell Hunter','Control Priest','Control Warlock','Recruit Warrior'],
    #'fr0zen'             : ['Spell Hunter','Control Priest','Control Warlock','Recruit Warrior'],
    'fibonacci'          : ['Spell Hunter','Control Priest','Control Warlock','Odd Warrior'],
    'fr0zen'             : ['Spell Hunter','Control Priest','Control Warlock','Odd Warrior'],
    'Gallon'            : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'garifar'            : ['Odd Hunter','Tempo Mage','Murloc Paladin','Odd Rogue'],
    'Gladen'            : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'Greed'             : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Guiyze'             : ['Even Paladin','Odd Rogue','Even Shaman','Zoo Warlock'],
    'Houdinii'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'IrvinG'             : ['Spiteful Druid','Even Paladin','Control Priest','Cube Warlock'],
    'Joaquin'            : ['Tempo Mage','Even Paladin','Quest Rogue','Cube Warlock'],
    'Justine'            : ['Spiteful Druid','Tempo Mage','Control Priest','Control Warlock'],
    'justsaiyan'         : ['Spiteful Druid','Even Paladin','Odd Rogue','Control Warlock'],
    'killinallday'       : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'klei'              : ['Spiteful Druid','Even Paladin','Control Priest','Control Warlock'],
    'korextron'          : ['Spiteful Druid','Even Paladin','Control Priest','Control Warlock'],
    'lnguagehackr'       : ['Big Spell Mage','Control Priest','Control Warlock','Odd Warrior'],
    'Lucas'             : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'magkey'             : ['Big Spell Mage','Even Paladin','Control Priest','Cube Warlock'],
    'maxtheripper'       : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'Monsanto'           : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
    #'muzzy'              : ['Token Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'muzzy'              : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'N0lan'             : ['Taunt Druid','Even Paladin','Control Priest','Control Warlock'],
    'Nalguidan'          : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'noblord'            : ['Spiteful Druid','Even Paladin','Odd Rogue','Control Warlock'],
    'PapaJason'          : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'Perna'              : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Pinche'            : ['Odd Hunter','Tempo Mage','Even Paladin','Odd Rogue'],
    'Pizza'              : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Pksnow'             : ['Spiteful Druid','Even Paladin','Miracle Rogue','Control Warlock'],
    'PNC'                : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Purple'             : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'Quiros2211'         : ['Taunt Druid','Control Priest','Quest Rogue','Cube Warlock'],
    'Rase'               : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'rayC'              : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'RealTerror'         : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'Ryuuzu'             : ['Taunt Druid','Control Priest','Quest Rogue','Control Warlock'],
    'SATANCURSEYO'       : ['Spiteful Druid','Murloc Paladin','Odd Rogue','Control Warlock'],
    'seiger'             : ['Even Paladin','Control Priest','Quest Rogue','Cube Warlock'],
    'seohyun628'         : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'SilentStorm'       : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Sneakyche'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'SnipedAgain'        : ['Taunt Druid','Murloc Paladin','Control Priest','Control Warlock'],
    'strifecro'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Odd Rogue'],
    'SwaggyG'            : ['Even Paladin','Odd Rogue','Even Shaman','Zoo Warlock'],
    'T4COTASTIC'         : ['Taunt Druid','Even Paladin','Control Priest','Cube Warlock'],
    'Tarei'             : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Terrencem'          : ['Even Paladin','Odd Rogue','Even Shaman','Cube Warlock'],
    'TheJordude'         : ['Taunt Druid','Spell Hunter','Control Warlock','Odd Warrior'],
    'TheMaverick'        : ['Tempo Mage','Even Paladin','Control Priest','Control Warlock'],
    'Tuliowz'            : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'UchihaSaske'       : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'ute1234'            : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'villain'            : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
    'wabeka'             : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'wiz'               : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'XisBau5e'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'yinus'              : ['Taunt Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    #'yoitsflo'           : ['Token Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'yoitsflo'           : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'zalae'              : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'zlsjs'              : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
}

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
