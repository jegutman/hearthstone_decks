import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

from random import shuffle

eu_decks = {
    #'AA_TEST'            : ['Spiteful Druid', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    #'AA_TEST2'           : ['Spiteful Druid','Murloc Paladin','Quest Rogue','Cube Warlock'],
    #'AA_TEST3'           : ['Spiteful Druid','Murloc Paladin','Tempo Mage','Cube Warlock'],
    #'AA_TEST4'           : "Taunt Druid,Control Priest,Quest Rogue,Cube Warlock".split(','),
    #'AA_TEST5'           : "Taunt Druid,Tempo Mage,Quest Rogue,Cube Warlock".split(','),
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

decks = {
    #'TEST_1'                  : "Spiteful Druid,Murloc Paladin,Odd Rogue,Cube Warlock".split(','),
    'Alan870806#1754'         : ['Spiteful Druid','Spell Hunter','Miracle Rogue','Cube Warlock'],
    'amnesiac#11705'          : ['Spiteful Druid','Murloc Paladin','Odd Rogue','Control Warlock'],
    'AnguiStar#1109'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Ant#1974'                : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Apxvoid#11872'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'bloodyface#1414'         : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'chosenone#1133'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'cthulukitty#1446'        : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    #'Deathsie#1201'           : ['Spiteful Druid','Even Paladin','Spiteful Priest','Control Warlock'],
    'Deathsie#1201'           : ['Spiteful Druid','Even Paladin','Spiteful Druid','Control Warlock'],
    'docpwn#1485'             : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Quest Rogue'],
    'dog#1593'                : ['Spiteful Druid','Control Priest','Control Warlock','Odd Warrior'],
    'DrJikininki#1889'        : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'ETC#11729'               : ['Even Paladin','Control Priest','Quest Rogue','Control Warlock'],
    #'fibonacci#1545'          : ['Spell Hunter','Control Priest','Control Warlock','Recruit Warrior'],
    #'fr0zen#1184'             : ['Spell Hunter','Control Priest','Control Warlock','Recruit Warrior'],
    'fibonacci#1545'          : ['Spell Hunter','Control Priest','Control Warlock','Odd Warrior'],
    'fr0zen#1184'             : ['Spell Hunter','Control Priest','Control Warlock','Odd Warrior'],
    'Gallon#11212'            : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'garifar#1898'            : ['Odd Hunter','Tempo Mage','Murloc Paladin','Odd Rogue'],
    'Gladen#11397'            : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'Greed#12707'             : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Guiyze#1681'             : ['Even Paladin','Odd Rogue','Even Shaman','Zoo Warlock'],
    'Houdinii#1378'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'IrvinG#1619'             : ['Spiteful Druid','Even Paladin','Control Priest','Cube Warlock'],
    'Joaquin#1259'            : ['Tempo Mage','Even Paladin','Quest Rogue','Cube Warlock'],
    'Justine#1262'            : ['Spiteful Druid','Tempo Mage','Control Priest','Control Warlock'],
    'justsaiyan#1493'         : ['Spiteful Druid','Even Paladin','Odd Rogue','Control Warlock'],
    'killinallday#1537'       : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'klei#11805'              : ['Spiteful Druid','Even Paladin','Control Priest','Control Warlock'],
    'korextron#1532'          : ['Spiteful Druid','Even Paladin','Control Priest','Control Warlock'],
    'lnguagehackr#1412'       : ['Big Spell Mage','Control Priest','Control Warlock','Odd Warrior'],
    'Lucas#12819'             : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'magkey#1730'             : ['Big Spell Mage','Even Paladin','Control Priest','Cube Warlock'],
    'maxtheripper#1454'       : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'Monsanto#1657'           : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
    #'muzzy#1105'              : ['Token Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'muzzy#1105'              : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'N0lan#11919'             : ['Taunt Druid','Even Paladin','Control Priest','Control Warlock'],
    'Nalguidan#1733'          : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'noblord#1509'            : ['Spiteful Druid','Even Paladin','Odd Rogue','Control Warlock'],
    'PapaJason#1186'          : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'Perna#1691'              : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Pinche#11361'            : ['Odd Hunter','Tempo Mage','Even Paladin','Odd Rogue'],
    'Pizza#1279'              : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Pksnow#1547'             : ['Spiteful Druid','Even Paladin','Miracle Rogue','Control Warlock'],
    'PNC#1102'                : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Purple#1567'             : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'Quiros2211#1746'         : ['Taunt Druid','Control Priest','Quest Rogue','Cube Warlock'],
    'Rase#1355'               : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'rayC#11391'              : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'RealTerror#1827'         : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'Ryuuzu#1203'             : ['Taunt Druid','Control Priest','Quest Rogue','Control Warlock'],
    'SATANCURSEYO#1263'       : ['Spiteful Druid','Murloc Paladin','Odd Rogue','Control Warlock'],
    'seiger#1577'             : ['Even Paladin','Control Priest','Quest Rogue','Cube Warlock'],
    'seohyun628#1679'         : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'SilentStorm#13722'       : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Sneakyche#1872'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'SnipedAgain#1736'        : ['Taunt Druid','Murloc Paladin','Control Priest','Control Warlock'],
    'strifecro#1914'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Odd Rogue'],
    'SwaggyG#1193'            : ['Even Paladin','Odd Rogue','Even Shaman','Zoo Warlock'],
    'T4COTASTIC#1121'         : ['Taunt Druid','Even Paladin','Control Priest','Cube Warlock'],
    'Tarei#11497'             : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Terrencem#1843'          : ['Even Paladin','Odd Rogue','Even Shaman','Cube Warlock'],
    'TheJordude#1239'         : ['Taunt Druid','Spell Hunter','Control Warlock','Odd Warrior'],
    'TheMaverick#1720'        : ['Tempo Mage','Even Paladin','Control Priest','Control Warlock'],
    'Tuliowz#1870'            : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'UchihaSaske#11453'       : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'ute1234#1252'            : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'villain#1999'            : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
    'wabeka#1626'             : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'wiz#11841'               : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'XisBau5e#1825'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'yinus#1258'              : ['Taunt Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    #'yoitsflo#1202'           : ['Token Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'yoitsflo#1202'           : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'zalae#1766'              : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'zlsjs#1181'              : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
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

overrides = [
    ('Zoo Warlock', 'Even Paladin', .47),
    ('Zoo Warlock', 'Tempo Mage', .55),
    ('Zoo Warlock', 'Odd Rogue', .42),
    ('Zoo Warlock', 'Spiteful Druid', .50),
    ('Zoo Warlock', 'Cube Warlock', .30),
    ('Zoo Warlock', 'Control Warlock', .30),
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

    ('Control Priest', 'Quest Rogue', .42),
    ('Control Priest', 'Spiteful Druid', .40),
    ('Tempo Mage', 'Quest Rogue', 0.63),
    ('Even Paladin', 'Quest Rogue', 0.63),
            ]
win_pcts = override_wr(overrides,win_pcts)
sim_matchup, mu_pcts = get_sim_matchup(decks,win_pcts)
num_sims = 100000
both = 0
one = 0
for x in range(0, num_sims):
    randomize = {}
    tmp_players = list(decks.keys())
    shuffle(tmp_players)
    for Y in tmp_players:
        randomize[Y] = decks[Y]
    decks = randomize
    results = simulate_tournament(decks, rounds=7, win_pcts=win_pcts, simulate_matchup=sim_matchup)
    top8 = sorted(results.items(), key=lambda x:x[1])[-8:]
    top8_players = [i for (i,j) in top8]
    if 'Guiyze#1681' in top8_players or 'Terrencem#1843' in top8_players:
        one += 1
    if 'Guiyze#1681' in top8_players and 'Terrencem#1843' in top8_players:
        both += 1
    for i, j in results.items():
        total_points[i] = total_points.get(i, 0) + j
    for i, j in top8:
        tops[i] = tops.get(i, 0) + 1
    if x % 50 == 0 and x > 0:
        print("sim %s" % x)

for i,j in sorted(tops.items(), key=lambda x:x[1], reverse=True):
    avg_points = round(float(total_points[i]) / num_sims, 1)
    print("%-20s %6s %5s %5s %s" % (i,j, avg_points, (str(round(float(j) / num_sims * 100., 1)) + '%'), str(decks[i])))

print("ONE:",str(round(float(one) / num_sims * 100., 1)))
print("BOTH:",str(round(float(both) / num_sims * 100., 1)))
