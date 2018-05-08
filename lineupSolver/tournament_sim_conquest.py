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
    'AA_TEST4'           : "Taunt Druid,Control Priest,Quest Rogue,Cube Warlock".split(','),
    'AA_TEST5'           : "Taunt Druid,Tempo Mage,Quest Rogue,Cube Warlock".split(','),
    'A83650#2106'        : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'Babon#21904'        : ['Spiteful Druid', 'Control Priest', 'Cube Warlock', 'Odd Quest Warrior'],
    'BoarControl#2986'   : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'Bozzzton#2511'      : ['Tempo Mage', 'Murloc Paladin', 'Odd Rogue', 'Cube Warlock'],
    'Bunnyhoppor#2897'   : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'Casie#2884'         : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'Crane333#2314'      : ['Big Spell Mage', 'Even Paladin', 'Cube Warlock', 'Odd Warrior'],
    'Duarte#21328'       : ['Token Druid', 'Spell Hunter', 'Odd Paladin', 'Odd Warrior'],
    'ElMachico#2287'     : ['Tempo Mage', 'Even Paladin', 'Odd Rogue', 'Cube Warlock'],
    'Faeli#2572'         : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Findan#2596'        : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'Fox#29320'          : ['Big Spell Mage', 'Control Priest', 'Control Warlock', 'Odd Quest Warrior'],
    'Glaser#2196'        : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Hypno#22145'        : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Jarla#21553'        : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Juristis#2130'      : ['Odd Hunter', 'Tempo Mage', 'Murloc Paladin', 'Odd Rogue'],
    'Kalas#2638'         : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Kalaxz#2721'        : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'Kolento#2266'       : ['Taunt Druid', 'Even Paladin', 'Control Warlock', 'Odd Warrior'],
    'Leta#21458'         : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'MM78#2809'          : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Maur1#2225'         : ['Control Priest', 'Miracle Rogue', 'Cube Warlock', 'Odd Quest Warrior'],
    'Maverick#2233'      : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Meati#2841'         : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Quest Rogue'],
    'Mryagut#2306'       : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Nicslay#2567'       : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'NoName#13139'       : ['Even Paladin', 'Control Priest', 'Cube Warlock', 'Odd Warrior'],
    'Odemian#2999'       : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Orange#2309'        : ['Tempo Mage', 'Even Paladin', 'Control Priest', 'Cube Warlock'],
    'RENMEN#2291'        : ['Spiteful Druid', 'Spell Hunter', 'Control Warlock', 'Quest Warrior'],
    'Raena#2283'         : ['Control Priest', 'Shudderwock Shaman', 'Control Warlock', 'Odd Warrior'],
    'Rdu#2340'           : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Rikitikitavi#2184'  : ['Spiteful Druid', 'Big Spell Mage', 'Cube Warlock', 'Quest Warrior'],
    'Ronnie#2895'        : ['Spiteful Druid', 'Tempo Mage', 'Control Warlock', 'Odd Warrior'],
    'SCACC#2315'         : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Scruffy#2659'       : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Seiko#2721'         : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'ShtanUdachi#2202'   : ['Spiteful Druid', 'Spell Hunter', 'Control Warlock', 'Quest Warrior'],
    'Sintolol#2775'      : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'SpaDj#2732'         : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Cube Warlock'],
    'Springy#2781'       : ['Spiteful Druid', 'Big Spell Mage', 'Even Paladin', 'Cube Warlock'],
    'Swidz#2563'         : ['Taunt Druid', 'Big Spell Mage', 'Control Warlock', 'Odd Warrior'],
    'Thiddi#2854'        : ['Tempo Mage', 'Even Paladin', 'Combo Priest', 'Cube Warlock'],
    'ThijsNL#2223'       : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Trec#2878'          : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Turna#2738'         : ['Tempo Mage', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'Twink#21785'        : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Tyler#2449'         : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Viper#23812'        : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'Warma#2764'         : ['Quest Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'Windello#2498'      : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'Zhym#2678'          : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Zuhex#21312'        : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Zuka#2978'          : ['Taunt Druid', 'Tempo Mage', 'Control Priest', 'Control Warlock'],
    'anduriel#21364'     : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'bequiet#2179'       : ['Tempo Mage', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'dawido#2832'        : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'eilic#2496'         : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Quest Warrior'],
    'esteban#2504'       : ['Quest Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'fenomeno#21327'     : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'greensheep#2290'    : ['Odd Hunter', 'Tempo Mage', 'Murloc Paladin', 'Odd Rogue'],
    'hunterace#2217'     : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'iNS4NE#21840'       : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'ignite#21733'       : ['Taunt Druid', 'Big Spell Mage', 'Quest Rogue', 'Control Warlock'],
    'kolmari#2701'       : ['Spiteful Druid', 'Even Paladin', 'Cube Warlock', 'Odd Warrior'],
    'martim#2226'        : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'ntR#1799'           : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'pokrovac#2638'      : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'riku97#2895'        : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'tanaka#21918'       : ['Taunt Druid', 'Spell Hunter', 'Big Spell Mage', 'Cube Warlock'],
    'xBlyzes#2682'       : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'yogg#2768'          : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'zumpp#2702'         : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Quest Warrior'],
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
total_points = {}

sim_matchup, mu_pcts = get_sim_matchup(decks,win_pcts)
num_sims = 100000
for x in range(0, num_sims):
    randomize = {}
    tmp_players = list(decks.keys())
    shuffle(tmp_players)
    for Y in tmp_players:
        randomize[Y] = decks[Y]
    decks = randomize
    results = simulate_tournament(decks, rounds=7, win_pcts=win_pcts, simulate_matchup=sim_matchup)
    top8 = sorted(results.items(), key=lambda x:x[1])[-8:]
    for i, j in results.items():
        total_points[i] = total_points.get(i, 0) + j
    for i, j in top8:
        tops[i] = tops.get(i, 0) + 1
    if x % 50 == 0 and x > 0:
        print("sim %s" % x)

for i,j in sorted(tops.items(), key=lambda x:x[1], reverse=True):
    avg_points = round(float(total_points[i]) / num_sims, 1)
    print("%-20s %6s %5s %5s %s" % (i,j, avg_points, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))

