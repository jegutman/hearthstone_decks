import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

from random import shuffle

decks = {
    'AA_TEST'            : ['Spiteful Druid', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'AA_TEST2'           : ['Spiteful Druid','Murloc Paladin','Quest Rogue','Cube Warlock'],
    'AA_TEST3'           : ['Spiteful Druid','Murloc Paladin','Tempo Mage','Cube Warlock'],
    'AA_TEST4'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'A83650'        : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'Babon'        : ['Spiteful Druid', 'Control Priest', 'Cube Warlock', 'Odd Quest Warrior'],
    'BoarControl'   : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'Bozzzton'      : ['Tempo Mage', 'Murloc Paladin', 'Odd Rogue', 'Cube Warlock'],
    'Bunnyhoppor'   : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'Casie'         : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'Crane333'      : ['Big Spell Mage', 'Even Paladin', 'Cube Warlock', 'Odd Warrior'],
    'Duarte'       : ['Token Druid', 'Spell Hunter', 'Odd Paladin', 'Odd Warrior'],
    'ElMachico'     : ['Tempo Mage', 'Even Paladin', 'Odd Rogue', 'Cube Warlock'],
    'Faeli'         : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Findan'        : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'Fox'          : ['Big Spell Mage', 'Control Priest', 'Control Warlock', 'Odd Quest Warrior'],
    'Glaser'        : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Hypno'        : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Jarla'        : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Juristis'      : ['Odd Hunter', 'Tempo Mage', 'Murloc Paladin', 'Odd Rogue'],
    'Kalas'         : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Kalaxz'        : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'Kolento'       : ['Taunt Druid', 'Even Paladin', 'Control Warlock', 'Odd Warrior'],
    'Leta'         : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'MM78'          : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Maur1'         : ['Control Priest', 'Miracle Rogue', 'Cube Warlock', 'Odd Quest Warrior'],
    'Maverick'      : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Meati'         : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Quest Rogue'],
    'Mryagut'       : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Nicslay'       : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'NoName'       : ['Even Paladin', 'Control Priest', 'Cube Warlock', 'Odd Warrior'],
    'Odemian'       : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Orange'        : ['Tempo Mage', 'Even Paladin', 'Control Priest', 'Cube Warlock'],
    'RENMEN'        : ['Spiteful Druid', 'Spell Hunter', 'Control Warlock', 'Quest Warrior'],
    'Raena'         : ['Control Priest', 'Shudderwock Shaman', 'Control Warlock', 'Odd Warrior'],
    'Rdu'           : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Rikitikitavi'  : ['Spiteful Druid', 'Big Spell Mage', 'Cube Warlock', 'Quest Warrior'],
    'Ronnie'        : ['Spiteful Druid', 'Tempo Mage', 'Control Warlock', 'Odd Warrior'],
    'SCACC'         : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Scruffy'       : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Seiko'         : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'ShtanUdachi'   : ['Spiteful Druid', 'Spell Hunter', 'Control Warlock', 'Quest Warrior'],
    'Sintolol'      : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'SpaDj'         : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Cube Warlock'],
    'Springy'       : ['Spiteful Druid', 'Big Spell Mage', 'Even Paladin', 'Cube Warlock'],
    'Swidz'         : ['Taunt Druid', 'Big Spell Mage', 'Control Warlock', 'Odd Warrior'],
    'Thiddi'        : ['Tempo Mage', 'Even Paladin', 'Combo Priest', 'Cube Warlock'],
    'ThijsNL'       : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Trec'          : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Turna'         : ['Tempo Mage', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'Twink'        : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Tyler'         : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Viper'        : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'Warma'         : ['Quest Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'Windello'      : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'Zhym'          : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Zuhex'        : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Zuka'          : ['Taunt Druid', 'Tempo Mage', 'Control Priest', 'Control Warlock'],
    'anduriel'     : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'bequiet'       : ['Tempo Mage', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'dawido'        : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'eilic'         : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Quest Warrior'],
    'esteban'       : ['Quest Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'fenomeno'     : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'greensheep'    : ['Odd Hunter', 'Tempo Mage', 'Murloc Paladin', 'Odd Rogue'],
    'hunterace'     : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'iNS4NE'       : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'ignite'       : ['Taunt Druid', 'Big Spell Mage', 'Quest Rogue', 'Control Warlock'],
    'kolmari'       : ['Spiteful Druid', 'Even Paladin', 'Cube Warlock', 'Odd Warrior'],
    'martim'        : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'ntR'           : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'pokrovac'      : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'riku97'        : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'tanaka'       : ['Taunt Druid', 'Spell Hunter', 'Big Spell Mage', 'Cube Warlock'],
    'xBlyzes'       : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'yogg'          : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'zumpp'         : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Quest Warrior'],
}

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)

tops = {}

#def simulate_tournament(decks, rounds, scores=None, win_pcts={}):
#    if scores == None:
#        for d in decks:
#            scores[d.name] = 0
#    for i in range(0, rounds):
#        simulate_round(decks, scores, win_pcts)
#    return scores

lineups = list(set([tuple(i) for i in decks.values()]))
mu_pcts = {}
for i in range(0, len(lineups)):
    for j in range(i, len(lineups)):
        l1 = tuple(lineups[i])
        l2 = tuple(lineups[j])
        sim_res = calculate_win_rate(list(l1), list(l2), win_pcts)
        sim_res2 = calculate_win_rate(list(l2), list(l1), win_pcts)
        if sim_res + sim_res2 < 0.98:
            l1 = '"' + ",".join(list(l1)) + '"'
            l2 = '"' + ",".join(list(l2)) + '"'
            print("%s %-50s %-50s %s %s %s" % (sim_res+sim_res2, l1, l2, sim_res, sim_res2, sim_res+sim_res2))
